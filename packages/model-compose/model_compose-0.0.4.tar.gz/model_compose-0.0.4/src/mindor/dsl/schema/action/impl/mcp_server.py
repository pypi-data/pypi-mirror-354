from pydantic import BaseModel, Field, HttpUrl
from pydantic import model_validator
from typing import Type, Union, Literal, Optional, Dict, List, Tuple, Set, Annotated, Any
from .common import CommonActionConfig

class McpServerActionConfig(CommonActionConfig):
    def __init__(self):
        super.__init__(self)
