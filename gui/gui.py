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



# 해야할 것 - opencv 화면과 점수화면 합쳐서 넣기, 문제 출력 

pygame.mixer.init()

def musicplay():
    pygame.mixer.music.load('bgm.mp3')
    pygame.mixer.music.play(loops=0)

def game1musicplay():
    pygame.mixer.music.load('origine.mp3')
    pygame.mixer.music.play(loops=0)

def game2musicplay():
    pygame.mixer.music.load('JJJ.mp3')
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
       
        tk.Frame.__init__(self, master)
        
        # 배경 불러오기
        back1 = tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\page\background.png")

        # 배경 배치
        lbl_b1 = Label(image = back1)
        lbl_b1.image = back1
        lbl_b1.place(x = 0, y = 0)
        
        #디자인 용 그림 불러오기
        design1=tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\background design\1.png")
        design2=tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\background design\2.png")
        design3=tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\background design\3.png")
        design4=tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\background design\4.png")
        design5=tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\background design\5.png")
        design6=tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\background design\6.png")
        design7=tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\background design\7.png")
        design8=tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\background design\8.png")
        design9=tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\background design\9.png")
        
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
        text1=tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\text\FNSG.png")
        
        # 텍스트 배치
        lbl_t1 = Label(image = text1, bg = '#F8FFAE')
        lbl_t1.image = text1
        lbl_t1.place(x=90, y=70) 
        
        
        # 버튼 불러오기
        start = tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\btn\game start.png")
        help = tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\btn\help.png")
        setting = tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\btn\setting.png")
        quit = tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\btn\quit.png")
        
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
        back1 = tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\page\background.png")

        # 배경 배치
        lbl_b1 = Label(image = back1)
        lbl_b1.image = back1
        lbl_b1.place(x = 0, y = 0)
        
        # 텍스트 불러오기
        text1=tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\text\t origine.png")
        
        # 텍스트 배치
        lbl_t1 = Label(image = text1, bg = '#F8FFAE')
        lbl_t1.image = text1
        lbl_t1.place(x=90, y=70)
            
        # 버튼 불러오기
        startSong = tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\btn\start song.png")
        back = tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\btn\back.png")
        
        # 버튼 배치
        
        btn1 = Button(image=startSong, bg = '#F8FFAE',
                      command=game1musicplay())
        btn1.image = startSong
        btn1.place(x = 320, y = 230)
        
        btn3 = Button(image=back, bg = '#F8FFAE',
                      command=lambda: master.switch_frame(Start))
        btn3.image = back
        btn3.place(x = 320, y = 430)
        
        


# 잘잘잘 숫자송 버튼을 누르면
class startgame2(tk.Frame): #Jar Jar Jar
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        # 배경 불러오기
        back1 = tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\page\background.png")

        # 배경 배치
        lbl_b1 = Label(image = back1)
        lbl_b1.image = back1
        lbl_b1.place(x = 0, y = 0)
        
        # 텍스트 불러오기
        text1=tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\text\t JJJ.png")
        
        # 텍스트 배치
        lbl_t1 = Label(image = text1, bg = '#F8FFAE')
        lbl_t1.image = text1
        lbl_t1.place(x=90, y=70)
            
        # 버튼 불러오기
        startSong = tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\btn\start song.png")
        back = tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\btn\back.png")
        
        # 버튼 배치
        
        btn1 = Button(image=startSong, bg = '#F8FFAE',
                      command=game2musicplay())
        btn1.image = startSong
        btn1.place(x = 320, y = 230)
        
        btn3 = Button(image=back, bg = '#F8FFAE',
                      command=lambda: master.switch_frame(Start))
        btn3.image = back
        btn3.place(x = 320, y = 430)


# 게임 시작 버튼을 눌렀을 때
class Start(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        # 배경 불러오기
        back2 = tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\page\background2.png")

        # 배경 배치
        lbl_b2 = Label(image = back2)
        lbl_b2.image = back2
        lbl_b2.place(x = 0, y = 0)
        
        # 텍스트 불러오기
        text1=tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\text\GameStart.png")
        
        # 텍스트 배치
        lbl_t1 = Label(image = text1, bg = '#F8FFAE')
        lbl_t1.image = text1
        lbl_t1.place(x=215, y=70) 
        
        # 버튼 불러오기
        Origine = tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\btn\origine.png")
        JarJarJar = tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\btn\JJJ.png")
        back = tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\btn\back.png")
        
        
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
        back2 = tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\page\background2.png")

        # 배경 배치
        lbl_b2 = Label(image = back2)
        lbl_b2.image = back2
        lbl_b2.place(x=0, y=0)
        
        # 텍스트 불러오기
        text1=tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\text\help.png")
        
        # 텍스트 배치
        lbl_t1 = Label(image = text1, bg = '#F8FFAE')
        lbl_t1.image = text1
        lbl_t1.place(x=350, y=70) 
        
        # 버튼 불러오기
        back = tk.PhotoImage(file=r"C:\git_open_02\T05\gui design\btn\back.png")
    
        # 버튼 배치
        btn1 = Button(image=back, bg = '#F8FFAE',
                      command=lambda: master.switch_frame(MainWindow))
        btn1.image = back
        btn1.place(x = 320, y = 430)
        
               
        
# 설정하기 버튼을 누르면        
class Setting(tk.Frame):
    def __init__(self, master):
        
        # 배경 불러오기
        back2 = tk.PhotoImage(file = r"C:\git_open_02\T05\gui design\page\background2.png")

        # 배경 배치
        lbl_b2 = Label(image = back2)
        lbl_b2.image = back2
        lbl_b2.place(x=0, y=0)
        
        # 텍스트 불러오기
        text1=tk.PhotoImage(file = r"C:\git_open_02\T05\gui design\text\setting.png")
        
        # 텍스트 배치
        lbl_t1 = Label(image = text1, bg = '#F8FFAE')
        lbl_t1.image = text1
        lbl_t1.place(x=300, y=70) 
        
        # 버튼 불러오기
        on = tk.PhotoImage(file = r"C:\git_open_02\T05\gui design\btn\on.png")
        off = tk.PhotoImage(file = r"C:\git_open_02\T05\gui design\btn\off.png")
        back = tk.PhotoImage(file = r"C:\git_open_02\T05\gui design\btn\back.png")
        
        
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
