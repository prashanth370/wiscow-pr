# Use Python as the base image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy the application code
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
