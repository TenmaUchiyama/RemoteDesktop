import asyncio
import websockets
from monitor_handler import stream_monitor, window_process
from input_handler import handle_input

async def handle_client(websocket, path):

  
    print(f"New connection at {path}")
    try:
        id =path.split("/")[-1]

        if(id.isdigit()):
            await stream_monitor(websocket, id)
        elif(id == "monitor_input"):
            await handle_input(websocket)
        else:
            await window_process(websocket, id)


    

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