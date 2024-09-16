import win32ui
import win32gui
import win32com
import win32con
import win32com.client
import ctypes
import ctypes.wintypes
from functools import partial
import numpy as np
import mss
from mss.base import MSSBase
from typing import Union

GW_OWNER = 4
DWMWA_= 9
def get_scene_color3( hwnd:int, is_foreground:bool = True) -> np.ndarray:
        
        window_rect = win32gui.GetWindowRect(hwnd) 


        offset_x = 10
        offset_y = 40

        width = window_rect[2] - window_rect[0] -20
        height = window_rect[3] - window_rect[1] - 50
        

        # get the window image data
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (width, height), dcObj, (offset_x, offset_y), win32con.SRCCOPY)

        # convert the raw data into a format opencv can read
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        image = np.frombuffer(signedIntsArray, dtype=np.uint8).reshape((height, width, 4))

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # drop the alpha channel
        image = np.flip(image[:, :, :3], 2)  # BGRA2RGB

        return image



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
     print(i)
# for i in data:
#     if("Powershell" in i):
#         output = i
# print(output)


import cv2 

window =win32gui.FindWindow(None, "OpenXR_Practice - BasicScene - Android - Unity 2022.3.12f1 <DX11>")


sct =  mss.mss()


while True: 
     
    img_data = get_scene_color3(window,sct)
    img_data =  cv2.cvtColor(img_data, cv2.COLOR_RGB2BGR)
    cv2.imshow("show", img_data)

    if cv2.waitKey(1) == ord('q'):
         break