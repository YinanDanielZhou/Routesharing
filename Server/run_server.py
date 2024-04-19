import asyncio
import json
import signal
import sys
import websockets
import mysql.connector

from server import register_at_coordinator, write_location_to_db

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="my_pool",
    pool_size=5,
    host='localhost',
    database='server',
    user='mytestuser',
    password=''
)

def get_connection():
    return connection_pool.get_connection()



# Define a WebSocket handler function
async def websocket_handler(websocket, path):
    # Print a message when a new connection is established
    print("Client connected")
    print(path)
    car_id = int(path[1:])
    mysql_connection = get_connection()

    try:
        # Continuously handle messages from the client
        async for message in websocket:
            write_location_to_db(mysql_connection, car_id, message)

    finally:
        # Print a message when the connection is closed
        mysql_connection.close()
        print("Client disconnected")

# Start the WebSocket server
async def start_server(port):
    # Create a WebSocket server
    async with websockets.serve(websocket_handler, "localhost", port):
        # Print a message when the server starts
        print("Server started")

        # Keep the server running indefinitely
        await asyncio.Future()  # Wait forever



# ip = "192.168.0.0"  # get self ip and port
# port = 10000
# register_at_coordinator(ip, port)


# Run the WebSocket server
def shutdown_handler(sig, frame):
    # clean up the connection pool after 
    connection_pool._remove_connections()

    print("Shutting down Server...")
    asyncio.get_event_loop().stop()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

port = 8765
asyncio.run(start_server(port))


