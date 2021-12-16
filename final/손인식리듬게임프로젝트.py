#모듈
import tkinter as tk
import tkinter.font as tkFont
import pygame
import sys
import cv2
import numpy as np
import threading
import datetime
import os
import PIL.Image, PIL.ImageTk
from pygame import mixer
from tkinter import *
import math
from PIL import Image
import time

#전역변수선언 
result = 0
score = 0
myanswer = None #미사용값
a = 0

#함수선언
def my_score():
    global score
    global result
    if result == myanswer:
        score += 100
        result = 0

def img1():
    global a
    ws = Tk()
    start = time()
    imgObj = PhotoImage(file = "10.png")
    imgLabel = Label(ws, image=imgObj)
    imgLabel.pack()
    ws.after(a, ws.destroy)
    ws.mainloop()
    result = 1

def img2():
    global a
    ws = Tk()
    start = time()
    imgObj = PhotoImage(file = "2.png")
    imgLabel = Label(ws, image=imgObj)
    imgLabel.pack()
    ws.after(a, ws.destroy)
    ws.mainloop()
    result = 2

def img3():
    global a
    ws = Tk()
    start = time()
    imgObj = PhotoImage(file = "3.png")
    imgLabel = Label(ws, image=imgObj)
    imgLabel.pack()
    ws.after(a, ws.destroy)
    ws.mainloop()
    result = 3

def img4():
    global a
    ws = Tk()
    start = time()
    imgObj = PhotoImage(file = "4.png")
    imgLabel = Label(ws, image=imgObj)
    imgLabel.pack()
    ws.after(a, ws.destroy)
    ws.mainloop()
    result = 4

def img5():
    global a
    ws = Tk()
    start = time()
    imgObj = PhotoImage(file = "5.png")
    imgLabel = Label(ws, image=imgObj)
    imgLabel.pack()
    ws.after(a, ws.destroy)
    ws.mainloop()
    result = 5

def img6():
    global a
    ws = Tk()
    start = time()
    imgObj = PhotoImage(file = "6.png")
    imgLabel = Label(ws, image=imgObj)
    imgLabel.pack()
    ws.after(a, ws.destroy)
    ws.mainloop()
    result = 6

def img7():
    global a
    ws = Tk()
    start = time()
    imgObj = PhotoImage(file = "7.png")
    imgLabel = Label(ws, image=imgObj)
    imgLabel.pack()
    ws.after(a, ws.destroy)
    ws.mainloop()
    result = 7

def img8():
    global a
    ws = Tk()
    start = time()
    imgObj = PhotoImage(file = "8.png")
    imgLabel = Label(ws, image=imgObj)
    imgLabel.pack()
    ws.after(a, ws.destroy)
    ws.mainloop()
    result = 8

def img9():
    global a
    ws = Tk()
    start = time()
    imgObj = PhotoImage(file = "9.png")
    imgLabel = Label(ws, image=imgObj)
    imgLabel.pack()
    ws.after(a, ws.destroy)
    ws.mainloop()
    result = 9

def img10():
    global a
    ws = Tk()
    start = time()
    imgObj = PhotoImage(file = "10.png")
    imgLabel = Label(ws, image=imgObj)
    imgLabel.pack()
    ws.after(a, ws.destroy)
    ws.mainloop()
    result = 10

