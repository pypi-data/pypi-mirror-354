from pydantic import BaseModel, Field, HttpUrl
from typing import Type, Union, Literal, Optional, Dict, List, Tuple, Set, Annotated, Any
from .types import ComponentType

class CommonComponentConfig(BaseModel):
    type: ComponentType
    runtime: Literal[ "docker", "native" ] = "native"
    max_concurrent_count: int = 1
    default: bool = False
