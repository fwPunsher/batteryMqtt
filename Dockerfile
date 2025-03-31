# Use an official Python runtime as a parent image
FROM python:3-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Set environment variables for configuration
ENV MQTT_PORT=1883
ENV MQTT_TOPIC=battery/reportEquip
ENV HEARTBEAT_INTERVAL=60
ENV RECONNECT_DELAY=60
ENV APP_CODE=ASGOFT

# Copy the current directory contents into the container at /usr/src/app
COPY batteryMqtt.py .

# Set Python to run unbuffered
ENV PYTHONUNBUFFERED=1

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the script when the container launches
CMD ["python", "./batteryMqtt.py"]
