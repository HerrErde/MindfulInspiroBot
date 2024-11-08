# Module imports
from io import BytesIO
from sys import exit as sys_exit
from threading import Thread
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk

from PIL import Image, ImageTk
from requests import get

# Displays a generated inspirational quote with a download button and refresh button which gets a new image

# Globals
IMAGE_LABEL = None
CURRENT_IMAGE = None


# Functions
# Gets an image from the inspirobot api
def get_img(photoimage=False):
    img_url = get("https://inspirobot.me/api?generate=true").text
    img_data = get(img_url).content
    img = Image.open(BytesIO(img_data))

    if photoimage:
        return ImageTk.PhotoImage(img)

    return img


# Replaces the image Label widget with a new one
def new_image(window):
    global IMAGE_LABEL
    global CURRENT_IMAGE

    # There is probably a better/more efficient way to do this
    if IMAGE_LABEL:
        IMAGE_LABEL.place_forget()
        IMAGE_LABEL.destroy()

    # Downloads the image through threading to ensure the program doesn't freeze
    def threaded_img():
        global CURRENT_IMAGE
        global IMAGE_LABEL

        CURRENT_IMAGE = get_img()
        resized_img = CURRENT_IMAGE.resize((250, 250), Image.ANTIALIAS)
        resized_img = ImageTk.PhotoImage(resized_img)
        window.wm_iconphoto(False, resized_img)

        IMAGE_LABEL = ttk.Label(window, image=resized_img)
        IMAGE_LABEL.image = resized_img
        IMAGE_LABEL.place(x=75, y=68)

    thread = Thread(target=threaded_img, daemon=True)
    thread.start()


# Saves the image to a chosen location through a file dialog popup
def save_image():
    global CURRENT_IMAGE

    file_types = [("JPEG Image", ".jpg"), ("All Files", "*")]

    saved_file = fd.asksaveasfile(filetypes=file_types, defaultextension=file_types)
    CURRENT_IMAGE.save(saved_file, format="jpeg")


# Window Setup
window = Tk()
window.title("AI Inspirational Quotes Generator")
window.geometry("400x375")
window.resizable(False, False)

# Non-Functional Labels
ttk.Label(window, text="Powered by inspirobot.me", font=("Arial", 15)).place(x=85, y=30)
ttk.Label(window, text="Inspirational Quote Generator", font=("Arial", 20)).place(
    x=17, y=0
)
ttk.Label(window, text="Getting new quote...", font=("Arial", 10)).place(x=138, y=175)

# Buttons
refresh_button = ttk.Button(window, text="Refresh", command=lambda: new_image(window))
refresh_button.place(x=100, y=335)  # place(x=75, y=350)

download_button = ttk.Button(window, text="Save", command=lambda: save_image())
download_button.place(x=225, y=335)  # place(x=250, y=350)

# Finalising the window
new_image(window)
window.mainloop()

sys_exit(0)
