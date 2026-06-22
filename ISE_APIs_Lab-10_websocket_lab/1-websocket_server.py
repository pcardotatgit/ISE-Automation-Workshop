import asyncio
import websockets
from crayons import *

connected_clients = set()
listening_port=8000

async def handler(websocket):
    connected_clients.add(websocket)
    print(yellow("\n--INFO-- Client Connected", bold=True))
    try:
        async for message in websocket:
            # Send back to sender
            await websocket.send(f"Echo from server : {message}")
            print("<= Received from client : ",green(message,bold=True),'\n')
            # Broadcast to every connected client
            await asyncio.gather(*[client.send(f"Message received from a client : {message}") for client in connected_clients if client != websocket])
    finally:
        connected_clients.remove(websocket)
        print(yellow("\n--INFO-- Client Disconnection", bold=True))

async def server_input():
    while True:
        try:
            # Use asyncio.to_thread to make input non-blocking
            msg = await asyncio.to_thread(input, "Send a message to everyone : ")
            if connected_clients:  # Check if there are any connected clients
                await asyncio.gather(*[
                    client.send(f"\n    ==> Server Said : {msg}")
                    for client in connected_clients
                ])
                print(" ==> Sending out : ",cyan(msg,bold=True),'\n')
            else:
                print(red("\nNo clients connected",bold=True))
        except Exception as e:
            print(red(f"Error in server input: {e}",bold=True))

async def main():
    server = await websockets.serve(handler, "localhost", listening_port)
    print(yellow(f"\n--INFO-- Server is running on ws://localhost:{listening_port}\n",bold=True))
    print(green("\nWaiting for client connections...\n",bold=True))
    
    # Run both server input handling and keep the server alive
    await asyncio.gather(
        server_input(),
        asyncio.Future()  # This future never completes, keeping the server running
    )

if __name__ == "__main__":
    asyncio.run(main())