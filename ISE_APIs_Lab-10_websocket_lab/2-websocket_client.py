import asyncio
import websockets
import sys
from crayons import *

port = 8000

async def chat():
    uri = f"ws://localhost:{port}"
    try:
        print(yellow(f"Connecting to server at {uri}...",bold=True))
        async with websockets.connect(uri) as websocket:
            print(green("\nConnection to server OKAY !\n",bold=True))
            print("Start chatting (type messages and press Enter)")
            
            async def receive():
                try:
                    async for message in websocket:
                        print(cyan(message,bold=True))
                        print(">: ", end="", flush=True)  # Prompt again after receiving
                except websockets.exceptions.ConnectionClosed:
                    print(red("\nConnection to server closed",bold=True))
                    return
                except Exception as e:
                    print(red(f"\nError receiving message: {e}",bold=True))
                    return

            async def send():
                try:
                    while True:
                        # Use asyncio.to_thread to make input non-blocking
                        msg = await asyncio.to_thread(input, "\nMe : ")
                        if msg.lower() == "exit":
                            print("Disconnect ...")
                            sys.exit(0)
                        await websocket.send(msg)
                except websockets.exceptions.ConnectionClosed:
                    print(red("\n--INFO-- Connection to server closed",bold=True))
                    return
                except Exception as e:
                    print(red(f"\nError sending message: {e}",bold=True))
                    return

            await asyncio.gather(receive(), send())
    except ConnectionRefusedError:
        print(red("--WARNING-- Could not connect to server",bold=True))
    except Exception as e:
        print(red(f"Error: {e}",bold=True))

if __name__ == "__main__":
    try:
        asyncio.run(chat())
    except KeyboardInterrupt:
        print("\nExiting from session ...")
        sys.exit(0)