# Grabba Python SDK

Grabba Python SDK provides a simple and intuitive interface for scheduling web data extraction jobs, retrieving job results, and managing your extraction workflows. All SDK types are now implemented as Pydantic BaseModels for full JSON compatibility and built-in validation.

## Installation

Install the SDK using pip:

```bash
pip install grabba
```

## Basic Setup

### Import the Client and Required Types

```python
from grabba import Grabba, Job, JobNavigationType, JobSchedulePolicy, JobTaskType
```

> **Note:** All types such as `Job`, `JobTask`, etc., are now Pydantic BaseModels. This means that they support methods like `.model_dump()` and `.json()` for serialization, and Enum fields are automatically converted to their literal values during JSON encoding.

### Initialize a Client Instance

```python
grabba = Grabba(api_key="your-api-key", region="US")  # Optional: Defaults to US
```

---

## Methods

### extract

`extract(job: Job) -> Dict`

Schedules a new web data extraction job.

**Parameters:**

- `job`: A `Job` object containing the extraction configuration.

**Returns:**

- A dictionary containing the response `status`, `message`, and `job_result`.

**Example:**

```python
from grabba import Job, JobSchedulePolicy, JobNavigationType, JobTaskType

job = Job(
    url="https://docs.grabba.dev/home",
    schedule={
        "policy": JobSchedulePolicy.IMMEDIATELY  # Enum values will be serialized as literals
    },
    navigation={
        "type": JobNavigationType.NONE
    },
    tasks=[{
        "type": JobTaskType.WEB_PAGE_AS_MARKDOWN,
        "options": {"only_main_content": True}
    }],
)

# Note: Since Job is a Pydantic model, you may also print its JSON representation:
print(job.json())

response = grabba.extract(job)
print(f"Job completed with status: {response['status']}")
```

---

### schedule\_job

`schedule_job(job_id: str) -> Dict`

Schedules an existing job for execution.

**Parameters:**

- `job_id`: The ID of the job to schedule.

**Returns:**

- A dictionary containing the response `status`, `message`, and `job_result`.

**Example:**

```python
response = grabba.schedule_job("12345")
print(f"Job completed with status: {response['status']}")
```

---

### get\_jobs

`get_jobs() -> GetJobsResponse`

Retrieves a list of all jobs associated with the API key.

**Returns:**

- A list of `Job` objects.

**Example:**

```python
jobs = grabba.get_jobs()
for job in jobs:
    print(job.model_dump())
```

---

### get\_job

`get_job(job_id: str) -> GetJobResponse`

Retrieves details of a specific job by its ID.

**Parameters:**

- `job_id`: The ID of the job to retrieve.

**Returns:**

- A `JobDetail` object containing job details.

**Example:**

```python
job = grabba.get_job("12345")
print(job.model_dump())
```

---

### get\_job\_result

`get_job_result(job_result_id: str) -> JobResult`

Retrieves the results of a specific job by its result ID.

**Parameters:**

- `job_result_id`: The ID of the job result to retrieve.

**Returns:**

- A `JobResult` object.

**Example:**

```python
result = grabba.get_job_result("67890")
print(result.model_dump())
```

---

### delete\_job (New in 0.0.4)

`delete_job(job_id: str) -> Dict`

Deletes a specific job by its ID.

**Parameters:**

- `job_id`: The ID of the job to delete.

**Returns:**

- A dictionary containing the response `status` and `message`.

**Example:**

```python
response = grabba.delete_job("12345")
print(f"Job deletion status: {response['status']}")
```

---

## Error Handling

The SDK throws errors for:

- Invalid API keys
- Failed API requests
- Missing or invalid parameters

**Example:**

```python
try:
    response = grabba.extract(job)
    if response["status"] == "success":
        print("Results data:", response["job_result"]["data"])
    else:
        print("Error message:", response["message"])
except Exception as err:
    print("Error:", err)
```

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on [GitHub](https://github.com/grabba-dev/grabba-sdk).

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### Additional Notes

- **Pydantic Serialization:**\
  All SDK models are now Pydantic BaseModels, so you can use `.json()` or `.model_dump()` to serialize your models with Enums automatically converted to their literal values.
- **Enum Configuration:**\
  In our BaseModels, we use `json_encoders` in the `Config` class to ensure Enum fields (such as `JobSchedulePolicy` and `JobTaskType`) are output as their literal values.
- **Type Safety:**\
  With Pydantic, all input data is validated against the model definitions, which helps catch errors early.

Feel free to adjust these examples as needed, and let us know if you have any questions or further changes!

---

## Change Log

### Version 0.0.4 (Latest)


- **Improved Job Task Handling:** Enhanced task validation and error handling for better reliability.
- **New API Method - ****\`\`****:** Now you can delete jobs using their `job_id`.
- **Performance Optimizations:** Improved response times by optimizing API requests and serialization.
- **Bug Fixes:** Fixed minor serialization issues with nested Pydantic models.
- **Added `delete_job(job_id: str) -> BaseResponse`**
- **Added `delete_job_result(job_result_id: str) -> BaseResponse`**

### Version 0.0.3

- **Pydantic Integration:** All SDK types are now Pydantic BaseModels, enabling JSON serialization and validation.
- **Enum Field Optimization:** Enums are automatically serialized to their literal values.
- **Better Error Handling:** More descriptive error messages and improved exception handling.
