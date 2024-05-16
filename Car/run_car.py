import asyncio
import json
import websockets
import time

class ServerConnectionsPool:
    def __init__(self, uris) -> None:
        self.uris = uris
        self.connections = []
        self.current_index = 0

    async def connect_all(self):
        for uri in self.uris:
            conn = await websockets.connect(uri)
            self.connections.append(conn)

    async def send_round_robin(self, message):
        if not self.connections:  # Ensure there are connections available
            raise Exception("No available WebSocket connections.")

        # Send a message using the current connection
        start = time.perf_counter()
        await self.connections[self.current_index].send(message)
        end = time.perf_counter()
        print(f"Write Latency: {round(end- start, 4)} seconds")

        # Move to the next connection in the list, wrapping around if necessary
        self.current_index = (self.current_index + 1) % len(self.connections)

    async def close_all(self):
        for conn in self.connections:
            await conn.close()
            print("closed one")
        print("closed all")

# Example usage
async def main():
    ip = "127.0.0.1"
    port = 8765
    car_id = 5

    uris = [f"ws://{ip}:{port}/car/{car_id}" for port in range(port, port+2)]

    try:
        ws_pool = ServerConnectionsPool(uris)
        
        await ws_pool.connect_all()

        with open('Car_samples/car_samples_data.txt', 'r') as fileIn:
            for line in fileIn:
                await ws_pool.send_round_robin(json.dumps(line.strip()))
                await asyncio.sleep(3)

    except KeyboardInterrupt:
        pass
    finally:
        await ws_pool.close_all()

# Run the example
try: 
    asyncio.run(main())
except KeyboardInterrupt:
    pass