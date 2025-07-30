import requests;
from typing import Dict, List;
from ..types.enums import (
    PuppetRegion, 
);
from ..types import (
    WebAgentConfig, 
    Job, JobSchedule, JobNavigation,
    JobNavigationType, JobSchedulePolicy, 
    BaseResponse, JobExecutionResponse, JobExecutionStatus,
    GetJobResponse, GetJobsResponse, GetJobResultResponse
);
from .utils import dict_to_camel_case, dict_to_snake_case

# Grabba SDK Class
class Grabba:
    def __init__(self, api_key: str, region: PuppetRegion = PuppetRegion.US.value):
        if not api_key:
            raise ValueError("API key is required")
        self.api_key = api_key
        self.api_url = "https://api.grabba.dev/v1"
        self.default_puppet_config = WebAgentConfig(region=region)
        self.default_job_navigation = JobNavigation(type=JobNavigationType.NONE.value)
        self.default_job_schedule = JobSchedule(policy=JobSchedulePolicy.IMMEDIATELY.value)

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key,
        }

    def extract(self, job: Job) -> JobExecutionResponse:
        job = Job.model_validate(job)
        if not job.puppet_config:
            job.puppet_config = self.default_puppet_config
        if not job.navigation:
            job.navigation = self.default_job_navigation
        if not job.schedule:
            job.schedule = self.default_job_schedule
        job_data = job.model_dump(by_alias=True, exclude_none=True)
        # convert job object keys to camelCase
        jobToCamelCase = dict_to_camel_case(job_data)
        # Send request
        response = requests.post(
            f"{self.api_url}/extract",
            headers=self._get_headers(),
            json=jobToCamelCase,
        )
        # Return response for only 'BadRequest' and 'response.OK'
        if response.ok:
            execution_response = response.json()
            return JobExecutionResponse(
                status=execution_response['status'], 
                message=execution_response['message'], 
                job_result=dict_to_snake_case(
                    execution_response['jobResult'],
                    skip_regex=r'^\d+\s-\s.+$' # Skips task output key
                )
            )
        if response.status_code == 400:
            # Catch error message
            execution_response = response.json()
            job_errors = { "errors": execution_response }
            return JobExecutionResponse(
                status=JobExecutionStatus.ERROR,
                message="BadRequestError", 
                job_result=job_errors
            )
        return response.raise_for_status()
    
    def schedule_job(self, job_id: str) -> JobExecutionResponse:
        response = requests.post(
            f"{self.api_url}/schedule-job/{job_id}",
            headers=self._get_headers(),
        )
        # Return response for only 'BadRequest' and 'response.OK'
        if response.ok:
            execution_response = response.json()
            return JobExecutionResponse(
                status=execution_response['status'], 
                message=execution_response['message'], 
                job_result=dict_to_snake_case(
                    execution_response['jobResult'],
                    skip_regex=r'^\d+\s-\s.+$' # Skips task output key
                )
            )
        if response.status_code == 400:
            # Catch error message
            execution_response = response.json()
            job_errors = { "errors": execution_response }
            return JobExecutionResponse(
                status=JobExecutionStatus.ERROR,
                message="BadRequestError", 
                job_result=job_errors
            )
        return response.raise_for_status()

    def get_jobs(self) -> GetJobsResponse:
        response = requests.get(
            f"{self.api_url}/jobs",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return GetJobsResponse(**response.json())

    def get_job(self, job_id: str) -> GetJobResponse:
        response = requests.get(
            f"{self.api_url}/jobs/{job_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return GetJobResponse(**response.json())
    
    def delete_job(self, job_id: str) -> BaseResponse:
        response = requests.delete(
            f"{self.api_url}/jobs/{job_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return BaseResponse(**response.json())

    def get_job_result(self, job_result_id: str) -> GetJobResultResponse:
        response = requests.get(
            f"{self.api_url}/job-result/{job_result_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return GetJobResultResponse(**response.json())
    
    def delete_job_result(self, job_result_id: str) -> BaseResponse:
        response = requests.delete(
            f"{self.api_url}/job-result/{job_result_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return BaseResponse(**response.json())

    def get_available_regions(self) -> List[Dict[str, PuppetRegion]]:
        return [{k: v.value} for k, v in PuppetRegion.__members__.items()]
    
