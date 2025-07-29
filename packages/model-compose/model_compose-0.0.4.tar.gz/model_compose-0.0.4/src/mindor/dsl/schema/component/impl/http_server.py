from pydantic import BaseModel, Field, HttpUrl
from pydantic import model_validator
from typing import Type, Union, Literal, Optional, Dict, List, Tuple, Set, Annotated, Any
from mindor.dsl.schema.action import HttpServerActionConfig
from .common import ComponentType, CommonComponentConfig

class HttpServerComponentConfig(CommonComponentConfig):
    type: Literal[ComponentType.HTTP_SERVER]
    port: Optional[int] = Field(None, ge=1, le=65535)
    base_path: Optional[str]
    actions: Optional[Dict[str, HttpServerActionConfig]] = Field(default_factory=dict)
