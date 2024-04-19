import asyncio
import websockets
from consumer import register_at_coordinator

async def main():
    # Connect to the WebSocket server
    async with websockets.connect("ws://localhost:8765") as websocket:
        # Send a message to the server
        await websocket.send("Hello, WebSocket server!")

        # Receive and print the server's response
        response = await websocket.recv()
        print(f"Received from server: {response}")



# register_at_coordinator(1, 5, 3)

# Run the main coroutine
asyncio.run(main())

