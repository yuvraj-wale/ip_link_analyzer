# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variables if needed
# ENV MY_VARIABLE=my_value

# Run the application when the container launches
CMD ["python", "main.py"]
