from pydantic import BaseModel, Field, HttpUrl
from pydantic import model_validator
from typing import Type, Union, Literal, Optional, Dict, List, Tuple, Set, Annotated, Any
from .common import CommonActionConfig

class HttpClientActionCompletionConfig(CommonActionConfig):
    endpoint: Optional[HttpUrl] = None
    path: Optional[str] = None
    method: Literal[ "GET", "POST", "PUT", "DELETE", "PATCH" ] = "GET"
    headers: Optional[Dict[str, str]] = Field(default_factory=dict)
    body: Optional[Dict[str, Any]] = Field(default_factory=dict)
    params: Optional[Dict[str, str]] = Field(default_factory=dict)
    interval: Optional[str] = None
    timeout: Optional[str] = None

    @model_validator(mode="before")
    def validate_endpoint_or_path(cls, values):
        if bool(values.get("endpoint")) == bool(values.get("path")):
            raise ValueError("Either 'endpoint' or 'path' must be set, but not both.")
        return values

class HttpClientActionConfig(CommonActionConfig):
    endpoint: Optional[HttpUrl] = None
    path: Optional[str] = None
    method: Literal[ "GET", "POST", "PUT", "DELETE", "PATCH" ] = "POST"
    headers: Optional[Dict[str, str]] = Field(default_factory=dict)
    body: Optional[Dict[str, Any]] = Field(default_factory=dict)
    params: Optional[Dict[str, str]] = Field(default_factory=dict)
    deferred: bool = False
    completion: Optional[HttpClientActionCompletionConfig] = None

    @model_validator(mode="before")
    def validate_endpoint_or_path(cls, values):
        if bool(values.get("endpoint")) == bool(values.get("path")):
            raise ValueError("Either 'endpoint' or 'path' must be set, but not both.")
        return values

    @model_validator(mode="after")
    def validate_completion_if_deferred(self):
        if self.deferred and self.completion is None:
            raise ValueError("If 'deferred' is true, 'completion' must be provided.")
        return self
