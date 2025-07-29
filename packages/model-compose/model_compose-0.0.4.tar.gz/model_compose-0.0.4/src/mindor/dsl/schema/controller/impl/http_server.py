from pydantic import BaseModel, Field, HttpUrl
from pydantic import model_validator
from typing import Type, Union, Literal, Optional, Dict, List, Tuple, Set, Annotated, Any
from .common import ControllerType, CommonControllerConfig

class HttpServerControllerConfig(CommonControllerConfig):
    type: Literal[ControllerType.HTTP_SERVER]
    host: Optional[str] = "0.0.0.0"
    port: Optional[int] = 8080
    base_path: Optional[str] = None
