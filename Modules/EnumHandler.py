import win32api
import win32gui
import win32con

def enumHandler(hwnd, lParam):
    xpos = 2
    ypos = 2
    width = 1361
    length = 648
    appname='On-Screen Keyboard'
    framename='Frame'
    rightclick='Program Manager'
    appname1='Control apps OpenCv'
    if win32gui.IsWindowVisible(hwnd):
        if appname not in win32gui.GetWindowText(hwnd):
            if framename not in win32gui.GetWindowText(hwnd):
                if rightclick not in win32gui.GetWindowText(hwnd):
                    if appname1 not in win32gui.GetWindowText(hwnd):
                        if "Recording" not in win32gui.GetWindowText(hwnd):
                            if "Recorder" not in win32gui.GetWindowText(hwnd):
                                if "Camtasia" not in win32gui.GetWindowText(hwnd):
                                    if "Selection" not in win32gui.GetWindowText(hwnd):
                                        if win32gui.GetWindowText(hwnd)!='':                            
                                            win32gui.MoveWindow(hwnd, xpos, ypos, width, length, True)