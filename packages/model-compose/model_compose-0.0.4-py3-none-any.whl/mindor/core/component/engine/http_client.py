from typing import Type, Union, Literal, Optional, Dict, List, Tuple, Set, Annotated, Any
from mindor.dsl.schema.component import HttpClientComponentConfig, HttpClientActionConfig, HttpUrl
from .base import BaseComponent, ComponentType, ComponentEngineMap, ActionConfig
from .context import ComponentContext

from requests.structures import CaseInsensitiveDict
from urllib.parse import urlencode, urljoin
import aiohttp, json

class HttpClientAction:
    def __init__(self, base_url: Union[str, None], config: HttpClientActionConfig):
        self.base_url: Union[HttpUrl, None] = base_url
        self.config: HttpClientActionConfig = config

    async def run(self, context: ComponentContext) -> Dict[str, Any]:
        url     = self._resolve_request_url(context)
        method  = context.render_template(self.config.method)
        params  = context.render_template(self.config.params)
        body    = context.render_template(self.config.body)
        headers = context.render_template(self.config.headers)

        response = await self._request(url, method, params, body, headers)

        if not self.config.output:
            return response or {}

        if response:
            context.register_source("response", response)

        return context.render_template(self.config.output)

    async def _request(self, url: str, method: str, params: Optional[Dict[str, Any]], body: Optional[Dict[str, Any]], headers: Optional[Dict[str, str]]) -> Union[dict, str, bytes]:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method,
                url,
                params=params,
                data=self._serialize_request_body(body, headers) if body is not None else None, 
                headers=headers
            ) as response:
                if response.status >= 400:
                    raise ValueError(f"Request failed with status {response.status}")

                return await self._deserialize_response_body(response)

    def _resolve_request_url(self, context: ComponentContext) -> str:
        if self.base_url and self.config.path:
            return context.render_template(str(self.base_url)) + context.render_template(self.config.path)
        
        return context.render_template(str(self.config.endpoint))
    
    def _serialize_request_body(self, body: Dict[str, Any], headers: Optional[Dict[str, str]]) -> str:
        content_type = CaseInsensitiveDict(headers or {}).get("Content-Type", "").lower()

        if content_type == "application/json":
            return json.dumps(body)

        if content_type == "application/x-www-form-urlencoded":
            return urlencode(body)
        
        return str(body)
    
    async def _deserialize_response_body(self, response: aiohttp.ClientResponse) -> Union[dict, str, bytes]:
        content_type = response.headers.get("Content-Type", "").lower()

        if content_type == "application/json":
            return await response.json()
        
        if content_type.startswith("text/"):
            return await response.text()

        return await response.read()

class HttpClientComponent(BaseComponent):
    def __init__(self, id: str, config: HttpClientComponentConfig, env: Dict[str, str], daemon: bool):
        super().__init__(id, config, env, daemon)

    async def _serve(self) -> None:
        pass

    async def _shutdown(self) -> None:
        pass

    async def _run(self, action: ActionConfig, context: ComponentContext) -> Dict[str, Any]:
        return await HttpClientAction(self.config.base_url, action).run(context)

ComponentEngineMap[ComponentType.HTTP_CLIENT] = HttpClientComponent
