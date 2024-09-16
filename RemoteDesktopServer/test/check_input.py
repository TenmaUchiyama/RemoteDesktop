import json
import websockets
import asyncio
from input_handler import function_mapping




async def handle_input(websocket, path):
    print("receive connection")
    try: 
        async for message in websocket:
            print(message)
            json_message = json.loads(message)
            call_back = function_mapping.get(json_message.get("type"))
            if(call_back):
                call_back(json_message)
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Client disconnected. Exception: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


async def server_run():
    server = await websockets.serve(handle_input, "localhost", 8765)
    print("Server started")
    await server.wait_closed()
    
asyncio.run(server_run())