class Cam:
    def __init__(self, window):
        self.width, self.height = 300,200
        self.window = window
        self.window.geometry("960x640")
        self.window.title("Tkinter + OpenCV")
        self.detect()
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.canvas = Canvas(window, width = self.width, height = self.height)
        self.canvas.pack()
        self.canvas_on_down = False
        self.delay = 33
        self.update()
        self.window.mainloop()

    def update(self):
        ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if self.canvas_on_down == True:
            frame = cv2.rectangle(frame)
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self.canvas.create_image(0, 0, image = self.photo, anchor = NW)
        self.window.after(self.delay, self.update)

    def detect(self):
    
        #capturing the video
        cap = cv2.VideoCapture(0)
        global myanswer

        while(cap.isOpened()):
            try:             
                ret, hand = cap.read()
                hand=cv2.flip(hand,1)
                if ret == True:
                    pass

                #making the img of dimension
                hand =hand[100:700,100:700]
            
                #using hsv we detect the color of skin
                hsv = cv2.cvtColor(hand, cv2.COLOR_BGR2HSV)
                lower_skin = np.array([0, 58, 30], dtype = "uint8")
                upper_skin = np.array([33, 255, 255], dtype = "uint8")
            
                #applying mask to extract skin color object from the img
                mask = cv2.inRange(hsv, lower_skin, upper_skin)

                #now we dilate our skin color object to remove black spots or noise from it
                kernel = np.ones((5,5),np.uint8)
                mask = cv2.dilate(mask,kernel,iterations = 3)
                blur = cv2.bilateralFilter(mask,9,200,200)
                res = cv2.bitwise_and(hand,hand, mask= blur)

                #convert to BGR -> GRAY 
                hand_gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)

                #thresholding the image
                ret, thresh = cv2.threshold(hand_gray, 98, 255,cv2.THRESH_TRUNC)
            
                #finding contours in the threshold image
                contours,_ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

                #selecting the contour of max area 
                cnt = max(contours, key = lambda x: cv2.contourArea(x))
            
                hull = cv2.convexHull(cnt)
                hullarea = cv2.contourArea(hull)
                cntarea = cv2.contourArea(cnt)
                x,y,w,h = cv2.boundingRect(hull)
                hand = cv2.rectangle(hand,(x,y),(x+w,y+h),(0,255,0),2)

                ratio=(hullarea+cntarea)/(hullarea-cntarea)
                print("ratio:",ratio)
                img = cv2.drawContours(hand, hull, -2, (0,0,255), 10)
            
                if len(contours) > 0:
                    hull = cv2.convexHull(cnt, returnPoints=False)
                    defects = cv2.convexityDefects(cnt, hull)
                    count_defects = 0
                                
                    for i in range(defects.shape[0]):
                        s,e,f,d = defects[i,0]
                        start = tuple(cnt[s][0])
                        end = tuple(cnt[e][0])
                        far = tuple(cnt[f][0])
                        cv2.circle(img,far,5,[0,0,255],-1)
                        cv2.line(img,start,end,[255,0,0],2)
                        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                        #find the angles between the sides of triangle
                        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57.295
                        if angle <= 90:
                            count_defects += 1
                            print("angle:",count_defects)

                    # hand gestures and display the result            
                    if count_defects == 0 :
                        if 9<ratio<11: #Gesture 1
                            myanswer = 1
                            my_score()
                            
                        elif 5<ratio<12: #Gesture 6
                            myanswer = 6
                            my_score()

                        elif 12<ratio<15: #Gesture 0
                            myanswer = 10
                            my_score()

                        elif 15 <ratio <30: #Gesture 9
                            myanswer = 9
                            my_score()

                    elif count_defects == 1 :
                        if 7<ratio<10: #Gesture 2
                            myanswer = 2
                            my_score()
                                
                        elif 4<ratio <8 : #Gesture 7
                            myanswer = 7
                            my_score()

                    elif count_defects == 2:
                        if ratio<10: #Gesture 8
                            myanswer = 8
                            my_score()

                        elif 6<ratio<11: #Gesture 3
                            myanswer = 3
                            my_score()
                
                    elif count_defects == 3: #Gesture 4
                            myanswer = 4
                            my_score()

                    elif count_defects == 4: #Gesture 5
                            myanswer = 5
                            my_score()
                
                    cv2.imshow('hand',hand)

            except:
                pass

            k = cv2.waitKey(250) & 0xFF
            if k == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

pygame.mixer.init()

def musicplay():
     pygame.mixer.music.load('bgm.mp3')
     pygame.mixer.music.play(loops=0)

def game1musicplay():
     pygame.mixer.music.load('JB.mp3')
     pygame.mixer.music.play(loops=0)

def game2musicplay():
    pygame.mixer.music.load('JJJ.MP3')
    pygame.mixer.music.play(loops=0)

def game3musicplay():
    pygame.mixer.music.load('I.mp3')
    pygame.mixer.music.play(loops=0)

def musicstop():
    pygame.mixer.music.stop()


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame= None
        self.switch_frame(MainWindow)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
           self._frame.destroy()
        self._frame = new_frame #기존 프레임 제거
        self._frame.pack() #전달받은 새로운 프레임을 화면에 출력

