from screen_shot_utils import ScreenShotUtil
import cv2
import asyncio
import websockets
import subprocess
import win32api
import win32con
from data_monitor import MonitorManager 






async def stream_window(websock, hwnd):

    monitor = ScreenShotUtil()
    try:
        while True: 
            
            frame = monitor.get_window_frame(hwnd)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            compressed_frame = monitor.compress_frame(frame)

            await websock.send(compressed_frame)
            # await websock.send(compressed_frame)
            
    except websockets.exceptions.ConnectionClosedOK:
        print("Connection was closed properly.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally: 
        monitor.closeSct()





async def window_process(websock, app_name):
 
    try: 
        if(app_name == "Notepad"):
            subprocess.Popen(['notepad.exe'])
            await asyncio.sleep(2)
            hwnd = ScreenShotUtil.get_window(app_name)

        if(app_name == "Edge"):
            
            edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
            url = "https://www.sony.co.jp/corporate/information/news/202401/24-001/"
            subprocess.Popen([edge_path, url])
            await asyncio.sleep(2)
            
            hwnd = ScreenShotUtil.get_window(app_name)
            
        

        if(app_name == "Paint"):
            # Paintを起動
            subprocess.Popen(['mspaint.exe'])
            await asyncio.sleep(2)  # 起動時間のため少し待つ

            # ScreenShotUtilを使ってウィンドウハンドルを取得
            hwnd = ScreenShotUtil.get_window(app_name)
        

        if app_name == "Calculator":
            subprocess.Popen(['calc.exe'])
            await asyncio.sleep(2)
            hwnd = ScreenShotUtil.get_window(app_name)



        MonitorManager.add_monitor(monitor_id=app_name, monitor_type = "window", monitor = hwnd)
           

        await stream_window(websock, hwnd)
    
        
    except Exception as e:
        print("Error occured", e)
    
    finally:
        if not websock.open:
            monitor = MonitorManager.get_monitors(app_name)
            if monitor:
                hwnd = monitor.get("monitor")
                if hwnd:
                    win32api.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0) 
                MonitorManager.remove_monitor(app_name)  # Monitorから削除
                print(f"Monitor for {app_name} has been closed and removed.")

    
         




async def stream_monitor(websock,id):

    monitor = ScreenShotUtil(id)
    MonitorManager.add_monitor(monitor_id=id, monitor_type = "monitor", monitor = monitor.monitor)
    try:

        while True: 
            frame = monitor.get_monitor_frame()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            compressed_frame = monitor.compress_frame(frame)
            await websock.send(compressed_frame)
    except websockets.exceptions.ConnectionClosedOK:
        print("Connection was closed properly.")
    except Exception as e:
        print(f"An error occurred: {e}") 
    finally:
        monitor.closeSct()