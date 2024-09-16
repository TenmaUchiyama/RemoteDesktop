import asyncio
import websockets
import pyaudio

# PyAudioの設定
chunk = 1024
sample_rate = 44100
format = pyaudio.paInt16
channels = 1

# 音声キャプチャの設定
p = pyaudio.PyAudio()
stream = p.open(format=format,
                channels=channels,
                rate=sample_rate,
                input=True,
                frames_per_buffer=chunk)

async def send_audio():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            data = stream.read(chunk)
            await websocket.send(data)

asyncio.run(send_audio())
