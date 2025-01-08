# # Use a Python base image
# FROM python:3.9-slim

# # Set the working directory inside the container
# WORKDIR /app

# # Copy the backend files to the container
# COPY backend/ ./backend/
# COPY frontend/ ./frontend/

# # Copy the requirements file to the container
# COPY backend/requirements.txt ./

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Expose the port your application will run on (assuming the backend runs on port 5000)
# EXPOSE 5000

# # Command to run your application (adjust based on your application setup)
# CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "5000"]


# Use a Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the backend files to the container
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Copy the requirements file to the container
COPY backend/requirements.txt ./backend/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Expose the port your application will run on (assuming the backend runs on port 5000)
EXPOSE 5000

# Command to run your application (adjust based on your application setup)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]