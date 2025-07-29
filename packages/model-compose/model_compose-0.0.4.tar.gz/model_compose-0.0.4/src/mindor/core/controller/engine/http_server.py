from pydantic import BaseModel
from typing import Type, Union, Literal, Optional, Dict, List, Tuple, Set, Annotated, Any
from typing_extensions import Self

from mindor.dsl.schema.controller import HttpServerControllerConfig
from mindor.dsl.schema.component import ComponentConfig
from mindor.dsl.schema.workflow import WorkflowConfig
from .base import BaseController, ControllerType, ControllerEngineMap, TaskState

from fastapi import FastAPI, APIRouter, Body, HTTPException
import uvicorn

class WorkflowTaskRequestBody(BaseModel):
    workflow_id: Optional[str] = None
    input: Optional[Dict[str, Any]] = None
    wait_for_completion: bool = True

class TaskResult(BaseModel):
    task_id: str
    status: Literal[ "pending", "processing", "completed", "failed" ]
    output: Optional[Any] = None
    error: Optional[Any] = None

    @classmethod
    def from_instance(cls, instance: TaskState) -> Self:
        return cls(
            task_id=instance.task_id,
            status=instance.status,
            output=instance.output,
            error=instance.error
        )

class HttpServerController(BaseController):
    def __init__(self, config: HttpServerControllerConfig, components: Dict[str, ComponentConfig], workflows: Dict[str, WorkflowConfig], env: Dict[str, str], daemon: bool):
        super().__init__(config, components, workflows, env, daemon)
        
        self.server: Optional[uvicorn.Server] = None
        self.app: FastAPI = FastAPI()
        self.router: APIRouter = APIRouter()
        
        self._configure_routes()
        self.app.include_router(self.router, prefix=self.config.base_path)

    def _configure_routes(self):
        @self.router.post("/workflows", response_model=TaskResult, response_model_exclude_none=True)
        async def run_workflow(
            body: WorkflowTaskRequestBody = Body(...)
        ):
            state = await self.run_workflow(body.workflow_id, body.input, body.wait_for_completion)

            return TaskResult.from_instance(state)

        @self.router.get("/tasks/{task_id}", response_model=TaskResult, response_model_exclude_none=True)
        async def get_task_state(
            task_id: str
        ):
            state = self.get_task_state(task_id)

            if not state:
                raise HTTPException(status_code=404, detail="Task not found")
            
            return TaskResult.from_instance(state)

    async def _serve(self) -> None:
        self.server = uvicorn.Server(uvicorn.Config(
            self.app, 
            host=self.config.host, 
            port=self.config.port, 
            log_level="info"
        ))
        await self.server.serve()
 
    async def _shutdown(self) -> None:
        self.server.should_exit = True

ControllerEngineMap[ControllerType.HTTP_SERVER] = HttpServerController
