# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .
COPY price_data.csv .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Copy the script and other necessary files to the working directory
COPY main.py .
COPY csv_handler.py .
COPY redis_handler.py .

# Set the command to run the script
CMD [ "python", "main.py" ]
