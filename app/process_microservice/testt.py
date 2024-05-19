import base64
import requests
from io import BytesIO



def decode_base64_to_image(encoded_image):
    decoded_image = base64.b64decode(encoded_image)
    image = Image.open(BytesIO(decoded_image))
    return image


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())
        return BytesIO(encoded_image)

encoded_image=encode_image_to_base64("./ff.png")

files = {'file': encoded_image}

response1 = requests.post('http://localhost:8003/jobs/image_to_text', files=files)


# data = {'width': '20', 'height': '20'}
# resizeee = {'file': ('./ff.png', open('./ff.png', 'rb'))}

# response2 = requests.post('http://localhost:8002/process/resize', files=resizeee, data=data)

print(response1.text)
# print(response2.text)