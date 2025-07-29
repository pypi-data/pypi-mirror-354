from pydantic import BaseModel, Field, HttpUrl
from pydantic import model_validator
from typing import Type, Union, Literal, Optional, Dict, List, Tuple, Set, Annotated, Any
from .common import CommonActionConfig

class HttpServerActionConfig(CommonActionConfig):
    path: Optional[str] = None
    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"] = "POST"
