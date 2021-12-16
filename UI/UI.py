import tkinter as tk
import tkinter.font as tkFont
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
from tkinter import *
from fingers_detection import *

# 해야할 것 - 프레임 배경 색 설정/ opencv 화면과 점수화면 합쳐서 넣기, 문제 출력 

pygame.mixer.init()

def musicplay():
    pygame.mixer.music.load('bgm.mp3')
    pygame.mixer.music.play(loops=0)

def game1musicplay():
    pygame.mixer.music.load('JB.mp3')
    pygame.mixer.music.play(loops=0)

def game2musicplay():
    pygame.mixer.music.load('JJJ.mp3')
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
        #cv()창 실행
        tk.Label(self, text="").pack()
        tk.Button(self, text="Quit", command=lambda: quit(), font=('Arial', 20)).pack()


class startgame2(tk.Frame): #Jar Jar Jar
    def __init__(self, master):
        game2musicplay()
        tk.Frame.__init__(self, master)
        #cv()
        tk.Label(self, text="").pack()
        
        tk.Button(self, text="Quit", command=lambda: quit(), font=('Arial', 20)).pack()


class startgame3(tk.Frame): #Indian
    def __init__(self, master):
        game3musicplay()
        tk.Frame.__init__(self, master)
        #cv()
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
    
    