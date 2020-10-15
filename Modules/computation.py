import numpy as np
import pyautogui as pag

def computeAngle(lefteye,righteye):
    leftEyeCenter = lefteye.mean(axis=0).astype("int")
    rightEyeCenter = righteye.mean(axis=0).astype("int")        
    dY = rightEyeCenter[1] - leftEyeCenter[1]
    dX = rightEyeCenter[0] - leftEyeCenter[0]
    return (np.degrees(np.arctan2(dY, dX))) #- 180

def direction(nose_point,anchor_point,w,h,multiple=1):
    nx,ny=nose_point
    x,y=anchor_point
    if nx>(x+multiple*w):
        return 'right'
    elif nx<(x-multiple*w):
        return 'left'
    if ny>(y+multiple*h):
        return 'down'
    elif ny<(y-multiple*h):
        return 'up'
    return '-'

def MovePointer(move,scroll_mode):
    drag = 18
    if move=='right':
        pag.moveRel(drag,0)
    elif move=='left':
        pag.moveRel(-drag,0)
    elif move=='up':
        if scroll_mode:
            pag.scroll(40)
        else:
            pag.moveRel(0,-drag)
    elif move=='down':
        if scroll_mode:
            pag.scroll(-40)
        else:
            pag.moveRel(0,drag)
           