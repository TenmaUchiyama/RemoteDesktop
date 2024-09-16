import subprocess
import time
import pygetwindow as gw
import pyautogui
import cv2
import numpy as np

# 特定のアプリケーションを起動 (例: メモ帳)
subprocess.Popen(['notepad.exe'])



# ウィンドウ名を指定して取得（例: メモ帳）
window = gw.getWindowsWithTitle("Untitled - Notepad")[0]

# ウィンドウが最小化されていないことを確認
if window.isMinimized:
    window.restore()

# ウィンドウの位置とサイズを取得
left, top, width, height = window.left, window.top, window.width, window.height

# ウィンドウ領域のスクリーンキャプチャ
screenshot = pyautogui.screenshot(region=(left, top, width, height))

# 画像をNumPy配列に変換
screenshot_np = np.array(screenshot)

# 色をBGR形式に変換 (OpenCVはBGRを使用するため)
screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

# OpenCVで画像を表示
cv2.imshow("Window Capture", screenshot_np)
cv2.waitKey(0)  # 任意のキーが押されるまで待機
cv2.destroyAllWindows()
