import asyncio
import json
import signal
import sys
import websockets


from car import initialize

consumer_server_lookup = dict()

async def connect_to_server(ip, port, car_id):
    ip = "127.0.0.1"
    port = 8765
    car_id = 5
    url = f"ws://{ip}:{port}/car/{car_id}"

    sample = {"location" : {"x": 1, "y": 1}, "timestamp" : "....."}

    # Connect to the WebSocket server
    async with websockets.connect(url) as websocket:

        while True:
            # Send a message to the server
            sample["location"]['x'] += 1
            sample["location"]['y'] += 1

            await websocket.send(json.dumps(sample))

            await asyncio.sleep(3)
            


# initialize(consumer_server_lookup)

# Run the main coroutine
def shutdown_handler(sig, frame):
    print("Shutting down car connection to server.")
    asyncio.get_event_loop().stop()
    sys.exit(0)
signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

asyncio.run(connect_to_server("IP, need replace", "Port, need replace", "Car_id, need replace"))
