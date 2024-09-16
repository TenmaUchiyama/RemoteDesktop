
import ctypes 
import time 
import win32con 
import cairosvg
import numpy as np 
import cv2 
import win32api

class CURSORINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_ulong),
                ("flags", ctypes.c_ulong),
                ("hCursor", ctypes.c_void_p),
                ("ptScreenPos", ctypes.c_ulong * 2)]
cursor_mapping = {
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


cursor_imgmap = {}
for key in cursor_mapping:
    cursor_image = cairosvg.svg2png(url=cursor_mapping[key])
    cursor_np = np.frombuffer(cursor_image, np.uint8)
    cursor_img = cv2.imdecode(cursor_np, cv2.IMREAD_UNCHANGED)
    cursor_img = cv2.flip(cursor_img, 0)
    cursor_img = cv2.resize(cursor_img, (32, 32)) 
    cursor_imgmap[key] = cursor_img




def get_cursor_imgmap():
    return cursor_imgmap



def get_current_cursor():
    cursor_info = CURSORINFO()
    cursor_info.cbSize = ctypes.sizeof(CURSORINFO)
    ctypes.windll.user32.GetCursorInfo(ctypes.byref(cursor_info))
    if cursor_info.flags == win32con.CURSOR_SHOWING:
       
        hCursor = cursor_info.hCursor
        
        return cursor_imgmap[hCursor]
    
