from pydantic import BaseModel, Field, HttpUrl
from pydantic import model_validator
from typing import Type, Union, Literal, Optional, Dict, List, Tuple, Set, Annotated, Any
from mindor.dsl.schema.action import McpClientActionConfig
from .common import ComponentType, CommonComponentConfig

class McpClientComponentConfig(CommonComponentConfig):
    type: Literal[ComponentType.MCP_CLIENT]
    endpoint: HttpUrl
    actions: Optional[Dict[str, McpClientActionConfig]] = Field(default_factory=dict)
