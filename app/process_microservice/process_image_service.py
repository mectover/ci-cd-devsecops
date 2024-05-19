#!/usr/bin/env python3

from PIL import Image
import pytesseract
from utils import job_compress,job_to_black_and_white,job_resize_image,image_to_textt,encode_image_to_base64,decode_base64_to_image
import uvicorn
import base64
from typing import List

from io import BytesIO
import uuid  # Add this import
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, BackgroundTasks, Path , Body , Query
from models import Jobs
from pydantic_settings import BaseSettings
import pymongo
from starlette.responses import Response
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware


from contextlib import asynccontextmanager
from pydantic_settings import BaseSettings
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
import pymongo
from beanie import init_beanie
import docs
from beanie import init_beanie
import motor
import motor

# class Settings(BaseSettings):
#     mongo_host: str = "172.17.0.2"
#     mongo_port: str = "27017"
#     database_name: str = "processimage"
    
class Settings(BaseSettings):
    mongo_host: str = "172.17.0.2"
    mongo_port: str = "27017"
    mongo_user: str = ""
    mongo_password: str = ""
    database_name: str = "processimage"
    auth_database_name: str = "processimage"


settings = Settings()




@asynccontextmanager
async def startup_event(application: FastAPI):
    conn = f"mongodb://"
    print(settings.mongo_user ," aaaa" , settings.mongo_password , settings.mongo_host)
    if settings.mongo_user:
        conn += f"{settings.mongo_user}:{settings.mongo_password}@"
    conn += f"{settings.mongo_host}:{settings.mongo_port}"
    conn += f"/{settings.database_name}?authSource={settings.auth_database_name}"
    client = motor.motor_asyncio.AsyncIOMotorClient(conn)
    await init_beanie(
        database=client[settings.database_name], document_models=[Jobs]
    )
    yield


# settings = Settings()

#PASSWORD="@imt_atlantique_trigger_gitlabsecurity!4"






def decode_and_save_image(file_contents, filename):
    decoded_image = base64.b64decode(file_contents)
    image = Image.open(BytesIO(decoded_image))
    image.save(filename)





    

database= None

app = FastAPI(title="Process Image Service",lifespan=startup_event)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the specific origins you want to allow (e.g., ["http://localhost", "https://yourfrontend.com"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/jobs/")
async def create_job(background_tasks: BackgroundTasks, file: UploadFile = File(...), job_type: str = Query(...), height: int = Query(None, description="New height of the image"), width: int = Query(None, description="New width of the image"), formatt: str = Query(None, description="New format of the image"), qualityy: int = Query(None, description="New quality of the image")):
    global database
    image_file = await file.read()
    job_id = str(uuid.uuid4())
    new_job = Jobs(job_id=job_id, job_type=job_type, image_file=image_file, status="ongoing", result="")
    print(job_type)
    await new_job.insert()
    print("width and height",width,height)
    if job_type == "job_OCR":
        background_tasks.add_task(image_to_textt, image_file, job_id)
    elif job_type == "job_resize":
        background_tasks.add_task(job_resize_image, image_file, job_id, height, width)
    elif job_type =="job_BW" :
        background_tasks.add_task(job_to_black_and_white, image_file, job_id)
    elif job_type =="job_compress" :
        background_tasks.add_task(job_compress, image_file, job_id,qualityy,formatt)

    return {"job_id": new_job.job_id, "job_type": job_type, "status": "ongoing"}


    

@app.get("/jobs/",  status_code=200,
    summary="Get a list of Jobs")
async def get_all_jobs():
    try:
        jobs = await Jobs.find().to_list()
        jobs_list=[]
        for job in jobs:

            job={"job_id": job.job_id,
                "job_type": job.job_type,
                "result":job.result,
                "status":job.status
            }
            jobs_list.append(job)
        return jobs_list
    except Exception as e:
        print("Exception:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/jobs/{job_id}")
async def get_job(job_id: str = Path(..., description="Unique identifier for the job")):
    try:
     


        job = await  Jobs.find_one(Jobs.job_id == str(job_id))

        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")
        # this line is important because we ca,t send binary data as a response otherwise we get a unicode error
        base64_image_data = base64.b64encode(job.image_file).decode() #base64.b64encode(job.image_file).decode
        return {
            "job_id": job.job_id,
            "job_type": job.job_type,
            "image_file": base64_image_data,
            "result":job.result,
            "status":job.status
           
        }
    except Exception as e:
       
        print("excepppt==",str(e))
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to retrieve job details by job_id for image_to_text
@app.delete("/jobs/{job_id}")
async def delete_job(job_id: str = Path(..., description="Unique identifier for the job")):
    try:
        # Retrieve job details from the database based on the provided job_id


        job = await  Jobs.find_one(Jobs.job_id == str(job_id))
        print(job)

        # Check if the job with the given job_id exists
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")

        await job.delete()

        return {
            "message": "Job Deleted"
            # Add more details as needed
        }
    except Exception as e:
        # Handle database errors or other exceptions
        raise HTTPException(status_code=500, detail=str(e))




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003, log_level="info")





