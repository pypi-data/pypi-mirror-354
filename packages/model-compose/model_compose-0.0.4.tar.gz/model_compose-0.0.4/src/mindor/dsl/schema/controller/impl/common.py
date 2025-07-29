from pydantic import BaseModel, Field
from typing import Type, Union, Literal, Optional, Dict, List, Tuple, Set, Annotated, Any
from .types import ControllerType

class CommonControllerConfig(BaseModel):
    type: ControllerType
    runtime: Literal[ "docker", "native" ] = "native"
    max_concurrent_count: int = 1
    threaded: bool = False