class MainWindow(tk.Frame):
    def __init__(self, master):
        self.width, self.height = 100,100
        tk.Frame.__init__(self, master)
        tk.Label(self, text="\n\nFingers Matching Rhythm game\n",
                 bg = '#0059b3', fg = "white", font=('Arial', 40)).pack()
        tk.Button(self, text= "Game Start",
                  command=lambda: master.switch_frame(Start), width = 10 , height = 1, font=('Arial', 20)).pack()
        tk.Label(self, text="",bg = '#0059b3').pack()
        tk.Button(self, text="Help",
                  command=lambda: master.switch_frame(Help), width = 10 , height = 1, font=('Arial', 20)).pack()
        tk.Label(self, text="",bg = '#0059b3').pack()
        tk.Button(self, text="Setting",
                  command=lambda: master.switch_frame(Setting), width = 10 , height = 1, font=('Arial', 20)).pack()
        tk.Label(self, text="",bg = '#0059b3').pack()
        tk.Button(self, text="Quit",
                  command=lambda: master.switch_frame(quit), width = 10 , height = 1, font=('Arial', 20)).pack()
        
        def quit(self):
            self.destroy()
            

    
class startgame1(tk.Frame): #Jelly bear
    def __init__(self, master):
        game1musicplay()
        tk.Frame.__init__(self, master)
        #화면 스위치
        Cam(Tk()) 
        tk.Label(self, text="").pack()
        tk.Button(self, text="Quit", command=lambda: quit(), font=('Arial', 20)).pack()


class startgame2(tk.Frame): #Jar Jar Jar
    def __init__(self, master):
        game2musicplay()
        tk.Frame.__init__(self, master)
        #화면 스위치
        Cam(Tk())
        tk.Label(self, text="").pack()
        tk.Button(self, text="Quit", command=lambda: quit(), font=('Arial', 20)).pack()



class Start(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="\n\nS T A R T\n", background = '#0059b3', foreground = "white", font=('Arial', 50)).pack()
        tk.Button(self, text="Jelly bear",
                  command=lambda: master.switch_frame(startgame1), width = 10 , height = 1, font=('Arial', 20)).pack()
        tk.Label(self, text="").pack()
        tk.Button(self, text="Jar Jar Jar",
                  command=lambda: master.switch_frame(startgame2), width = 10 , height = 1, font=('Arial', 20)).pack()
        tk.Label(self, text="").pack()
        tk.Button(self, text="Indian",
                  command=lambda: master.switch_frame(startgame3), width = 10 , height = 1, font=('Arial', 20)).pack()
        tk.Label(self, text="").pack()
        tk.Button(self, text="Back",
                  command=lambda: master.switch_frame(MainWindow), font=('Arial', 20)).pack()


class Help(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="\n\nHelp\n", font=('Arial', 60), background = '#0059b3', foreground = "white").pack()
        tk.Label(self, text="Game Rule", font=('Arial', 25)).pack()
        # 게임설명 관련 라벨텍스트 추가
        tk.Button(self, text="Back",
                  command=lambda: master.switch_frame(MainWindow),font=('Arial', 20)).pack()

class Setting(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        app.attributes("-fullscreen", False)
        tk.Label(self, text="\n\nSetting\n", background = '#0059b3', foreground = "white", font=('Arial', 50)).pack()
        
        tk.Label(self, text="Music", font=('Arial', 25)).pack()
        tk.Button(self, text="On",
                  command=musicplay,font=('Arial', 20), width = 10 , height = 1).pack()
        tk.Button(self, text="Off",
                  command=musicstop,font=('Arial', 20), width = 10 , height = 1).pack()
        tk.Label(self, text="").pack()
        tk.Button(self, text="Back",
                  command=lambda: master.switch_frame(MainWindow),font=('Arial', 20)).pack()



if __name__ == "__main__":
    app = App()
    app['bg'] = '#0059b3'
    app.title("FMRG")
    app.geometry('960x640+100+100')
    app.minsize(960,640)
    app.maxsize(960,640)
    app.resizable(False, False)
    app.mainloop()