from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
french_words_to_learn_dict = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    french_words_to_learn_dict = original_data.to_dict(orient="records")
else:
    french_words_to_learn_dict = data.to_dict(orient="records")

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(french_words_to_learn_dict)
    canvas.itemconfig(card_title,text="French",fill="black")
    canvas.itemconfig(card_word, text=current_card.get("French"),fill="black")
    canvas.itemconfig(card_background,image=card_front_img)
    flip_timer =  window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="English",fill="white")
    canvas.itemconfig(card_word,text=current_card.get("English"),fill="white")
    canvas.itemconfig(card_background,image=card_back_img)

def is_known():
    french_words_to_learn_dict.remove(current_card)
    data = pandas.DataFrame(french_words_to_learn_dict)
    data.to_csv("data/words_to_learn.csv",index=False)
    next_card()

window = Tk()
window.title("Capstone Flash Card Game")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer =  window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=cross_image, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
right_button = Button(image=check_image, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

next_card()

window.mainloop()
