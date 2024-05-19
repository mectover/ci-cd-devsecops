import base64
import requests
from models import *
from io import BytesIO
from PIL import Image
import pytesseract


def decode_base64_to_image(encoded_image):
    decoded_image = base64.b64decode(encoded_image)
    image = Image.open(BytesIO(decoded_image))
    return image


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())
        return BytesIO(encoded_image)


async def image_to_textt(file,job_id):
        print("Starting OCR!!")
        encoded_image = base64.b64decode(base64.b64encode(file))
        im = Image.open(BytesIO(encoded_image))
        # Save the PIL Image object to a file
        with open('image_to_OCR.png', 'wb') as f:
            im.save(f)
        # Perform OCR on the image
        text = pytesseract.image_to_string(im)

        # Print the OCR result
        print("OCR Result:")
        print(text)

        job = await  Jobs.find_one(Jobs.job_id == str(job_id))

        job.status="Completed"
        job.result=text
        await job.set(dict(job))
        return text
async def job_to_black_and_white(image,job_id):
    try:
        job = await  Jobs.find_one(Jobs.job_id == str(job_id))
        encoded_image = base64.b64decode( base64.b64encode(image))
        im = Image.open(BytesIO(encoded_image))
        # Save the PIL Image object to a file
        with open('image_to_resize.png', 'wb') as f:
            im.save(f)

        with Image.open("image_to_resize.png") as img:
           bw_image = img.convert('L') 
           output_buffer = BytesIO()
           bw_image.save(output_buffer, format="PNG")
           job.image_file= output_buffer.getvalue()
           job.status="Done"
           await job.set(dict(job))
           bw_image.save('myimage_bw.jpg')
        print(f"Image converted to black and white and saved successfully")
    except Exception as e:
        return f"Error converting image to black and white: {str(e)}"


async def job_compress(image,job_id,chosen_quality,chosen_format):
    try:
        job = await  Jobs.find_one(Jobs.job_id == str(job_id))
        encoded_image = base64.b64decode( base64.b64encode(image))
        im = Image.open(BytesIO(encoded_image))
        # Save the PIL Image object to a file
        with open('image_to_compress.png', 'wb') as f:
            im.save(f)

        with Image.open("image_to_compress.png") as img:
           
           output=f"image_compressed.{chosen_format}"
           img.save(output,format=chosen_format,quality=chosen_quality)
           output.show()
           output_buffer = BytesIO()
           img.save(output_buffer, format=chosen_format,quality=chosen_quality)
           job.image_file= output_buffer.getvalue()
           job.status="Done"
           await job.set(dict(job))
          
        print(f"Image compressed and saved successfully")
    except Exception as e:
        return f"Error compressing image {str(e)}"

async def job_resize_image(image,job_id,width,height):
    try:
    # Open the image file
        job = await  Jobs.find_one(Jobs.job_id == str(job_id))

        encoded_image = base64.b64decode( base64.b64encode(image))
        im = Image.open(BytesIO(encoded_image))
        # Save the PIL Image object to a file
        with open('image_to_resize.png', 'wb') as f:
            im.save(f)

        with Image.open("image_to_resize.png") as img:
            # Resize the image
            resized_img = img.resize((width, height))
            # Save the resized image to bytes
            output_buffer = BytesIO()
            resized_img.save(output_buffer, format="PNG")
            job.image_file= output_buffer.getvalue()
            job.status="Done"
            await job.set(dict(job))

            # Save the resized image
            resized_img.save("image_resized.png")

        print(f"Image resized and saved in this directory ")

    except Exception as e:
        print(f"Error resizing image: {e}")
