import os
import pygame.mixer, pygame.time
import pyautogui as pag
import webbrowser

def Quit():
    sound()
    os._exit(0)
def speech_open():
    sound()
    pag.hotkey('win','ctrl','s')    
    pag.moveTo(833,38)
def vlc_open():
    sound()
   #os.startfile('C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe')
    webbrowser.open_new_tab('http://www.gaana.com/')
def notepad_open():
    sound()
    os.startfile('C:\\windows\\system32\\notepad.exe')
def movies_open():
    sound()
    os.startfile('E:\Movies')
def desktop_open():
    sound()
    os.startfile('C:\\Users\\Sundara Ganpathy L\\Desktop')
def chrome_open():
    sound()
    os.startfile('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')

def cortanaOpen():
    os.system("TASKKILL /F /IM osk.exe")
    pag.keyDown('win')
    pag.press('c')
    pag.keyUp('win')
    sound()

def sound():
    mixer = pygame.mixer
    time = pygame.time
    file_path="sound//beep-02.wav"
    mixer.init(11025) #raises exception on fail
    sound = mixer.Sound(file_path)
    channel = sound.play()