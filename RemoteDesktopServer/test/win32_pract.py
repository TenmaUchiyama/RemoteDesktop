import win32gui 
GW_OWNER =4 


data = []
def list_window_names():
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            # print(hex(hwnd), win32gui.GetWindowText(hwnd))
            data.append(win32gui.GetWindowText(hwnd))

    win32gui.EnumWindows(winEnumHandler, None)

list_window_names()
output = ""

for i in data:
    if("Unity" in i and "Hub" not in i):
        output = i
print(output)



import time
import cv2 
import ctypes
from PIL import ImageGrab


hwnd = win32gui.FindWindow(None, output)
if hwnd:
    # 前面に移動
    win32gui.SetForegroundWindow(hwnd)
 
    # 1秒待つ
    time.sleep(1)
 
    # ウィンドウサイズを取得
    window_size = win32gui.GetWindowRect(hwnd)
 
    # 取得したウィンドウサイズでスクリーンショットを撮る
    f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    rect = ctypes.wintypes.RECT()
    DWMWA_EXTENDED_FRAME_BOUNDS = 9
    f(  ctypes.wintypes.HWND(hwnd),
        ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
        ctypes.byref(rect),
        ctypes.sizeof(rect)
    )


    image = ImageGrab.grab((rect.left, rect.top, rect.right, rect.bottom))
    image.show()
