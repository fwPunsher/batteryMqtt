# Battery MQTT Client
Local script to fetch Data for ASGOFT ASE 1000 and related variants of solar battery.

Create a docker image using
```
docker build -t battery-mqtt-client .
```

Run using:
```
docker run -d \
  -e MQTT_BROKER="192.168.1.2" \
  -e MQTT_PORT="1883" \
  -e APP_CODE="ASGOFT" \
  -e LOGIN_NAME="test@example.com" \
  -e PASSWORD="YourPassword" \
  --name battery-mqtt-client battery-mqtt-client
```

Alternatively edit the configuration section and run the script directly 

### Configuration Parameters

This application can be configured through the following environment variables. Please note that some of these are mandatory for the application to function correctly:

- **`MQTT_BROKER`** (mandatory): 
  - **Description**: The IP address or hostname of the MQTT broker.
  - **Default**: None (must be provided).

- **`MQTT_PORT`** (optional): 
  - **Description**: The port number on which the MQTT broker is listening.
  - **Default**: `1883`.

- **`MQTT_TOPIC`** (optional): 
  - **Description**: The MQTT topic where messages will be published.
  - **Default**: `battery/reportEquip`.

- **`WS_URI`** (optional): 
  - **Description**: The full URI for establishing the WebSocket connection.
  - **Default**: `ws://baterway.com:9501/equip/info/`.

- **`TOKEN_URL`** (mandatory): 
  - **Description**: The URL to fetch the authorization token required for WebSocket authentication.
  - **Default**: `http://baterway.com/api/user/app/login`.

- **`HEARTBEAT_INTERVAL`** (optional): 
  - **Description**: The interval in seconds between each heartbeat message sent to maintain the WebSocket connection.
  - **Default**: `60` seconds.

- **`RECONNECT_DELAY`** (optional): 
  - **Description**: The delay in seconds before attempting to reconnect after a connection loss.
  - **Default**: `60` seconds.

- **`APP_CODE`** (mandatory): 
  - **Description**: The application code used as part of the authentication process to fetch the token.
  - **Default**: `ASGOFT`.

- **`LOGIN_NAME`** (mandatory): 
  - **Description**: The login name used in conjunction with `PASSWORD` for authentication purposes.
  - **Default**: None (must be provided).

- **`PASSWORD`** (mandatory): 
  - **Description**: The password corresponding to the `LOGIN_NAME` for authentication purposes.
  - **Default**: None (must be provided).


