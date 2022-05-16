from tkinter import *
from tkinter import messagebox
import pandas as pd
import random

import pandas.errors

BACKGROUND_COLOR = "#B1DDC6"

random_data_set = {}
try:
    french_word = pd.read_csv("data/words_to_learn.csv")
except pandas.errors.EmptyDataError:
    original_french_word = pd.read_csv("data/french_words.csv")
    list_of_dict = original_french_word.to_dict(orient="records")
except FileNotFoundError:
    original_french_word = pd.read_csv("data/french_words.csv")
    list_of_dict = original_french_word.to_dict(orient="records")
else:
    list_of_dict = french_word.to_dict(orient="records")


def random_word():
    global random_data_set
    global card_appearance_delay
    screen.after_cancel(card_appearance_delay)
    try:
        random_data_set = random.choice(list_of_dict)
    except IndexError:
        screen.destroy()
        messagebox.showinfo(title="CONGRATS", message="You've learned all the words, congrats!")
    else:
        card_canvas.itemconfig(current_card_image, image=card_front_img)
        card_canvas.itemconfig(language, text="French", fill="black")
        card_canvas.itemconfig(word, text=random_data_set["French"], fill="black")
        card_appearance_delay = screen.after(3000, english_word)


def english_word():
    card_canvas.itemconfig(current_card_image, image=card_back_img)
    card_canvas.itemconfig(language, text="English", fill="white")
    card_canvas.itemconfig(word, text=random_data_set["English"], fill="white")


def save():
    list_of_dict.remove(random_data_set)
    new_df = pd.DataFrame(list_of_dict)
    new_df.to_csv("data/words_to_learn.csv", index=False)
    random_word()


screen = Tk()
screen.title("Flashy")
screen.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

card_appearance_delay = screen.after(3000, english_word)

card_back_img = PhotoImage(file="images/card_back.png")
card_front_img = PhotoImage(file="images/card_front.png")
card_canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
current_card_image = card_canvas.create_image(400, 263, image=card_front_img)
language = card_canvas.create_text(400, 150, text="Language", font=("Ariel", 40, "italic"))
word = card_canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
card_canvas.grid(row=0, column=0, columnspan=2)

wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, bg=BACKGROUND_COLOR, bd=0, relief="flat", activebackground=BACKGROUND_COLOR,
                      command=random_word)
wrong_button.grid(row=1, column=0)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, bg=BACKGROUND_COLOR, bd=0, relief="flat", activebackground=BACKGROUND_COLOR,
                      command=save)
right_button.grid(row=1, column=1)

random_word()

screen.mainloop()
