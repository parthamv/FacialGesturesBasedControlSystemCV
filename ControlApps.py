from imutils import face_utils
import numpy as np
import pyautogui as pag
import imutils
import dlib
from Modules import EnumHandler,LandMark,computation,Requirments,UserInterface
import cv2
import win32api
import win32gui
import win32con
import psutil
import os
import sys
import threading
import time
import tkinter as tk
import pygame.mixer, pygame.time
import webbrowser

root = tk.Tk()
                     
def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():        
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():                
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False



def start():
    mouth_threash=0.3
    mouth_frames=10
    eye_threash=0.25
    eye_frames=10
    wink_diff_threash=0.02
    wink_close_threash=0.20
    wink_frames=10
    angle_frames=10
    mouth_counter=0
    eye_counter=0
    angle_counter=0
    wink_counter=0
    input_mode_type=0 
    input_mode=False
    eye_click=False
    left_wink=False
    right_wink=False
    scroll_mode=False
    anchor_point=(0,0)
    yellow=(0,255,255)
    red=(0,0,255)
    green=(0,255,0)
    black=(0,0,0)
    
    pag.FAILSAFE = True

    shape_predictor = "shape_predictor_68_face_landmarks.dat"
    detector=dlib.get_frontal_face_detector()
    predictor=dlib.shape_predictor(shape_predictor)

    (lstart,lend)=face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rstart,rend)=face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    (nstart,nend)=face_utils.FACIAL_LANDMARKS_IDXS["nose"]
    (mstart,mend)=face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

    vid=cv2.VideoCapture(0)
    resolution_w=1366
    resolution_h=768
    cam_w=720
    cam_h=720
    unit_w=resolution_w/cam_w
    unit_h=resolution_h/cam_h

    while True:
        _,frame=vid.read()
        frame=cv2.flip(frame,1)
        frame=imutils.resize(frame,width=cam_w,height=cam_h)
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        rects=detector(gray,0)

        if len(rects)>0:
            rect=rects[0]
        else:
            cv2.imshow("Frame",frame)
            key=cv2.waitKey(1) & 0xFF
            continue

        shape=predictor(gray,rect)
        shape=face_utils.shape_to_np(shape)

        mouth=shape[mstart:mend]
        lefteye=shape[lstart:lend]
        righteye=shape[rstart:rend]
        nose=shape[nstart:nend]

        #cam frames are flipped so left = right and right = left
        temp=lefteye
        lefteye=righteye
        righteye=temp

        mar=LandMark.mouth_aspect_ratio(mouth)
        leftear=LandMark.eye_aspect_ratio(lefteye)
        rightear=LandMark.eye_aspect_ratio(righteye)
        ear=(leftear+rightear)/2.0
        diff_ear=np.abs(leftear-rightear)

        nose_point=(nose[3,0],nose[3,1])

        mouthhull=cv2.convexHull(mouth)
        lefteyehull=cv2.convexHull(lefteye)
        righteyehull=cv2.convexHull(righteye)
        cv2.drawContours(frame,[mouthhull],-1,black,1)
        cv2.drawContours(frame,[lefteyehull],-1,black,1)
        cv2.drawContours(frame,[righteyehull],-1,black,1)

        # compute the angle between the eye centroids
        angle = computation.computeAngle(lefteye,righteye)
        
        # for (x,y) in np.concatenate((mouth,lefteye,righteye),axis=0):
        #     cv2.circle(frame,(x,y),2,red,-1)        
        
        if mar>mouth_threash:
            mouth_counter+=1
            if mouth_counter>=mouth_frames:
                #input_mode=not input_mode
                if(input_mode_type==0):
                    input_mode_type=1
                    mouth_counter=0
                    anchor_point=nose_point
                elif(input_mode_type==1):
                    input_mode_type=2
                    mouth_counter=0
                    anchor_point=nose_point
                elif(input_mode_type==2):
                    input_mode_type=3
                    mouth_counter=0
                    anchor_point=nose_point
                elif(input_mode_type==3):
                    input_mode_type=0
                    mouth_counter=0
                    anchor_point=nose_point
                scroll_mode=False
                Requirments.sound()
        else:
            mouth_counter=0

        hcruc_x,hcruc_y=win32api.GetCursorPos()
        flags, hcursor, (hcruc_x,hcruc_y) = win32gui.GetCursorInfo()    
        
        s1=" "
        s2=" "
        flag=0

        s1=win32gui.GetWindowText(win32gui.GetForegroundWindow())
                
        if(s1 != s2):
            flag=0
            s2=s1

        f=0
        f1=0
        f2=0
        f3=0
        f=s1.find("Notepad")
        f1=s1.find("WordPad") 
        f2=s1.find("VLC")
        f3=s1.find("Chrome")

        keyboard_input=0

        if input_mode_type==1:  
            cv2.putText(frame,"APPLICATION MODE",(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,yellow,2)
            x,y=anchor_point
            nx,ny=nose_point
            w,h=60,35
            multiple=1
            cv2.rectangle(frame,(x-w,y-h),(x+w,y+h),green,2)
            cv2.line(frame,anchor_point,nose_point,red,2)

            move=computation.direction(nose_point,anchor_point,w,h)
            #cv2.putText(frame,move.upper(),(10,90), cv2.FONT_HERSHEY_SIMPLEX,0.7,red,2)
            drag=18
            if(f2>0):
                cv2.putText(frame,"VLC MEDIA PLAYER",(10,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,yellow,2)
                #print(angle)
                if(angle>=25):
                    angle_counter+=1
                    if(angle_counter>angle_frames):
                        cv2.putText(frame,"FORWARD",(10,90), cv2.FONT_HERSHEY_SIMPLEX,0.7,red,2)
                        pag.hotkey('ctrl', 'right')
                                                                      
                elif(angle<=-25):
                     angle_counter+=1
                     if(angle_counter>angle_frames):
                         cv2.putText(frame,"REWIND",(10,90), cv2.FONT_HERSHEY_SIMPLEX,0.7,red,2)
                         pag.hotkey('ctrl', 'left')
                else:
                    angle_counter=0
                    
                if diff_ear>wink_diff_threash:
                    if leftear<rightear:
                        if leftear<eye_threash:
                            wink_counter+=1                    
                            if wink_counter>wink_frames:
                                wink_counter=0
                    elif rightear<leftear:
                        if rightear<eye_threash:
                            wink_counter+=1
                            if wink_counter>wink_frames:
                                cv2.putText(frame,"VOLUME UP/DOWN",(10,90), cv2.FONT_HERSHEY_SIMPLEX,0.7,red,2)
                                if move=='up':
                                    pag.hotkey('ctrl', 'up')
                                    wink_counter=0                    
                                elif move=='down':
                                    pag.hotkey('ctrl', 'down')
                                    wink_counter=0
                    else:
                        wink_counter=0
                else:
                    if ear<eye_threash:
                        eye_counter+=1
                        if eye_counter>eye_frames:
                            pag.typewrite(['space'], 0.2)
                            eye_counter=0
                            Requirments.sound()
                    else:
                        eye_counter=0
                        wink_counter=0
            if(f>0 or f1>0):
                keyboard_input=1
                if not checkIfProcessRunning('osk'):
                    flag=1
                    #time.sleep(2)
                    os.startfile('C:\\Windows\\system32\\osk.exe')
                    pag.moveTo(537,897)
                cv2.putText(frame,"TYPING MODE",(10,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,yellow,2)

                #print(angle)
                if(angle>=25):
                    angle_counter+=1
                    if(angle_counter>angle_frames):                    
                        pag.press('backspace',interval=0.30)                                                              
                else:
                    angle_counter=0
                
                if diff_ear>wink_diff_threash:
                    if leftear<rightear:
                        if leftear<eye_threash:
                            wink_counter+=1
                            if wink_counter>wink_frames:
                                pag.click(button='left')
                                wink_counter=0
                                if(hcursor==65541):
                                    os.startfile('C:\\Windows\\system32\\osk.exe')
                                    pag.moveTo(537,897)
                    elif leftear>rightear:
                        if rightear<eye_threash:
                            wink_counter+=1
                            if wink_counter>wink_frames:
                                pag.click(button='right')
                                wink_counter=0
                    else:
                        wink_counter=0
                #for scroll mode
                else:
                    if ear<=eye_threash:
                        eye_counter+=1
                        if eye_counter>eye_frames:
                            pag.moveTo(81,704)
                    else:
                        eye_counter=0
                        wink_counter=0
                                        
                #to move the pointer
                computation.MovePointer(move,scroll_mode)
                
            if(f3>0):
                cv2.putText(frame,"CHROME MODE",(10,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,yellow,2)
                if not checkIfProcessRunning('osk'):
                    os.startfile('C:\\Windows\\system32\\osk.exe')
                    pag.moveTo(537,897)

                #print(angle)
                if(angle>=25):
                    angle_counter+=1
                    if(angle_counter>angle_frames):
                        pag.press('backspace',interval=0.30)                                                
                elif(angle<=-25):
                     angle_counter+=1
                     if(angle_counter>angle_frames):                    
                        pag.keyDown('ctrl')
                        pag.press('t')
                        pag.keyUp('ctrl')
                else:
                    angle_counter=0
                
                hcruc_x,hcruc_y=win32api.GetCursorPos()
                flags, hcursor, (hcruc_x,hcruc_y) = win32gui.GetCursorInfo()
                #for left and right clicks
                if diff_ear>wink_diff_threash:
                    if leftear<rightear:
                        if leftear<eye_threash:
                            wink_counter+=1
                            if wink_counter>wink_frames:
                                pag.click(button='left')
                                wink_counter=0
                                if(hcursor==65541):
                                    os.startfile('C:\\Windows\\system32\\osk.exe')
                                    pag.moveTo(537,897)  
                                if(move=='right'):
                                    pag.keyDown('ctrl')
                                    pag.press('w')
                                    pag.keyUp('ctrl')
                    elif leftear>rightear:
                        if rightear<eye_threash:
                            wink_counter+=1
                            if wink_counter>wink_frames:
                                pag.click(button='right')
                                wink_counter=0
                    else:
                        wink_counter=0
                #for scroll mode
                else:
                    if ear<=eye_threash:
                        eye_counter+=1
                        if eye_counter>eye_frames:
                            scroll_mode=not scroll_mode
                            eye_counter=0
                            Requirments.sound()
                    else:
                        eye_counter=0
                        wink_counter=0

                #to move the pointer
                computation.MovePointer(move,scroll_mode)
                
                if scroll_mode:                    
                    cv2.putText(frame, 'SCROLL MODE IS ON!', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, red, 2)             

        if input_mode_type==2:
            cv2.putText(frame,"Mouse Pointer Mode!",(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,yellow,2)
            x,y=anchor_point
            nx,ny=nose_point
            w,h=60,35
            multiple=1
            cv2.rectangle(frame,(x-w,y-h),(x+w,y+h),green,2)
            cv2.line(frame,anchor_point,nose_point,red,2)

            move=computation.direction(nose_point,anchor_point,w,h)
            cv2.putText(frame,move.upper(),(10,90), cv2.FONT_HERSHEY_SIMPLEX,0.7,red,2)
            drag=18

            hcruc_x,hcruc_y=win32api.GetCursorPos()
            flags, hcursor, (hcruc_x,hcruc_y) = win32gui.GetCursorInfo()
            #for left and right clicks
            if diff_ear>wink_diff_threash:
                if leftear<rightear:
                    if leftear<eye_threash:
                        wink_counter+=1
                        if wink_counter>wink_frames:
                            pag.click(button='left')
                            wink_counter=0
                            if(hcursor==65541):
                                os.startfile('C:\\Windows\\system32\\osk.exe')
                                pag.moveTo(537,897)
                elif leftear>rightear:
                    if rightear<eye_threash:
                        wink_counter+=1
                        if wink_counter>wink_frames:
                            pag.click(button='right')
                            wink_counter=0
                else:
                    wink_counter=0
            #for scroll mode
            else:
                if ear<=eye_threash:
                    eye_counter+=1
                    if eye_counter>eye_frames:
                        scroll_mode=not scroll_mode
                        eye_counter=0
                        Requirments.sound()
                else:
                    eye_counter=0
                    wink_counter=0

            #to move the pointer
            computation.MovePointer(move,scroll_mode)
            
            if scroll_mode:                
                cv2.putText(frame, 'SCROLL MODE IS ON!', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, red, 2)                

            #end of input mode 2 #mouse pointer mode

            #Input mode 3 #Easy access mode
        elif input_mode_type==3:
            cv2.putText(frame,"Easy Access Mode",(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,yellow,2)
            x,y=anchor_point
            nx,ny=nose_point
            w,h=60,35
            multiple=1
            cv2.rectangle(frame,(x-w,y-h),(x+w,y+h),green,2)
            cv2.line(frame,anchor_point,nose_point,red,2)

            move=computation.direction(nose_point,anchor_point,w,h)
            cv2.putText(frame,move.upper(),(10,90), cv2.FONT_HERSHEY_SIMPLEX,0.7,red,2)
            drag=18

            hcruc_x,hcruc_y=win32api.GetCursorPos()
            flags, hcursor, (hcruc_x,hcruc_y) = win32gui.GetCursorInfo()

            if(angle>=25):                
                angle_counter+=1
                if(angle_counter>angle_frames):                       
                    current=win32gui.GetWindowText(win32gui.GetForegroundWindow())                    
                    if(current!='Control apps OpenCv'):                              
                        cmd=current.find('Command')
                        if(cmd<0):
                            pag.keyDown('alt')
                            pag.press('f4',interval=0.5)
                            pag.keyUp('alt')
            elif(angle<=-25):
                    angle_counter+=1
                    if(angle_counter>angle_frames):                                        
                        pag.keyDown('win')
                        pag.press('tab',interval=0.5)
                        pag.keyUp('win')
            else:
                angle_counter=0

            #for left and right clicks
            if diff_ear>wink_diff_threash:
                if leftear<rightear:
                    if leftear<eye_threash:
                        wink_counter+=1
                        if wink_counter>wink_frames:
                            pag.click(button='left')
                            wink_counter=0
                            if(hcursor==65541):
                                os.startfile('C:\\Windows\\system32\\osk.exe')
                                pag.moveTo(537,897)
                elif leftear>rightear:
                    if rightear<eye_threash:
                        wink_counter+=1
                        if wink_counter>wink_frames:
                            pag.click(button='right')
                            wink_counter=0
                else:
                    wink_counter=0
            #for cortana
            else:
                eth=0.20
                if ear<=eth:
                    eye_counter+=1
                    if eye_counter>eye_frames:
                        Requirments.cortanaOpen()
                        eye_counter=0
                else:
                    eye_counter=0
                    wink_counter=0

            #to move the pointer
            computation.MovePointer(move,scroll_mode)             
          
        #win32gui.EnumWindows(EnumHandler.enumHandler, None)
        winname="Frame"
        cv2.namedWindow(winname)
        cv2.moveWindow(winname,1365,3)
        cv2.resizeWindow(winname,550,460)
        cv2.imshow(winname,frame)
        key=cv2.waitKey(1) & 0xFF

        if key==27:
            break

    cv2.destroyAllWindows()
    vid.release()

def start_thread():
    start_button.config(state="disable")
    threads=[]
    t = threading.Thread(target=start)
    threads.append(t)
    t.start()

    
frame = tk.Frame(root)
frame.pack()
root.title("Control apps OpenCv")
root.geometry("500x400+1400+500")
root.overrideredirect(True)

speech_button=tk.Button(root)
speech_img=tk.PhotoImage(file="images//speech.png")
speech_button.config(image=speech_img,width="100",height="80",command=Requirments.speech_open)
speech_button.place(x=50,y=20)

start_button = tk.Button(root,
                   text="Start",
                   command=start_thread,
                   height=3,
                   width=15)
start_button.place(x=190,y=20)

quit_button = tk.Button(root, 
                   text="Quit", 
                   fg="red",
                   command=Requirments.Quit,
                   height=3,
                   width=15)
quit_button.place(x=350,y=20)

b = UserInterface.createSpotify(root) #vlc_button

c = UserInterface.createNotepad(root) #notepad_button

e = UserInterface.createChrome(root) #chrome

d = UserInterface.createMovies(root) #Folder for Movies

f = UserInterface.createDesktop(root) #Folder for Desktop

g  =UserInterface.createAdd(root) #Folder for Add
root.mainloop()