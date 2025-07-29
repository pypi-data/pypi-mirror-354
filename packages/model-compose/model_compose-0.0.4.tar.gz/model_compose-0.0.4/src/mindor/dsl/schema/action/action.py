from pydantic import BaseModel, Field
from typing import Type, Union, Literal, Optional, Dict, List, Tuple, Set, Annotated, Any
from .impl import *

ActionConfig = Annotated[ 
    Union[ 
        HttpServerActionConfig,
        HttpClientActionConfig,
        McpServerActionConfig,
        McpClientActionConfig
    ],
    Field(discriminator="type")
]
