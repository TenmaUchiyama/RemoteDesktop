
import asyncio
import ctypes 
import time 
import win32con 
import cairosvg
import numpy as np 
import cv2 
import win32api
import pyautogui
import pynput
from screeninfo import get_monitors
import mss
import pygetwindow




class ScreenShotUtil:
    monitor_id : int
    is_primary :bool = True
    x : int 
    y : int 
    width : int 
    height : int 

    
    
   

    def __init__(self, monitor_id = None):
       
     
        self.sct = mss.mss()


        if(monitor_id):
            monitors = self.sct.monitors
            self.monitor_id = int( monitor_id)
            self.monitor = monitors[self.monitor_id] 

            
            self.x = self.monitor["left"]
            self.y =self.monitor["top"]
            self.width = self.monitor["width"]
            self.height = self.monitor["height"]

            self.position_norm = (self.x + self.width // 2, self.y + self.height // 2)


            self.total_width_offset= 0 
            self.total_height_offset= 0
  
            
       
        
        


        self.cursor_mapping = {
        ctypes.windll.user32.LoadCursorW(0,win32con.IDC_ARROW): "C:\\Windows\\Cursors\\arrow.svg",
        ctypes.windll.user32.LoadCursorW(0,win32con.IDC_WAIT): "C:\\Windows\\Cursors\\wait.svg",
        ctypes.windll.user32.LoadCursorW(0,win32con.IDC_APPSTARTING): "C:\\Windows\\Cursors\\busy.svg",
        ctypes.windll.user32.LoadCursorW(0,win32con.IDC_HAND): "C:\\Windows\\Cursors\\link.svg",
        ctypes.windll.user32.LoadCursorW(0,win32con.IDC_IBEAM): "C:\\Windows\\Cursors\\ibeam.svg",
        ctypes.windll.user32.LoadCursorW(0,win32con.IDC_CROSS): "C:\\Windows\\Cursors\\cross.svg",
        ctypes.windll.user32.LoadCursorW(0,win32con.IDC_NO): "C:\\Windows\\Cursors\\unavail.svg",
        ctypes.windll.user32.LoadCursorW(0,win32con.IDC_SIZEALL): "C:\\Windows\\Cursors\\move.svg",
        ctypes.windll.user32.LoadCursorW(0,win32con.IDC_SIZEWE): "C:\\Windows\\Cursors\\ew.svg",
        ctypes.windll.user32.LoadCursorW(0,win32con.IDC_SIZENWSE): "C:\\Windows\\Cursors\\nwse.svg",
        ctypes.windll.user32.LoadCursorW(0,win32con.IDC_SIZENESW): "C:\\Windows\\Cursors\\nesw.svg",
        ctypes.windll.user32.LoadCursorW(0,win32con.IDC_SIZENS): "C:\\Windows\\Cursors\\ns.svg"
        }

        self.require_transport = [
            ctypes.windll.user32.LoadCursorW(0,win32con.IDC_IBEAM),
            ctypes.windll.user32.LoadCursorW(0,win32con.IDC_CROSS) ,
            ctypes.windll.user32.LoadCursorW(0,win32con.IDC_APPSTARTING),
            ctypes.windll.user32.LoadCursorW(0,win32con.IDC_NO),
            ctypes.windll.user32.LoadCursorW(0,win32con.IDC_SIZEWE),
            ctypes.windll.user32.LoadCursorW(0,win32con.IDC_SIZENWSE),
            ctypes.windll.user32.LoadCursorW(0,win32con.IDC_SIZENESW),
            ctypes.windll.user32.LoadCursorW(0,win32con.IDC_SIZENS)
            
            ]
        self.cursor_imgmap = {}

        for key in self.cursor_mapping:
            cursor_image = cairosvg.svg2png(url=self.cursor_mapping[key])
            cursor_np = np.frombuffer(cursor_image, np.uint8)
            cursor_img = cv2.imdecode(cursor_np, cv2.IMREAD_UNCHANGED)
            cursor_img = cv2.flip(cursor_img, 0)
            cursor_img = cv2.resize(cursor_img, (64, 64))    
            self.cursor_imgmap[key] = cursor_img




    class CURSORINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong),
                    ("flags", ctypes.c_ulong),
                    ("hCursor", ctypes.c_void_p),
                    ("ptScreenPos", ctypes.c_ulong * 2)]
    


    def closeSct(self):
        self.sct.close()


    def get_cursor_imgmap(self):
        return self.cursor_imgmap


    def get_current_window_size(self):
        return (self.x, self.y, self.width, self.height)

    def get_current_cursor(self):
        
        cursor_info = self.CURSORINFO()
        cursor_info.cbSize = ctypes.sizeof(self.CURSORINFO)
        ctypes.windll.user32.GetCursorInfo(ctypes.byref(cursor_info))
        if cursor_info.flags == win32con.CURSOR_SHOWING:
            hCursor = cursor_info.hCursor
            if hCursor in self.cursor_imgmap: 
                return self.cursor_imgmap[hCursor] , hCursor in self.require_transport
        return None, False
            
        


    def get_monitor_frame(self):
        
        
        # 指定したモニターの情報を取得
        monitor = self.sct.monitors[self.monitor_id]
        screenshot = self.sct.grab(monitor)

        screenshot_np = self.render_screen_shot(screenshot, monitor)

        return screenshot_np



    def render_screen_shot(self, screenshot, monitor):
        cursor_img, is_offset_required = self.get_current_cursor()
        screenshot_np = np.array(screenshot)

       
        screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)


        if cursor_img is None:
            return screenshot_np

        
       
        mouse = pynput.mouse.Controller()
        cursor_position = mouse.position  # (x, y)

      
        x = int(cursor_position[0] - monitor["left"])
        y = int(cursor_position[1] - monitor["top"])

        if is_offset_required:
       
            x -= 32  
            y -= 32 
        
        h, w = cursor_img.shape[:2]
        screen_height, screen_width = screenshot_np.shape[:2]


        if 0 <= x < screen_width and 0 <= y < screen_height:
            x_start = max(x, 0)
            y_start = max(y, 0)
            x_end = min(x + w, screen_width)
            y_end = min(y + h, screen_height)


            cursor_x_start = x_start - x
            cursor_y_start = y_start - y
            cursor_x_end = cursor_x_start + (x_end - x_start)
            cursor_y_end = cursor_y_start + (y_end - y_start)

            cursor_region = cursor_img[cursor_y_start:cursor_y_end, cursor_x_start:cursor_x_end]
            background_region = screenshot_np[y_start:y_end, x_start:x_end]


            alpha_mask = cursor_region[:, :, 3] / 255.0
            alpha_mask = alpha_mask[:, :, np.newaxis]

        
            blended_region = (alpha_mask * cursor_region[:, :, :3] + (1 - alpha_mask) * background_region).astype(np.uint8)

      
            screenshot_np[y_start:y_end, x_start:x_end] = blended_region
    
        return screenshot_np

    



    def get_window_bbox(self, window):

  

        offset_x = 10
        offset_width = -20

        offset_y = 2
        offset_height = -10

        left, top, width, height = window.left +  offset_x , window.top  + offset_y, window.width + offset_width, window.height + offset_height
        
        return {"top": top, "left": left, "width": width, "height": height}





    @staticmethod
    def get_window(rough_name = ""):
        # 開いているウィンドウの一覧を取得
        
        windows = pygetwindow.getWindowsWithTitle('')
        output = []
        # 各ウィンドウのタイトルを表示

        for window in windows:
            if rough_name in window.title:
                    
                output.append(window)
        
        return output[0]
    


    def get_window_frame(self, hwnd):
        
        # ウィンドウまたはモニターのバウンディングボックスを取得
        monitor = self.get_window_bbox(hwnd)
        screenshot = self.sct.grab(monitor)
        
        screenshot_np = self.render_screen_shot(screenshot, monitor)
        return screenshot_np


    def decode_frame(self, jpeg_bytes):
        # バイナリデータを numpy 配列に変換
        nparr = np.frombuffer(jpeg_bytes, np.uint8)
        # numpy 配列を OpenCV 画像にデコード
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        
        return img

    def compress_frame(self,frame):
        _, jpeg = cv2.imencode('.jpg', frame)
        jpeg_bytes = jpeg.tobytes()
        return jpeg_bytes