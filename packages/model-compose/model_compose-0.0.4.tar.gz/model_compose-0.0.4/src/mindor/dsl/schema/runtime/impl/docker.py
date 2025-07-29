from pydantic import BaseModel, Field, HttpUrl
from pydantic import model_validator
from typing import Type, Union, Literal, Optional, Dict, List, Tuple, Set, Annotated, Any
from .common import RuntimeType, CommonRumtimeConfig

class DockerRuntimeConfig(CommonRumtimeConfig):
    type: Literal[RuntimeType.DOCKER]
