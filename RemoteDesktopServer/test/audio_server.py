import asyncio
import websockets
import pyaudio

# PyAudioの設定
chunk = 1024
sample_rate = 44100
format = pyaudio.paInt16
channels = 2

p = pyaudio.PyAudio()
stream = p.open(format=format,
                channels=channels,
                rate=sample_rate,
                output=True)

async def handle_client(websocket, path):
    print("Client connected")
    try:
        async for message in websocket:
            if message:
                # 音声データを再生
                stream.write(message)
    except websockets.ConnectionClosed:
        print("Client disconnected")

async def server():
    server = await websockets.serve(handle_client, "localhost", 8765)
    print("WebSocket server started on ws://localhost:8765")
    await server.wait_closed()

asyncio.run(server())
