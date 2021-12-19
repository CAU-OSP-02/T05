import tkinter as tk
import pygame
import sys
import cv2
import mediapipe as mp
import numpy as np
import threading
import datetime
import os
import PIL.Image, PIL.ImageTk
from pygame import mixer
import PIL.Image, PIL.ImageTk
from tkinter import *
from random import *
import time
import math


pygame.mixer.init()

def musicplay():
    pygame.mixer.music.load('bgm.wav')
    pygame.mixer.music.play(loops=0)

def game1musicplay():
    pygame.mixer.music.load('origine.wav')
    pygame.mixer.music.play(loops=0)

def game2musicplay():
    pygame.mixer.music.load('JJJ.wav')
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


#전역변수선언 
result = 0
score = 0
myanswer = None
a = 0

#함수선언
def my_score():
    global score
    global result
    if result == myanswer:
        score += 100
        result = 0


#cv 창       
class Cam(tk.Frame):
    
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.width, self.height = 300,200
        self.master = master
        self.cap = cv2.VideoCapture(0)
        self.ret, self.hand = self.cap.read()
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.canvas = Canvas(master, width = self.width, height = self.height)
        self.canvas.place(x=520, y=210)
        self.delay = 33
        self.update()
        self.detect()
        
    def update(self):
        self.hand = cv2.cvtColor(self.hand, cv2.COLOR_BGR2RGB)
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.hand))
        self.canvas.create_image(0, 0, image = self.photo, anchor = NW)
        self.master.after(self.delay, self.update)
    
    def detect(self):
        global myanswer
        while(self.cap.isOpened()):
            try:             
                
                self.hand=cv2.flip(self.hand,1)
                if self.ret == True:
                    pass

                #making the img of dimension
                self.hand =self.hand[100:700,100:700]
            
                #using hsv we detect the color of skin
                hsv = cv2.cvtColor(self.hand, cv2.COLOR_BGR2HSV)
                lower_skin = np.array([0, 58, 30], dtype = "uint8")
                upper_skin = np.array([33, 255, 255], dtype = "uint8")
            
                #applying mask to extract skin color object from the img
                mask = cv2.inRange(hsv, lower_skin, upper_skin)

                #now we dilate our skin color object to remove black spots or noise from it
                kernel = np.ones((5,5),np.uint8)
                mask = cv2.dilate(mask,kernel,iterations = 3)
                blur = cv2.bilateralFilter(mask,9,200,200)
                res = cv2.bitwise_and(self.hand,self.hand, mask= blur)

                #convert to BGR -> GRAY 
                hand_gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)

                #thresholding the image
                self.ret, thresh = cv2.threshold(hand_gray, 98, 255,cv2.THRESH_TRUNC)
            
                #finding contours in the threshold image
                contours,_ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

                #selecting the contour of max area 
                cnt = max(contours, key = lambda x: cv2.contourArea(x))
            
                hull = cv2.convexHull(cnt)
                hullarea = cv2.contourArea(hull)
                cntarea = cv2.contourArea(cnt)
                x,y,w,h = cv2.boundingRect(hull)
                self.hand = cv2.rectangle(self.hand,(x,y),(x+w,y+h),(0,255,0),2)

                ratio=(hullarea+cntarea)/(hullarea-cntarea)
                print("ratio:",ratio)
                img = cv2.drawContours(self.hand, hull, -2, (0,0,255), 10)
            
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

            except:
                pass

            k = cv2.waitKey(250) & 0xFF
            if k == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()

        

pygame.mixer.init()

def musicplay():
     pygame.mixer.music.load('bgm.mp3')
     pygame.mixer.music.play(loops=0)


def musicstop():
    pygame.mixer.music.stop()



