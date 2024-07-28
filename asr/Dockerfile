FROM python:3.9

WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY asr_api.py /app

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the FastAPI server when the container launches
CMD ["uvicorn", "asr_api:app", "--host", "0.0.0.0", "--port", "80"]