import websockets
import asyncio
import json

async def request_test():
    
    try:

        async with websockets.connect("ws://localhost:8765/monitor_input") as websock:
            print("Connected to server")
            msg = json.dumps({"type": "cursor", "monitor_id": 2, "position": {"x": 0.4, "y": 0.2}})
            await websock.send(msg)




            
    except websockets.exceptions.ConnectionClosedOK:
        print("Connection closed normally. Reconnecting...")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Reconnecting in 5 seconds...")

# asyncio.run() で非同期関数を実行
asyncio.run(request_test())