class MainWindow(tk.Frame):
    def __init__(self, master):
       
        tk.Frame.__init__(self, master)
        
        # 배경 불러오기
        back1 = tk.PhotoImage(file="./gui/page/background.png")

        # 배경 배치
        lbl_b1 = Label(image = back1)
        lbl_b1.image = back1
        lbl_b1.place(x = 0, y = 0)
        
        #디자인 용 그림 불러오기
        design1=tk.PhotoImage(file="./background design/1.png")
        design2=tk.PhotoImage(file="./background design/2.png")
        design3=tk.PhotoImage(file="./background design/3.png")
        design4=tk.PhotoImage(file="./background design/4.png")
        design5=tk.PhotoImage(file="./background design/5.png")
        design6=tk.PhotoImage(file="./background design/6.png")
        design7=tk.PhotoImage(file="./background design/7.png")
        design8=tk.PhotoImage(file="./background design/8.png")
        design9=tk.PhotoImage(file="./background design/9.png")
        
        #디자인 용 그림배치
        lbl1 = Label(image=design1, bg = '#F8FFAE')
        lbl1.image = design1
        lbl1.place(x=10, y=200) 
        lbl2 = Label(image=design2, bg = '#F8FFAE')
        lbl2.image = design2
        lbl2.place(x=50, y=400) 
        lbl3 = Label(image=design3, bg = '#F8FFAE')
        lbl3.image = design3
        lbl3.place(x=80, y=300)
        lbl4 = Label(image=design4, bg = '#F8FFAE')
        lbl4.image = design4
        lbl4.place(x=850, y=50)
        lbl5 = Label(image=design5, bg = '#F8FFAE')
        lbl5.image = design5
        lbl5.place(x=700, y=300)
        lbl6 = Label(image=design6, bg = '#F8FFAE')
        lbl6.image = design6
        lbl6.place(x=500, y=100) 
        lbl7 = Label(image=design7, bg = '#F8FFAE')
        lbl7.image = design7
        lbl7.place(x=20, y=0) 
        lbl8 = Label(image=design8, bg = '#F8FFAE')
        lbl8.image = design8
        lbl8.place(x=800, y=400) 
        lbl9 = Label(image=design9, bg = '#F8FFAE')
        lbl9.image = design9
        lbl9.place(x=700, y=50) 
        
        
        # 텍스트 불러오기
        text1=tk.PhotoImage(file="./T05/gui/text/FNSG.png")
        
        # 텍스트 배치
        lbl_t1 = Label(image = text1, bg = '#F8FFAE')
        lbl_t1.image = text1
        lbl_t1.place(x=90, y=70) 
        
        
        # 버튼 불러오기
        start = tk.PhotoImage(file="./T05/gui/btn/game start.png")
        help = tk.PhotoImage(file="./T05/gui/btn/help.png")
        setting = tk.PhotoImage(file="./T05/gui/btn/setting.png")
        quit = tk.PhotoImage(file="./T05/gui/btn/quit.png")
        
        # 버튼 배치
        
         
        btn1 = Button(image=start, bg = '#F8FFAE',
                      command=lambda: master.switch_frame(Start))
        btn1.image = start
        btn1.place(x = 320, y = 230)
        btn2 = Button(image=help, bg = '#F8FFAE',
                      command=lambda: master.switch_frame(Help))
        btn2.image = help
        btn2.place(x = 320, y = 330)
        btn3 = Button(image=setting, bg = '#F8FFAE',
                      command=lambda: master.switch_frame(Setting))
        btn3.image = setting
        btn3.place(x = 320, y = 430)
        btn4 = Button(image=quit, bg = '#F8FFAE',
                      command=lambda: master.switch_frame(quit))
        btn4.image = quit
        btn4.place(x = 320, y = 530)
                   
        
        def quit(self):
            self.destroy()



# 숫자송 버튼을 누르면
class startgame1(tk.Frame): #Jelly bear
    def __init__(self, master):
        
        tk.Frame.__init__(self, master)
        
        # 배경 불러오기
        back1 = tk.PhotoImage(file="./T05/gui/page/background.png")

        # 배경 배치
        lbl_b1 = Label(image = back1)
        lbl_b1.image = back1
        lbl_b1.place(x = 0, y = 0)
        
        # 텍스트 불러오기
        text1=tk.PhotoImage(file="./T05/gui/text/t origine.png")
        
        # 텍스트 배치
        lbl_t1 = Label(image = text1, bg = '#F8FFAE')
        lbl_t1.image = text1
        lbl_t1.place(x=90, y=70)
            
        # 버튼 불러오기
        startSong = tk.PhotoImage(file="./T05/gui/btn/start song.png")
        back = tk.PhotoImage(file="./T05/gui/btn/back.png")
        
        # 버튼 배치
        
        def origine():
            sound = "./T05/music/origine.wav"
            mixer.init()
            mixer.music.load(sound)
            mixer.music.play()
        def music_stop():
            mixer.music.stop()
        
        btn1 = Button(image=startSong, bg = '#F8FFAE',
                      command = lambda:[ master.switch_frame(Cam), origine] )
        btn1.image = startSong
        btn1.place(x = 150, y = 430)
        
        
        btn3 = Button(image=back, bg = '#F8FFAE',
                      command=lambda: [master.switch_frame(Start), music_stop()])
        btn3.image = back
        btn3.place(x = 520, y = 430)
        
 




# 잘잘잘 숫자송 버튼을 누르면
class startgame2(tk.Frame): #Jar Jar Jar
    def __init__(self, master):
        tk.Frame.__init__(self, master)               
        
        # 배경 불러오기
        back1 = tk.PhotoImage(file="./T05/gui/page/background.png")

        # 배경 배치
        lbl_b1 = Label(image = back1)
        lbl_b1.image = back1
        lbl_b1.place(x = 0, y = 0)
        
        # 텍스트 불러오기
        text1=tk.PhotoImage(file="./T05/gui/text/t JJJ.png")
        
        # 텍스트 배치
        lbl_t1 = Label(image = text1, bg = '#F8FFAE')
        lbl_t1.image = text1
        lbl_t1.place(x=90, y=70)
            
        # 버튼 불러오기
        startSong = tk.PhotoImage(file="./T05/gui/btn/start song.png")
        back = tk.PhotoImage(file="./T05/gui/btn/back.png")
        
        # 버튼 배치
        
        
        def jaljaljal():
            sound = "./T05/music/JJJ.wav"
            mixer.init()
            mixer.music.load(sound)
            mixer.music.play()
        def music_stop():
            mixer.music.stop()

        btn1 = Button(image=startSong, bg = '#F8FFAE',
                      command = lambda:[ master.switch_frame(Cam), jaljaljal])
                                        #master.switch_frame(Question)] )
                      
        btn1.image = startSong
        btn1.place(x = 150, y = 430)
        
        
        btn3 = Button(image=back, bg = '#F8FFAE',
                      command=lambda: [master.switch_frame(Start), music_stop()])
        btn3.image = back
        btn3.place(x = 520, y = 430)


