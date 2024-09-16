import asyncio 
import websockets








async def sending_msg_process(websock):

    try:
        while True: 
            await websock.send("A")
            await asyncio.sleep(1)
            await websock.send("B")
            await asyncio.sleep(1)
    except websockets.exceptions.ConnectionClosedOK:
        print("Connection was closed properly.")
    except Exception as e:
        print(f"An error occurred: {e}") 




async def handle_client(websocket, path):
    print(f"New connection at {path}")
    try:
        async for message in websocket:
            # Handle incoming messages here
            print(f"Received message from {path}: {message}")

    except websockets.exceptions.ConnectionClosed as e:
        # Handle client disconnection
        print(f"Client disconnected from {path}. Exception: {e}")
    finally:
        # Clean up actions when client disconnects
        print(f"Cleanup for {path}")




async def server (): 
    server = await websockets.serve(handle_client, "localhost", 8765)
    print("WebSocket server started on ws://0.0.0.0:8765")
    await server.wait_closed()


asyncio.run(server())