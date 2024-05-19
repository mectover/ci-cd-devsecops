FROM python:3.10.8
# Install Tesseract OCR and any additional dependencies
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev  && rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir  --trusted-host pypi.python.org -r requirements.txt
RUN pip install --trusted-host pypi.python.org  python-multipart

# Make port 80 available to the world outside this container
#EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "process_image_service.py"]
