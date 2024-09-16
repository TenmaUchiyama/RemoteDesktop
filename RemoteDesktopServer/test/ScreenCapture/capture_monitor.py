import ctypes
import numpy as np
import cv2

# DLLをロードする (DLLのパスを指定してください)
dll = ctypes.CDLL(r'./ScreenCapture.dll')

# CaptureMonitor関数の定義
dll.CaptureMonitor.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
dll.CaptureMonitor.restype = ctypes.c_bool

# Windows API の構造体定義
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

class ICONINFO(ctypes.Structure):
    _fields_ = [("fIcon", ctypes.c_bool),
                ("xHotspot", ctypes.c_ulong),
                ("yHotspot", ctypes.c_ulong),
                ("hbmMask", ctypes.c_void_p),
                ("hbmColor", ctypes.c_void_p)]

class CURSORINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_ulong),
                ("flags", ctypes.c_ulong),
                ("hCursor", ctypes.c_void_p),
                ("ptScreenPos", POINT)]

# Windows API 呼び出し
user32 = ctypes.windll.user32
user32.GetCursorInfo.restype = ctypes.c_bool
user32.GetCursorInfo.argtypes = [ctypes.POINTER(CURSORINFO)]
user32.GetIconInfo.restype = ctypes.c_bool
user32.GetIconInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(ICONINFO)]

def capture_monitor_image():
    # 画面の幅と高さを取得するための変数を準備
    width = ctypes.c_int(0)
    height = ctypes.c_int(0)

    # 一度DLLを呼び出して画面サイズを取得する
    dll.CaptureMonitor(None, ctypes.byref(width), ctypes.byref(height))

    # 幅と高さが0の場合、キャプチャに失敗
    if width.value == 0 or height.value == 0:
        print("Failed to capture monitor.")
        return None

    # 画面サイズに基づいてピクセルデータを格納するためのバッファを確保
    pixel_data_size = width.value * height.value * 4  # 32ビット（4バイト）BGRAフォーマット
    pixel_data = (ctypes.c_ubyte * pixel_data_size)()

    # 実際に画面をキャプチャする
    success = dll.CaptureMonitor(pixel_data, ctypes.byref(width), ctypes.byref(height))

    # キャプチャに成功したかどうかを確認
    if not success:
        print("Failed to capture monitor.")
        return None

    # キャプチャされたピクセルデータをNumPy配列に変換
    np_pixel_data = np.ctypeslib.as_array(pixel_data).reshape((height.value, width.value, 4))

    # BGRAフォーマットをBGRに変換 (cv2はBGRフォーマットを使用する)
    bgr_image = cv2.cvtColor(np_pixel_data, cv2.COLOR_BGRA2BGR)

    return bgr_image, width.value, height.value

def draw_cursor_on_image(image):
    # カーソル情報を取得
    cursor_info = CURSORINFO()
    cursor_info.cbSize = ctypes.sizeof(CURSORINFO)
    
    if not user32.GetCursorInfo(ctypes.byref(cursor_info)):
        print("Failed to get cursor info.")
        return image
    
    # カーソルが表示されている場合
    if cursor_info.flags == 1:  # CURSOR_SHOWING == 1
        icon_info = ICONINFO()
        
        # カーソルのアイコン情報を取得
        if user32.GetIconInfo(cursor_info.hCursor, ctypes.byref(icon_info)):
            cursor_pos = (cursor_info.ptScreenPos.x, cursor_info.ptScreenPos.y)
            
            # カーソルの描画 (ここでは単純な白い丸でカーソルを模倣します)
            cv2.circle(image, cursor_pos, 10, (255, 255, 255), -1)  # カーソルを白い円で描画

    return image

if __name__ == "__main__":
    # 画面キャプチャを実行
    while True: 
        image, width, height = capture_monitor_image()


        # カーソルを描画
        image_with_cursor = draw_cursor_on_image(image)

        # 画像を表示する
        cv2.imshow("Monitor Capture with Cursor", image_with_cursor)
        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()  # ウィンドウを閉じる
