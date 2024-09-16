from mss import mss
import pynput


while True:
    mouse = pynput.mouse.Controller()
    print(mouse.position)