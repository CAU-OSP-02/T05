class Title_origin(tk):
    def __init__(self):
        label = tk.Label(self, text="숫자송", bg = '#0059b3', fg = "white", font=('Arial', 20))
        label.pack()



button = tk.Button(text = "PLAY", relief=GROOVE, overrelief=RAISED, width = 5 , height = 1, font=('Arial', 10))
button.pack

class Playbutton_origin(tk.frame):
    def __init__(self):
        pygame.mixer.music.load('origin.mp3')
        pygame.mixer.music.play(loop=0)