import websockets
import asyncio 


async def send_request(websock, endpoint, time):
    print("Connected to the server.")
    await asyncio.sleep(time)
    print(f"Sending request to {endpoint}")
    await asyncio.sleep(time * 1.2)
    print("Request sent. Connection will be closed now.")
    await websock.close()




async def receive_test(websock):
    try:
        while True:
            msg = await websock.recv()
            print(f"Received message: {msg}")
    except websockets.exceptions.ConnectionClosedOK:
        print("Connection was closed properly.")
    except Exception as e:
        print(f"An error occurred: {e}")

    
    


async def connect_to_server_in_async(endpoint, time):
    uri = f"ws://localhost:8765/{endpoint}"
    try:
        async with websockets.connect(uri) as websock:
            sending_task = asyncio.create_task(send_request(websock, endpoint, time))
            receiving_task = asyncio.create_task(receive_test(websock))
            await sending_task  # Wait for the sending task to complete
            receiving_task.cancel()  # Cancel the receiving task when sending is done
    except Exception as e:
        print(f"Failed to connect or communicate with {endpoint}: {e}")

      
  


async def main():
    endpoints = [
        "A", "B", "C"
    ]
    tasks = [
        connect_to_server_in_async(endpoint, time) 
        for endpoint, time in zip(endpoints, [1, 5, 10])
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for result in results:
        if isinstance(result, Exception):
            print(f"Task encountered an error: {result}")





asyncio.run(main())