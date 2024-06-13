import asyncio
import os
import signal
import sys
import websockets
import mysql.connector

from server import extract_sample_from_db, register_at_coordinator, write_sample_to_db

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="my_pool",
    pool_size=5,
    # host='127.0.0.1',
    # database='server',
    # user='mytestuser',
    # password=''
    host=os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_DATABASE')
)


def get_connection():
    return connection_pool.get_connection()


async def car_connection_handler(websocket, car_id):
    mysql_connection = get_connection()

    try:
        # Continuously handle messages from the client
        async for message in websocket:
            print("received ", message)
            write_sample_to_db(mysql_connection, car_id, message)
        print()
    except Exception as e:
        print("Car connection handler caught error: " + e)
    finally:
        # Print a message when the connection is closed
        mysql_connection.close()
        print("Car disconnected")


async def consumer_connection_handler(websocket, car_id):
    mysql_connection = get_connection()

    try:
        async for message in websocket:
            print("Consumer requesting ", message, " samples of car ", car_id)
            extracted_samples = extract_sample_from_db(mysql_connection, car_id, int(message))
            for sample in extracted_samples:
                await websocket.send(sample)
            await websocket.send("DONE")
            print("Returned ", len(extracted_samples), " samples of car " , car_id, " to the Consumer.")
    except Exception as e:
        print("Consumer connection handler caught error: " + e)
    finally:
        mysql_connection.close()
        print("Consumer disconnected")

# Define a WebSocket handler function
async def websocket_handler(websocket, path):
    # Print a message when a new connection is established
    arg_list = path.split('/')
    if arg_list[1] == 'car':
        print("Car connected")
        await car_connection_handler(websocket, arg_list[2])
    elif arg_list[1] == 'consumer':
        print("Consumer connected")
        await consumer_connection_handler(websocket, arg_list[2])


# Start the WebSocket server
async def start_server(port):
    # Create a WebSocket server
    async with websockets.serve(websocket_handler, '0.0.0.0', port):
        # Print a message when the server starts
        print("Server started")

        # Keep the server running indefinitely
        await asyncio.Future()  # Wait forever



# Run the WebSocket server
def shutdown_handler(sig, frame):
    # clean up the connection pool after 
    connection_pool._remove_connections()

    print("Shutting down Server...")
    asyncio.get_event_loop().stop()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)



COORDINATOR_URL = f"http://{sys.argv[1]}/register/server"
ip = sys.argv[2]
port = int(sys.argv[3])
register_at_coordinator(COORDINATOR_URL, ip, port)


port = 8765
asyncio.run(start_server(port))


