# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./requirements.txt /app
COPY ./src /app/src

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run api.py when the container launches
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "80"]


# Usage

# Build the image
# docker build -t my-fastapi-app -f deployment/Dockerfile .

# Run the container
# docker run -d --name my-fastapi-app -p 80:80 my-fastapi-app