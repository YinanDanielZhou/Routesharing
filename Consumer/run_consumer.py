import asyncio
import websockets
from consumer import register_at_coordinator

async def main():
    ip = "127.0.0.1"
    port = 8765
    car_id = 5
    url = f"ws://{ip}:{port}/consumer/{car_id}"
    requested_sample_quantity = 10

    # Connect to the WebSocket server
    async with websockets.connect(url) as websocket:
        # Send a message to the server
        await websocket.send(str(requested_sample_quantity))

        # Receive and print the server's response
        try:
            while True:
                response = await websocket.recv()
                print(response)
                if response == "DONE":
                    break
        except websockets.exceptions.ConnectionClosed:
            print("Server closed the conneciton.")

# uncomment below to register
# register_at_coordinator(1, 5, 3)

# Run the main coroutine
asyncio.run(main())

