from tkinter import *
from pygame import mixer

ws = Tk()
ws.geometry("960x480")
ws.title("게임시작 버튼")

def jaljaljal():
    sound = "./T05/music/JJJ.wav"
    mixer.init()
    mixer.music.load(sound)
    mixer.music.play()
    

photo = PhotoImage(file="./T05/final/startbutton.png")
btn = Button(ws, image=photo,command = jaljaljal)
btn.pack()
ws.mainloop()
