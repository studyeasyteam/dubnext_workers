# Use an official Python slim image as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install git
RUN apt-get update && apt-get install -y git
RUN DEBIAN_FRONTEND="noninteractive" TZ="Europe/London" apt-get -y install poppler-utils python3-pip python3-opencv

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file to the container
COPY ./requirements.txt /app/requirements.txt

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . /app/

# Expose port 80 to the outside world
EXPOSE 9000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]
