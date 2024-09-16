import asyncio
import json
import math
import websockets
import win32api
import win32con
import pyautogui as pag
from data_monitor import MonitorManager



def move_cursor_to_position(input_data):
    monitor_id = input_data.get("monitor_id")
    monitor = MonitorManager.get_monitors(monitor_id)
    cursor_position = input_data.get("position")
    
    # Use cached monitor to move the cursor
    if(monitor["monitor_type"] == "window"):
        width = monitor["monitor"].width
        height = monitor["monitor"].height
        left = monitor["monitor"].left  # Added this line to define 'left'
        top = monitor["monitor"].top
    else:
        width = monitor["monitor"]['width'] 
        height = monitor["monitor"]['height']
        left = monitor["monitor"]['left']
        top = monitor["monitor"]['top']
    
    # Convert relative position to pixel position
    pixel_x = left + int(width * cursor_position['x'])
    pixel_y = top + int(height * (1 - cursor_position['y']))
    
    # Move the cursor to the calculated position
    win32api.SetCursorPos((pixel_x, pixel_y))





def click_cursor(input_data):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def double_click(input_data):
    click_cursor(input_data)
    click_cursor(input_data)


def right_click(input_data):
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)



def mouse_press(input_data):
    if input_data.get("value"):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        
    else:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        






def scroll_wheel(input_data):

    base_scroll_value = 120  
    
   
    value = input_data.get("value")
    

    if value >= 0:
        scroll_value = int(base_scroll_value * (1 + math.pow(value, 2)))  
    else:
        scroll_value = int(base_scroll_value * (1 + math.pow(abs(value), 2))) * -1  
  
 
    

    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, scroll_value, 0)




def go_back(input_data):
   
    pag.hotkey("alt", "left")

def go_forward(input_data):
  
    pag.hotkey("alt", "right")
    



function_mapping = {
    "cursor": move_cursor_to_position,
    "click": click_cursor,
    "double_click": double_click,
    "mouse_press": mouse_press,
    "right_click": right_click,
    "scroll": scroll_wheel,
    "go_back": go_back,
    "go_forward": go_forward        
    
}


async def handle_input(websocket):
    try: 
        async for message in websocket:
            json_message = json.loads(message)
            print(json_message )
            call_back = function_mapping.get(json_message.get("type"))
            if(call_back):
                call_back(json_message)
            

            



            
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Client disconnected. Exception: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
