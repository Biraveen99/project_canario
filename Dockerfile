# Use an official Python runtime as the parent image
FROM python:3.8-slim-buster

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application into the container at /app
COPY . /app/

# Specify the port number the container should expose
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]