import tkinter
from PIL import Image, ImageTk, ImageOps
import time
from random import randint, random

SCALE_FACTOR = 5

root = tkinter.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


bg = Image.open("image.png")

img_width, img_height = bg.size
img_width //= SCALE_FACTOR
img_height //= SCALE_FACTOR

bg = bg.resize((img_width, img_height))
bgL = bg.convert("L")

root.geometry("{}x{}".format(img_width, img_height))
root.overrideredirect(True)

img = ImageTk.PhotoImage(bg)

label1 = tkinter.Label(root, image = img) 
label1.place(x = 0, y = 0)

x = 0
y = 0

# root.?xpos? = randint(0, screen_width - 475)
# root.?ypos? = randint(50, screen_height - 250)

xVel = random()
yVel = random()

while True:
    hits = 0
    
    windowX = root.winfo_x()
    windowY = root.winfo_y()

    if windowX == screen_width - 475:
        xVel = -1
        bg = ImageOps.colorize(bgL, black=(0, 0, 0, 0), white=(randint(0, 255), randint(0, 255), randint(0, 255)))

        img = ImageTk.PhotoImage(bg)

        label1 = tkinter.Label(root, image = img) 
        label1.place(x = 0, y = 0)

        hits += 1

    elif windowX == 0:
        xVel = 1

        bg = ImageOps.colorize(bgL, black=(0, 0, 0, 0), white=(randint(0, 255), randint(0, 255), randint(0, 255)))

        img = ImageTk.PhotoImage(bg)

        label1 = tkinter.Label(root, image = img) 
        label1.place(x = 0, y = 0)

        hits += 1

    if windowY == screen_height - 250:
        yVel = -1

        bg = ImageOps.colorize(bgL, black=(0, 0, 0, 0), white=(randint(0, 255), randint(0, 255), randint(0, 255)))

        img = ImageTk.PhotoImage(bg)

        label1 = tkinter.Label(root, image = img)
        label1.place(x = 0, y = 0)

        hits += 1

    elif windowY == 50:
        yVel = 1

        bg = ImageOps.colorize(bgL, black=(0, 0, 0, 0), white=(randint(0, 255), randint(0, 255), randint(0, 255)))

        img = ImageTk.PhotoImage(bg)

        label1 = tkinter.Label(root, image = img)
        label1.place(x = 0, y = 0)

        hits += 1   

    root.geometry('+{}+{}'.format(int(x), int(y)))

    if (hits >= 2):
        # if it hits the corner, happiness happens
        print("OMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMG")

    root.update()

    x += xVel
    y += yVel

    time.sleep(0.001)
