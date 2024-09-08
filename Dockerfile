# Use the official Python 3.10.1 image from the Docker Hub
FROM python:3.10.1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/requirements.txt

# Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Expose port 8080 for the application
EXPOSE 8080

# Command to run the FastAPI application using Uvicorn
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]