import asyncio
import websockets

async def send_obj_file(uri, obj_file_path):
    async with websockets.connect(uri) as websocket:
        with open(obj_file_path, 'rb') as f:
            data = f.read()
            await websocket.send(data)
            print("OBJファイルを送信しました。")

uri = 'ws://192.168.10.107:8080/obj' 
obj_file_path = r"C:\Users\Tenma\Desktop\SONY_intern\RemoteDesktop\RemoteDesktop\RemoteDesktopServer\ObjSender\car\bugatti\bugatti.obj"  # Replace with your OBJ file path

asyncio.run(send_obj_file(uri, obj_file_path))
