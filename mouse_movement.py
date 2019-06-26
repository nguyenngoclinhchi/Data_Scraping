from pynput.mouse import Button, Controller
import pyautogui

def main():
    mouse = Controller()
    print(mouse.position)
    print(pyautogui.size())
    width, height = pyautogui.size()
    # moving the mouse
    for i in range(20):
        pyautogui.moveTo(100, 100, duration = 0.25)
        pyautogui.moveTo(200, 100, duration = 0.25)
        pyautogui.moveTo(300, 100, duration = 0.25)
        pyautogui.moveTo(400, 100, duration = 0.25)

if __name__ == '__main__':
    main()


