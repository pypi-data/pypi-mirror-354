from pydantic import BaseModel, Field
from typing import Type, Union, Literal, Optional, Dict, List, Tuple, Set, Annotated, Any

class CommonActionConfig(BaseModel):
    output: Optional[Dict[str, Any]] = Field(default_factory=dict)
    default: bool = False
