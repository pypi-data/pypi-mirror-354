from typing import List, Dict, Union, Any, Optional
from pydantic import BaseModel
from .job_types import Job, JobDetail, JobResult
from .enums import (
    JobExecutionStatus, 
)

class BaseResponse(BaseModel):
    message: str

class PaginationResponse(BaseModel):
    page: int
    limit: int 
    totalCount: int

class JobExecutionResponse(BaseResponse):
    status: JobExecutionStatus
    job_result: Union[JobResult, Dict[str, Any]]

    class Config:
        json_encoders = {
            JobExecutionStatus: lambda v: v.value
        }

class GetJobResponse(BaseResponse):
    job: JobDetail

class GetJobsResponse(BaseResponse):
    jobs: List[Job]
    pagination: Optional[PaginationResponse] = None

class GetJobResultResponse(BaseResponse):
    job_result: JobResult
