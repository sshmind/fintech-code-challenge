# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .
COPY consumer.py .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the script
CMD [ "python", "producer.py" ]
