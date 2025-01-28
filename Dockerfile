# Use an official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements and application files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the application files
COPY . .


EXPOSE 5000

# Set the environment variables
ENV FLASK_APP=main.py
ENV FLASK_ENV=development

# Command to run the console application
CMD ["python", "main.py"]