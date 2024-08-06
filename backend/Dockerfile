# Use the Python 3.12 slim base image
FROM python:3.12-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose port 8000 for the application
EXPOSE 8000

# Run the entrypoint.sh script when the container starts
CMD ["sh", "entrypoint.sh"]