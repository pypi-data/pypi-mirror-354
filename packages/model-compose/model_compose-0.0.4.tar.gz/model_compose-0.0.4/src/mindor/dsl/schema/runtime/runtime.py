from pydantic import BaseModel, Field, HttpUrl
from typing import Type, Union, Literal, Optional, Dict, List, Tuple, Set, Annotated, Any
from .impl import *

RuntimeConfig = Annotated[ 
    Union[ 
        DockerRuntimeConfig 
    ],
    Field(discriminator="type")
]
