import asyncio
import websockets
import time

class ServerConnectionsPool:
    def __init__(self, uris) -> None:
        self.uris = uris
        self.connections = []
        self.current_index = 0

    async def connect_all(self):
        for uri in self.uris:
            print(uri)
            conn = await websockets.connect(uri)
            self.connections.append(conn)

    async def send_all(self, requested_sample_quantity):
        if not self.connections:  # Ensure there are connections available
            raise Exception("No available WebSocket connections.")

        tasks = []
        for conn in self.connections:
            tasks.append(conn.send(str(requested_sample_quantity)))
        
        await asyncio.gather(*tasks)


    async def receive_all(self):
        if not self.connections:  # Ensure there are connections available
            raise Exception("No available WebSocket connections.")
        try:
            for i in range(len(self.connections)):
                conn = self.connections[i]
                while True:
                    response = await conn.recv()
                    print(i, response)
                    if response == "DONE":
                        break
        except websockets.exceptions.ConnectionClosed:
            print("Server closed the conneciton.")

        
    async def close_all(self):
        print("closing...")
        for conn in self.connections:
            await conn.close()
            print("closed one")
        print("closed all")


async def main():
    ip = "127.0.0.1"
    port = 8765
    car_id = 5

    uris = [f"ws://{ip}:{port}/consumer/{car_id}" for port in range(port, port+2)]

    try:
        ws_pool = ServerConnectionsPool(uris)
        await ws_pool.connect_all()
        print(f"Connected to {len(uris)} Servers")

        try:
            while True:
                try:
                    requested_sample_quantity = abs(int(input("how many car sample to pull from each server (0 to exit): ")))
                    if requested_sample_quantity == 0:
                        break
                    start = time.perf_counter()
                    await ws_pool.send_all(requested_sample_quantity)
                    await ws_pool.receive_all()
                    end = time.perf_counter()
                    print(f"Read latency: {round(end - start, 4)} seconds")
                except ValueError as e:
                    print("please a input valid number")
                    continue
                
        except websockets.exceptions.ConnectionClosed:
            print("Server closed the conneciton.")

    except KeyboardInterrupt:
        pass
    finally:
        await ws_pool.close_all()

# Run the main coroutine
asyncio.run(main())

