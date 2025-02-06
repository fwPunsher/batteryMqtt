import os
import asyncio
import websockets
import json
import requests
from paho.mqtt import client as mqtt_client

# Function to fetch environment variables and raise error if not set
def get_env_variable(var_name):
    value = os.getenv(var_name)
    if not value:
        raise EnvironmentError(f"Environment variable {var_name} is required and not set.")
    return value

# Configuration
broker = get_env_variable('MQTT_BROKER')
port = int(os.getenv('MQTT_PORT', 1883))
topic = os.getenv('MQTT_TOPIC', 'battery/reportEquip')
username = os.getenv('MQTT_USERNAME', None)  # New username variable
password = os.getenv('MQTT_PASSWORD', None)  # New password variable
ws_uri = "ws://baterway.com:9501/equip/info/"
token_url = "http://baterway.com/api/user/app/login"
heartbeat_interval = int(os.getenv('HEARTBEAT_INTERVAL', 60))
reconnect_delay = int(os.getenv('RECONNECT_DELAY', 60))
app_code = os.getenv('APP_CODE', 'ASGOFT')
login_name = get_env_variable('LOGIN_NAME')
password_auth = get_env_variable('PASSWORD')
token_credentials = {
    "appCode": app_code,
    "loginName": login_name,
    "password": password_auth
}
deviceId = get_env_variable('DEVICE_ID')

# Authorization Token Fetch
def get_auth_token():
    headers = {'Content-Type': 'application/json'}
    response = requests.post(token_url, json=token_credentials, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        if response_data['code'] == 200:
            return response_data['data']['token']
        else:
            raise Exception(f"Failed to fetch token: {response_data['message']}")
    else:
        raise Exception(f"HTTP error during token fetch: Status {response.status_code}")

# MQTT Connection Setup
def connect_mqtt():
    client = mqtt_client.Client()  # Utilise la dernière version API MQTT
    if username and password:  # If username and password are set, use them
        client.username_pw_set(username, password)
    client.connect(broker, port)
    return client

# Send Initial and Heartbeat Messages
async def send_initial_and_heartbeat_messages(ws):
    initial_message = json.dumps({"reportEquip": [deviceId]})
    heartbeat_message = json.dumps({"heartbeat": [deviceId]})
    while True:
        if ws.open:
            await ws.send(initial_message)
            print(f"Sent initial message: {initial_message}")
            await ws.send(heartbeat_message)
            print(f"Sent heartbeat message: {heartbeat_message}")
        else:
            print("WebSocket is closed. Attempting to reconnect...")
            break
        await asyncio.sleep(heartbeat_interval)

# Main WebSocket and MQTT loop
async def websocket_to_mqtt():
    client = connect_mqtt()
    client.loop_start()
    while True:
        try:
            token = get_auth_token()
            uri = ws_uri + token
            headers = {
                "Authorization": token,
                "content-type": "application/json",
                "User-Agent": "okhttp/3.12.11"
            }
            async with websockets.connect(uri, extra_headers=list(headers.items())) as websocket:
                consumer_task = asyncio.create_task(receive_messages(websocket, client))
                producer_task = asyncio.create_task(send_initial_and_heartbeat_messages(websocket))
                done, pending = await asyncio.wait(
                    [consumer_task, producer_task],
                    return_when=asyncio.FIRST_COMPLETED
                )
                for task in pending:
                    task.cancel()
        except Exception as e:
            print(f"Error: {e}. Reconnecting in {reconnect_delay} seconds...")
            await asyncio.sleep(reconnect_delay)

# Receive and handle messages from WebSocket
async def receive_messages(websocket, mqtt_client):
    try:
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")
            if "totalPv1power" in message:
                mqtt_client.publish(topic, message)
            else:
                print("Message does not contain 'totalPv1power', not publishing.")
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket connection closed.")

# Running the asyncio main function
async def main():
    await websocket_to_mqtt()

asyncio.run(main())
