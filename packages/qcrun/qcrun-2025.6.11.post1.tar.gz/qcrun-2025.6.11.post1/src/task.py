from typing import Literal
from pydantic import BaseModel, Field, model_validator
from abc import ABC, abstractmethod
from datetime import datetime
import os

workspace = os.environ.get("SC_WORKSPACE_PATH", "/public/home/chengz/workspace")

TaskState = Literal[
    "queuing",
    "staging",
    "canceled",
    "running",
    "finished",
    "failed",
    "killed",
    "holding",
]
structure_file_suffix = Literal["smi", "sdf", "mol", "xyz", "chk", "fchk"]


class Task(BaseModel, ABC):
    id: str = ""
    owner: str = ""
    title: str = ""
    name: str = ""
    app_id: str = ""
    status: TaskState = "queuing"
    exec_time: float | None = None
    end_time: float | None = None
    input_file: list[str] = Field(default_factory=list)
    output_file: list[str] = Field(default_factory=list)

    @abstractmethod
    async def pre_check(self) -> bool:
        # 检查任务是否有效,文件依赖是否存在等
        pass


    ## 2. run on task-instance input/out
    @model_validator(mode="before")
    def polyfill_with_mongo_raw_data(cls, data):
        data["id"] = (
            str(data.get("_id", "")) if data.get("_id", "") else data.get("id", "")
        )
        return data

    def model_dump_without_id(self):
        # 使用字典推导式去除 _id 字段
        out = self.model_dump()
        del out["id"]
        return out
