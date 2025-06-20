# Use a lightweight Python image
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port your app runs on
# Railway injects the PORT environment variable
ENV PORT 8000
EXPOSE $PORT

# Command to run your FastAPI application
# Assuming your main app is at agno/cookbook/apps/fastapi/basic.py
CMD ["uvicorn", "agno.cookbook.apps.fastapi.basic:app", "--host", "0.0.0.0", "--port", "$PORT"]
