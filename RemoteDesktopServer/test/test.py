import mss
import mss.tools
import pygetwindow as gw

# キャプチャしたいウィンドウのタイトル
window_title = "OpenXR_Practice - BasicScene - Android - Unity 2022.3.12f1 <DX11>"

import pygetwindow as gw




def get_window_bbox(window_title):
    # ウィンドウを取得
    window = gw.getWindowsWithTitle(window_title)[0]

    offset_x = 10
    offset_width = -20

    offset_y = 2
    offset_height = -10

    left, top, width, height = window.left +  offset_x , window.top  + offset_y, window.width + offset_width, window.height + offset_height

    return {"top": top, "left": left, "width": width, "height": height}






def get_window_name(rough_name = ""):
    # 開いているウィンドウの一覧を取得
    windows = gw.getWindowsWithTitle('')
    output = []
    # 各ウィンドウのタイトルを表示
    for window in windows:
        if rough_name in window.title:
            output.append(window.title)
    
    return output


import numpy as np 
import cv2 





sct = mss.mss() 

print(get_window_name("Unity"))


# while True:
    
#     monitor = get_window_bbox(window_title)
#     screenshot = sct.grab(monitor)
#     img_np = np.array(screenshot)
#     cv2.imshow("data", img_np)

#     if cv2.waitKey(1) == ord("q"):
#         break
    

sct.close() 
cv2.destroyAllWindows()