from typing import Type, Union, Literal, Optional, Dict, List, Tuple, Set, Annotated, Any
from mindor.core.utils.template import TemplateRenderer

class WorkflowContext:
    def __init__(self, input: Dict[str, Any], env: Dict[str, str]):
        self.input: Dict[str, Any] = input
        self.env: Dict[str, str] = env
        self.sources: Dict[str, Any] = { "jobs": {} }
        self.renderer = TemplateRenderer(self._resolve_source)

    def complete_job(self, job_id: str, output: Any) -> None:
        self.sources["jobs"][job_id] = { "output": output }

    def register_source(self, key: str, source: Any) -> None:
        self.sources[key] = source

    def render_template(self, data: Dict[str, Any]) -> Any:
        return self.renderer.render(data)

    def _resolve_source(self, key: str) -> Any:
        if key in self.sources:
            return self.sources[key]
        if key == "input":
            return self.input
        if key == "env":
            return self.env
        raise KeyError(f"Unknown source: {key}")
