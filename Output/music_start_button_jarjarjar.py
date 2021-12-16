from tkinter import *
from pygame import mixer

ws = Tk()
ws.geometry("960x480")
ws.title("게임시작 버튼")

def jaljaljal():
    sound = "C:/Users/minja/Desktop/강민재/음악/잘잘잘.wav"
    mixer.init()
    mixer.music.load(sound)
    mixer.music.play()
    

photo = PhotoImage(file="C:/Users/minja/Desktop/강민재/잘잘잘 게임버튼.png")
btn = Button(ws, image=photo,command = jaljaljal)
btn.pack()

ws.mainloop()