# 게임 시작 버튼을 눌렀을 때
class Start(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        # 배경 불러오기
        back2 = tk.PhotoImage(file="./T05/gui/page/background2.png")

        # 배경 배치
        lbl_b2 = Label(image = back2)
        lbl_b2.image = back2
        lbl_b2.place(x = 0, y = 0)
        
        # 텍스트 불러오기
        text1=tk.PhotoImage(file="./T05/gui/text/GameStart.png")
        
        # 텍스트 배치
        lbl_t1 = Label(image = text1, bg = '#F8FFAE')
        lbl_t1.image = text1
        lbl_t1.place(x=215, y=70) 
        
        # 버튼 불러오기
        Origine = tk.PhotoImage(file="./T05/gui/btn/origine.png")
        JarJarJar = tk.PhotoImage(file="./T05/gui/btn/JJJ.png")
        back = tk.PhotoImage(file="./T05/gui/btn/back.png")
        
        
        # 버튼 배치
        
         
        btn1 = Button(image=Origine, bg = '#F8FFAE',
                      command=lambda: master.switch_frame(startgame1))
        btn1.image = Origine
        btn1.place(x = 320, y = 230)
        btn2 = Button(image=JarJarJar, bg = '#F8FFAE',
                      command=lambda: master.switch_frame(startgame2))
        btn2.image = JarJarJar
        btn2.place(x = 320, y = 330)
        btn3 = Button(image=back, bg = '#F8FFAE',
                      command=lambda: master.switch_frame(MainWindow))
        btn3.image = back
        btn3.place(x = 320, y = 430)
        
            
       

# 도움말 버튼을 누르면
class Help(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        # 배경 불러오기
        back2 = tk.PhotoImage(file="./T05/gui/page/background2.png")

        # 배경 배치
        lbl_b2 = Label(image = back2)
        lbl_b2.image = back2
        lbl_b2.place(x=0, y=0)
        
        # 텍스트 불러오기
        text1=tk.PhotoImage(file="./T05/gui/text/help.png")
        
        # 텍스트 배치
        lbl_t1 = Label(image = text1, bg = '#F8FFAE')
        lbl_t1.image = text1
        lbl_t1.place(x=350, y=70) 
        
        # 버튼 불러오기
        back = tk.PhotoImage(file="./T05/gui/btn/back.png")
    
        # 버튼 배치
        btn1 = Button(image=back, bg = '#F8FFAE',
                      command=lambda: master.switch_frame(MainWindow))
        btn1.image = back
        btn1.place(x = 320, y = 430)
        
               
        
# 설정하기 버튼을 누르면        
class Setting(tk.Frame):
    def __init__(self, master):
        
        # 배경 불러오기
        back2 = tk.PhotoImage(file = "./T05/gui/page/background2.png")

        # 배경 배치
        lbl_b2 = Label(image = back2)
        lbl_b2.image = back2
        lbl_b2.place(x=0, y=0)
        
        # 텍스트 불러오기
        text1=tk.PhotoImage(file = "./T05/gui/text/setting.png")
        
        # 텍스트 배치
        lbl_t1 = Label(image = text1, bg = '#F8FFAE')
        lbl_t1.image = text1
        lbl_t1.place(x=300, y=70) 
        
        # 버튼 불러오기
        on = tk.PhotoImage(file = "./T05/gui/btn/on.png")
        off = tk.PhotoImage(file = "./T05/gui/btn/off.png")
        back = tk.PhotoImage(file = "./T05/gui/btn/back.png")
        
        
        # 버튼 배치
        
        btn1 = Button(image=on, bg = '#F8FFAE',
                      command = musicplay)
        btn1.image = on
        btn1.place(x = 255, y = 300)
        btn2 = Button(image=off, bg = '#F8FFAE',
                      command = musicstop)
        btn2.image = off
        btn2.place(x = 495, y = 300)
        btn3 = Button(image=back, bg = '#F8FFAE',
                      command = lambda: master.switch_frame(MainWindow))
        btn3.image = back
        btn3.place(x = 320, y = 430)


if __name__ == "__main__":
    app = App()
    app.configure(bg = '#F8FFAE')
    app.title("FMRG")
    app.geometry('960x640+100+100')
    app.minsize(960,640)
    app.maxsize(960,640)
    app.resizable(False, False)
    app.mainloop()  # 창 유지