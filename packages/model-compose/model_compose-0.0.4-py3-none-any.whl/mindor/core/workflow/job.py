from typing import Type, Union, Literal, Optional, Dict, List, Tuple, Set, Annotated, Callable, Any
from mindor.dsl.schema.workflow import JobConfig
from mindor.dsl.schema.component import ComponentConfig
from mindor.core.component import BaseComponent
from .context import WorkflowContext

class Job:
    def __init__(self, id: str, config: JobConfig, component_provider: Callable[[Union[ComponentConfig, str]], BaseComponent]):
        self.id: str = id
        self.config: JobConfig = config
        self.component_provider: Callable[[Union[ComponentConfig, str]], BaseComponent] = component_provider

    async def run(self, context: WorkflowContext) -> Dict[str, Any]:
        component = self.component_provider(self.config.component)

        if not component.started:
            await component.start()

        input = context.render_template(self.config.input)
        output = await component.run(self.config.action, input)

        context.register_source("output", output)
        output = context.render_template(self.config.output)

        return output
