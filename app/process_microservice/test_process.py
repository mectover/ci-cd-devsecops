from process_image_service import app  # Assuming your FastAPI app is in main.py
import requests
import pytest   
import uuid 
import base64
import requests
from io import BytesIO



def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())
        return BytesIO(encoded_image)
    


encoded_image=encode_image_to_base64("./text.png")
files = {'file': encoded_image}



def test_OCR_job():
    encoded_image=encode_image_to_base64("./text.png")
    files = {'file': encoded_image}
    print("test_ocr")
    params={'job_type':'job_OCR'}
    response =  requests.post("http://127.0.0.1:8003/jobs/", files=files,params=params)
    print("response ==== ",response.text)
    # Assert the response status code
    assert response.status_code == 200
    # Assert the response contains the expected job_id
    assert "job_id" in response.json()
    return response.json()["job_id"]





def test_bw_job():
    encoded_image=encode_image_to_base64("./text.png")
    files = {'file': encoded_image}
    print("test_bw")
    params={'job_type':'job_BW',}
    response =  requests.post("http://127.0.0.1:8003/jobs/", files=files,params=params)
    print("response ==== ",response.text)
    # Assert the response status code
    assert response.status_code == 200
    # Assert the response contains the expected job_id
    assert "job_id" in response.json()
    return response.json()["job_id"]

def test_resize_job():
    encoded_image=encode_image_to_base64("./text.png")
    files = {'file': encoded_image}
    print("test_resize")
    params={'job_type':'job_resize', 'height':50,'width':20}
    response =  requests.post("http://127.0.0.1:8003/jobs/", files=files,params=params)
    print("response ==== ",response.text)
    # Assert the response status code
    assert response.status_code == 200
    # Assert the response contains the expected job_id
    assert "job_id" in response.json()
    return response.json()["job_id"]


def test_compress_job():
    encoded_image=encode_image_to_base64("./ff.png")
    files = {'file': encoded_image}
    print("test_compress")
    params={'job_type':'job_compress','formatt':'PNG','qualityy':50,}
    response =  requests.post("http://127.0.0.1:8003/jobs/", files=files,params=params)
    print("response ==== ",response.text)
    # Assert the response status code
    assert response.status_code == 200
    # Assert the response contains the expected job_id
    assert "job_id" in response.json()
    return response.json()["job_id"]




def test_get_job():
    job_id=test_compress_job()
    response =  requests.get(f"http://127.0.0.1:8003/jobs/{job_id}")
    assert response.status_code == 200

def test_delete_job():
    job_id=test_OCR_job()
    response =  requests.delete(f"http://127.0.0.1:8003/jobs/{job_id}")
    assert response.status_code == 200



def test_get_all_jobs():
    response =  requests.get(f"http://127.0.0.1:8003/jobs")
    assert response.status_code == 200
