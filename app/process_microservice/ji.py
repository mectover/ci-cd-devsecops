from PIL import Image
import zipfile
import os
def resize(file, width, height):
    try:
        image = Image.open(file)
        new_image = image.resize((width, height))
        new_image.save('myimage_resized.png')
        return "Image resized and saved successfully"
    except Exception as e:
        return f"Error: {str(e)}"
def to_black_and_white(file):
    try:
        image = Image.open(file)
        bw_image = image.convert('L') 
        bw_image.save('myimage_bw.jpg')
        return "Image converted to black and white and saved successfully"
    except Exception as e:
        return f"Error: {str(e)}"

def compress_to_zip(file):
    try:
        zip_filename = 'file.zip'
        with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        
                 zip_file.write(file, "image_unzip.png")

        return f"Images compressed to {zip_filename} successfully"
    except Exception as e:
        return f"Error: {str(e)}"
    
    
to_black_and_white('image.png')
resize('image.png', 100, 100)
compress_to_zip('image.png')
