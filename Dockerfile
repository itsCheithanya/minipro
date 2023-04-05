# Use a Python base image
FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the required packages
RUN pip install -r requirements.txt

# Copy the source code
COPY . .

# Expose the port that the model listens on
EXPOSE $PORT

# Start the model
CMD ["python", "app.py"]
