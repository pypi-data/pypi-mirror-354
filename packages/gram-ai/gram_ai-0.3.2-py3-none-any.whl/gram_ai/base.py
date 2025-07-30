from dataclasses import dataclass
import functools
import json
from typing import Any, Awaitable, Callable, Dict, List, Optional, Union
import httpx

from gram_ai import VERSION
from gram_ai.environments import get_server_url_by_key
from gram_ai.utils.retries import BackoffStrategy, Retries, RetryConfig, retry_async, retry
from gram_ai import GramAPI


@dataclass
class GramInstanceRequest:
    project: str
    toolset: str
    environment: Optional[str] = None


@dataclass
class BaseTool:
    name: str
    description: str
    parameters: Dict[str, Any]
    execute: Callable[[Union[Dict[str, Any], str]], Awaitable[str]]
    execute_sync: Callable[[Union[Dict[str, Any], str]], str]


_default_retry_policy = Retries(
    config=RetryConfig(
        strategy="backoff",
        backoff=BackoffStrategy(
            initial_interval=500,
            max_interval=60000,
            exponent=1.5,
            max_elapsed_time=3600000,
        ),
        retry_connection_errors=True,
    ),
    status_codes=["429", "5XX"],
)


class BaseAdapter:
    _api_key: str
    _server_url: str
    _environment_variables: Dict[str, str]
    _cache: Dict[str, List[BaseTool]]
    _core: GramAPI

    def __init__(
        self,
        *,
        api_key: str,
        environment_variables: Optional[Dict[str, str]] = None,
    ):
        self._api_key = api_key
        self._environment_variables = environment_variables or {}
        self._server_url = get_server_url_by_key(api_key)
        self._core = GramAPI(server_url=self._server_url)
        self._cache = {}

    async def _do_request_for_tool_execution(self, request: httpx.Request) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            return await client.send(request)

    def _do_request_for_tool_execution_sync(self, request: httpx.Request) -> httpx.Response:
        with httpx.Client() as client:
            return client.send(request)
    
    def prompt(
        self,
        project: str,
        name: str,
        args: Dict[str, Any],
    ) -> str:
        prompt = self._core.templates.get(
            name=name,
            security={
                "option2": {
                    "apikey_header_gram_key": self._api_key,
                    "project_slug_header_gram_project": project,
                }
            },
        )
        response = self._core.templates.render(
            id=prompt.template.id,
            render_template_request_body={"arguments": args},
            security={
                "option2": {
                    "apikey_header_gram_key": self._api_key,
                    "project_slug_header_gram_project": project,
                }
            },
        )
        return response.prompt

    def _base_tools(
        self, request: GramInstanceRequest
    ) -> List[BaseTool]:
        key = f"{request.project}:{request.toolset}:{request.environment or ''}"

        if key in self._cache:
            return self._cache[key]
        
        instance = self._core.instances.get_by_slug(
            security={
                "option2": {
                    "apikey_header_gram_key": self._api_key,
                    "project_slug_header_gram_project": request.project,
                }
            },
            toolset_slug=request.toolset,
            environment_slug=request.environment,
        )

        tools: List[BaseTool] = []
        
        for prompt in (instance.prompt_templates or []):
            if prompt.kind == "higher_order_tool":
                schema = json.loads(prompt.arguments) if prompt.arguments else {}
                async def execute_higher_order_tool_async_impl(
                    input_data: Union[Dict[str, Any], str],
                    _prompt_id: str = prompt.id,
                ) -> str:
                    parsed_input: Any
                    if isinstance(input_data, str):
                        try:
                            parsed_input = json.loads(input_data)
                        except json.JSONDecodeError as e:
                            raise ValueError("Error parsing input string for tool call.") from e
                    else:
                        parsed_input = input_data
                    response = await self._core.templates.render_async(
                        id=_prompt_id,
                        render_template_request_body={"arguments": parsed_input},
                        security={
                            "option2": {
                                "apikey_header_gram_key": self._api_key,
                                "project_slug_header_gram_project": request.project,
                            }
                        },
                    )
                    return response.prompt
                def execute_higher_order_tool_sync_impl(
                    input_data: Union[Dict[str, Any], str],
                    _prompt_id: str = prompt.id,
                ) -> str:
                    parsed_input: Any
                    if isinstance(input_data, str):
                        try:
                            parsed_input = json.loads(input_data)
                        except json.JSONDecodeError as e:
                            raise ValueError("Error parsing input string for tool call.") from e
                    else:
                        parsed_input = input_data
                    response = self._core.templates.render(
                        id=_prompt_id,
                        render_template_request_body={"arguments": parsed_input},
                        security={
                            "option2": {
                                "apikey_header_gram_key": self._api_key,
                                "project_slug_header_gram_project": request.project,
                            }
                        },
                    )
                    return response.prompt
            tools.append(
                BaseTool(
                    name=prompt.name,
                    description=prompt.description or "",
                    parameters=schema,
                    execute=execute_higher_order_tool_async_impl,
                    execute_sync=execute_higher_order_tool_sync_impl,
                )
            )

        for tool_data in instance.tools:
            schema = json.loads(tool_data.schema_) if tool_data.schema_ else {}

            async def execute_tool_async_impl(
                input_data: Union[Dict[str, Any], str],
                _tool_id: str = tool_data.id,
                _project: str = request.project,
                _environment: Optional[str] = request.environment,
            ) -> str:
                url, params, headers, payload = self._prepare_http_request_args(input_data, _tool_id, _project, _environment)
                
                http_request = httpx.Request(
                    "POST", url=url, params=params, headers=headers, content=json.dumps(payload)
                )
                
                response = await retry_async(
                    functools.partial(self._do_request_for_tool_execution, http_request),
                    _default_retry_policy,
                )
                response.raise_for_status()
                return response.text

            def execute_tool_sync_impl(
                input_data: Union[Dict[str, Any], str],
                _tool_id: str = tool_data.id,
                _project: str = request.project,
                _environment: Optional[str] = request.environment,
            ) -> str:
                url, params, headers, payload = self._prepare_http_request_args(input_data, _tool_id, _project, _environment)

                http_request = httpx.Request(
                    "POST", url=url, params=params, headers=headers, content=json.dumps(payload)
                )

                response = retry(
                    functools.partial(self._do_request_for_tool_execution_sync, http_request),
                    _default_retry_policy,
                )
                response.raise_for_status()
                return response.text

            tools.append(
                BaseTool(
                    name=tool_data.name,
                    description=tool_data.description,
                    parameters=schema,
                    execute=execute_tool_async_impl,
                    execute_sync=execute_tool_sync_impl,
                )
            )

        self._cache[key] = tools
        return tools

    def _prepare_http_request_args(
        self,
        input_data_local: Union[Dict[str, Any], str],
        _tool_id_local: str,
        _project_local: str,
        _environment_local: Optional[str]
    ):
        parsed_input: Dict[str, Any]
        if isinstance(input_data_local, str):
            try:
                parsed_input = json.loads(input_data_local)
            except json.JSONDecodeError as e:
                raise ValueError("Error parsing input string for tool call.") from e
        else:
            parsed_input = input_data_local

        if self._environment_variables:
            parsed_input["environmentVariables"] = self._environment_variables
        
        headers = {
            "gram-key": self._api_key,
            "gram-project": _project_local,
            "user-agent": f"gram-ai/adapter python {VERSION}",
            "content-type": "application/json",
        }

        url = f"{self._server_url}/rpc/instances.invoke/tool"
        params = {"tool_id": _tool_id_local}
        if _environment_local:
            params["environment_slug"] = _environment_local
        
        return url, params, headers, parsed_input
