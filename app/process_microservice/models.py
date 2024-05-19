from fastapi import Path
from pydantic import BaseModel, Field
from typing import List
from beanie import Document




class Job(BaseModel):
    job_id: str
    job_type: str
    image_file: bytes
    status: str
    result: str
        
class Jobs(Document,Job):
    pass
