
import ctypes 
import time 
import win32con 
import cairosvg
import numpy as np 
import cv2 
import pygetwindow
import pyautogui
import pynput
from screeninfo import get_monitors


class ScreenShotUtil:
    is_primary :bool = True
    x : int 
    y : int 
    width : int 
    height : int 

    def __init__(self, monitor_id = None):
        if monitor_id: 
            monitors = get_monitors()
            monitor = monitors[monitor_id]
            self.is_primary = False
    
            self.x = monitor.x
            self.y = monitor.y
            self.width = monitor.width
            self.height = monitor.height
        


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
            cursor_img = cv2.resize(cursor_img, (32, 32))    
            self.cursor_imgmap[key] = cursor_img




    class CURSORINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong),
                    ("flags", ctypes.c_ulong),
                    ("hCursor", ctypes.c_void_p),
                    ("ptScreenPos", ctypes.c_ulong * 2)]
    




    def get_cursor_imgmap(self):
        return self.cursor_imgmap



    def get_current_cursor(self):
        cursor_info = self.CURSORINFO()
        cursor_info.cbSize = ctypes.sizeof(self.CURSORINFO)
        ctypes.windll.user32.GetCursorInfo(ctypes.byref(cursor_info))
        if cursor_info.flags == win32con.CURSOR_SHOWING:
        
            hCursor = cursor_info.hCursor
            
            return self.cursor_imgmap[hCursor], hCursor in self.require_transport
        
    from screeninfo import get_monitors

    monitors = get_monitors()


    def get_monitor(self):
        cursor_img , is_offset_required= self.get_current_cursor()
        

        screenshot =  pyautogui.screenshot() 

        screenshot_np = np.array(screenshot)

        # BGR形式に変換（PillowはRGB、OpenCVはBGRを使用）
        screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

        # カーソルの位置を取得
        mouse = pynput.mouse.Controller()
        cursor_position = mouse.position

        # カーソルをスクリーンショットに重ねる
        x, y = int(cursor_position[0]), int(cursor_position[1])


        if is_offset_required:
            # オフセットを追加する（例：x座標を10ピクセル右に、y座標を10ピクセル下に）
            x -= 16 # 右に10ピクセルずらす
            y -= 16  # 下に10ピクセルずらす


        h, w = cursor_img.shape[:2]
        screen_height, screen_width = screenshot_np.shape[:2]
        # カーソル画像のアルファチャンネルを使って合成
        for i in range(h):
            for j in range(w):
                if cursor_img[i, j, 3] > 0 :  # アルファ値が0以上のピクセルのみ描画
                    if 0 <= x + j < screen_width and 0 <= y + i < screen_height:
                        screenshot_np[y + i, x + j] = cursor_img[i, j, :3]  # RGB値を合成



        return screenshot_np
    


    


    def get_window_bbox(self, window_title):
        # ウィンドウを取得
        window = gw.getWindowsWithTitle(window_title)[0]

        offset_x = 10
        offset_width = -20

        offset_y = 2
        offset_height = -10

        left, top, width, height = window.left +  offset_x , window.top  + offset_y, window.width + offset_width, window.height + offset_height

        return {"top": top, "left": left, "width": width, "height": height}






    def get_window_name(self, rough_name = ""):
        # 開いているウィンドウの一覧を取得
        windows = gw.getWindowsWithTitle('')
        output = []
        # 各ウィンドウのタイトルを表示
        for window in windows:
            if rough_name in window.title:
                output.append(window.title)
        
        return output
    


    def get_window(self):
        cursor_img , is_offset_required= self.get_current_cursor()
        

        monitor = self.get_window_bbox("Edge")
        screenshot = self.sct.grab(monitor)

        screenshot_np = np.array(screenshot)

        # BGR形式に変換（PillowはRGB、OpenCVはBGRを使用）
        screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

        # カーソルの位置を取得
        mouse = pynput.mouse.Controller()
        cursor_position = mouse.position

        # カーソルをスクリーンショットに重ねる
        x, y = int(cursor_position[0]), int(cursor_position[1])


        if is_offset_required:
            # オフセットを追加する（例：x座標を10ピクセル右に、y座標を10ピクセル下に）
            x -= 16 # 右に10ピクセルずらす
            y -= 16  # 下に10ピクセルずらす


        h, w = cursor_img.shape[:2]
        screen_height, screen_width = screenshot_np.shape[:2]
        # カーソル画像のアルファチャンネルを使って合成
        for i in range(h):
            for j in range(w):
                if cursor_img[i, j, 3] > 0 :  # アルファ値が0以上のピクセルのみ描画
                    if 0 <= x + j < screen_width and 0 <= y + i < screen_height:
                        screenshot_np[y + i, x + j] = cursor_img[i, j, :3]  # RGB値を合成



        return screenshot_np
