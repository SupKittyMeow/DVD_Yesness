import tkinter
from PIL import Image, ImageTk, ImageOps
import time
import random

class DVD():
    def __init__(self):
        SCALE_FACTOR = 10
        MULTIPLIER = 0.4

        root = tkinter.Tk()

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()


        bg = Image.open("src/DVD_Yesness/image.png")

        img_width, img_height = bg.size
        img_width //= SCALE_FACTOR
        img_height //= SCALE_FACTOR

        root.geometry("{}x{}+{}+{}".format(img_width, img_height, screen_width // 2, screen_height // 2))
        x = screen_width // 2
        y = screen_height // 2

        bg = bg.resize((img_width, img_height))
        bgL = bg.convert("L")

        root.overrideredirect(True)

        img = ImageTk.PhotoImage(bg)

        label1 = tkinter.Label(root, image = img) 
        label1.place(x = 0, y = 0)

        if (random.randint(0, 1) == 0):
            xVel = MULTIPLIER
        else:
            xVel = -MULTIPLIER

        if (random.randint(0, 1) == 0):
            yVel = MULTIPLIER
        else:
            yVel = -MULTIPLIER

        def randColor():
            newImg = Image.new('RGB', (img_width, img_height), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            return Image.composite(newImg, bg, bgL)
            # return ImageOps.colorize(bgL, black=(0, 0, 0, 0), white=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))


        while True:
            hits = 0

            if x >= screen_width - img_width:
                xVel = -xVel
                bg = randColor()

                img = ImageTk.PhotoImage(bg)

                label1 = tkinter.Label(root, image = img) 
                label1.place(x = 0, y = 0)

                hits += 1

            elif x <= 0:
                xVel = -xVel

                bg = randColor()

                img = ImageTk.PhotoImage(bg)

                label1 = tkinter.Label(root, image = img) 
                label1.place(x = 0, y = 0)

                hits += 1

            if y >= screen_height - img_height:
                yVel = -yVel

                bg = randColor()

                img = ImageTk.PhotoImage(bg)

                label1 = tkinter.Label(root, image = img)
                label1.place(x = 0, y = 0)

                hits += 1

            elif y <= 0:
                yVel = -yVel

                bg = randColor()

                img = ImageTk.PhotoImage(bg)

                label1 = tkinter.Label(root, image = img)
                label1.place(x = 0, y = 0)

                hits += 1   

            if (hits >= 2):
                # if it hits the corner, happiness happens
                print("OMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMG")

            root.geometry('+{}+{}'.format(int(x), int(y)))
            root.overrideredirect(True)
            root.attributes('-topmost', True)

            root.update()

            x += xVel
            y += yVel

            time.sleep(0.001)
DVD()