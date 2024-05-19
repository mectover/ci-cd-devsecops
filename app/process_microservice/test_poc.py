# import requests
# import uuid

# # Assuming your FastAPI app is in main.py

# # Replace "your_job_type" with the actual job type you want to test
# job_type = "image_to_text"

# # # Assuming you have set up your database with a known job_id for testing
# # known_job_id = str(uuid.uuid4())

# # # Create a fake image file for testing
# # fake_image_content = b"fake_image_content"
# # files = {"file": ("image.jpg", fake_image_content, "image/jpeg")}

# # Perform a POST request to create a job



# # Extract the created job_id

# # Perform a GET request to retrieve the created job details
# # response_get = requests.post(f"http://127.0.0.1:8002/jobs/{job_type}")

# # Assert the response status code for job retrieva



# # Additional assertions based on your requirements
# # For example, you might want to assert the correctness of the returned data
# # ...


#  # Create a fake image file for testing
# fake_image_content = b"fake_image_content"
# files = {"file": ("image.jpg", fake_image_content, "image/jpeg")}


# response_post = requests.post(f"http://127.0.0.1:8002/jobs/{job_type}",files=files)
# print(response_post.text)

# json_response=response_post.json()

# print(json_response["job_id"])

# job_id=str(json_response["job_id"])


# response_get = requests.get(f"http://127.0.0.1:8002/jobs/{job_type}/{job_id}")

# print(response_get.text)

