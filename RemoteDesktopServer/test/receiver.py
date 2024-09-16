import asyncio
import websockets
import cv2
import numpy as np
import struct
import websockets
import cv2 






def decode_frame( jpeg_bytes):
    # バイナリデータを numpy 配列に変換
    nparr = np.frombuffer(jpeg_bytes, np.uint8)
    # numpy 配列を OpenCV 画像にデコード
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    
    return img





async def receive_data(websock, uri):
  
    try:
        while True: 
        
            jpeg_data = await websock.recv()
            decoded_data = decode_frame(jpeg_data)

            cv2.imshow(uri, decoded_data)

            if cv2.waitKey(1) == ord('q'):
                break
    except Exception as e:
        print(f"An error occurred: {e}")
    



async def handle_connection_task(uri):
    print(uri.split("/"))
    try:
        async with websockets.connect(uri) as websock: 
           
            await receive_data(websock, uri)
    except Exception as e:
        print(e)




async def request_test(): 
    uris = [
    "ws://localhost:8765/2",
    # "ws://localhost:8765/Edge",
    # "ws://localhost:8765/Notepad",
    # "ws://localhost:8765/Paint"
    ]
    try:
       tasks = [
            asyncio.create_task(handle_connection_task(uri)) for uri in uris
       ]

       await asyncio.gather(*tasks, return_exceptions=True)

    except Exception as e:
        print(f"An error occurred: {e}")


    



asyncio.run(request_test())




