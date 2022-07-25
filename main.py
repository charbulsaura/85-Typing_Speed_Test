# Assignment: Typing Speed Test
"""
A Tkinter GUI desktop application that tests your typing speed.
"""
"""
Using Tkinter and what you have learnt about building GUI applications with Python, 
build a desktop app that assesses your typing speed. 
Give the user some sample text and detect how many words they can type per minute.

The average typing speed is 40 words per minute. But with practice, you can speed up to 100 words per minute.
https://www.typing.com/blog/typing-speed/

You can try out a web version here:
https://typing-speed-test.aoeu.eu/

If you have more time, you can build your typing speed test into a typing trainer, 
with high scores and more text samples. You can design your program any way you want.
"""
# Approach
"""
https://tkdocs.com/tutorial/text.html #Selecting Text
1. Sample text for user to follow typing along (bonus if able to highlight words already typed/ typed correctly)
2. Textbox for user to input text; but also has to extract text and determine the words typed per second
(maybe run a function using window.after(1000,function) every sec then extract # of characters/words and compute length)
3. Timer (1 min countdown)
4. WPM/CPM counter - Extract # of words or characters first then compute WPM/CPM from countdown mechanism
    -Check WPM/CPM every sec but need to account for scenario if same index checked bef+ user doesnt type anything
    -Have to remove element from list aft check
    -What if user gets one word/character wrong? Then all the following characters and words will all be wrong. 
     How to check? Or just remove wrong word/char from list aft first check
    -Also the writing_text.get(1.0,END) will parse all checked elements back into compare_text... 
    (ADD LIST OF REMOVED ELEMENTS SO ITS NOT REPEATEDLY COMPARED)
    - Global variables not updating from function call (even aft declaring global)--- countdown variable (count) , WPM/CPM/words/chars not being updated on GUI
        https://stackoverflow.com/questions/39669122/function-not-updating-global-variable
        If you pass x as a parameter and then do operations on it inside a function, the global variable x won't be changed.
        Why? Numbers in Python are immutable.
        ---Works in python but not tkinter. Tkinter global variable not updating problem?
        ---Actually its bcos u didnt update/refresh widget on screen!
5. Add win condition if user finishes typing
6. Successfully added adaptive total_duration variable according to "counter" value

Display Improvements: 
-Grey out already typed words/characters

References
>>Tkinter text box insert/delete
"""
# Minor flaws:
# 1.Timer keeps continuing into negatives- use return statement to stop function run
# 2.WPM/CPM doesnt update if user stops typing; YAY FIXED- Added clause to check even if user doesn't input
# 3.No infinite sample text if user has insane typing speed; can read larger sample text from file
# or just extend the sample text length (Easily fixed)
# 4. Achievement message appearing 1 sec earlier due to count and counter mismatch
# 5. Any word entered correctly will count as correct; not checked in order

# SAMPLE_TEXT = "APPLE BANANA CHERRY"
SAMPLE_TEXT = "APPLE BANANA CHERRY DRAGONFRUIT ELDERBERRY FIG GRAPE HONEYDEW IMBE JACKFRUIT KIWI LIME MANGO NECTARINE " \
              "ORANGE PINEAPPLE\nQUINCE RASPBERRY STRAWBERRY TOMATO UGNI WATERMELON XANGO YANGMEI ZUCCHINI\n" \
              "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
sample_text_list = SAMPLE_TEXT.split()
compare_text = ""
removed_text_list = []
SAMPLE_TEXT_BOX_BG = "#41344a"
TYPING_TEXT_BOX_BG = "#d1b879"
COLOR_BG = "#373745"
BLOOD_RED = "#ff3838"
FONT_NAME = "Consolas"

count = 0
words = 0
characters = 0
WPM = 0
CPM = 0
timer = None
win_con = False

from tkinter import *
import math


def get_ready():
    global timer_text, words_counter, char_counter, count, win_con
    canvas.itemconfig(timer_text, text="00:00")

    canvas.itemconfig(words_counter, text=f"WORDS: {words}")
    canvas.itemconfig(wpm_counter, text=f"WPM: {WPM}")
    canvas.itemconfig(char_counter, text=f"CHARACTERS: {characters}")
    canvas.itemconfig(cpm_counter, text=f"CPM: {CPM}")

    count_loop(3, 3)

    sample_text_box.place(x=100, y=500)
    writing_text.place(x=100, y=700)
    writing_text.insert(1.0, "Get ready to be the best typer in the world!")
    start_typing_button.place_forget()
    window.after(1000, message_get_ready)


def message_get_ready():
    sample_text_box.insert(1.0, "GET READY...")
    window.after(1000, message_go)


def message_go():
    writing_text.delete(1.0, END)
    writing_text.insert(1.0, "AND BEGIN!")
    window.after(1000, start_typing)


def start_typing():
    # WORKAROUND: Reinitialize count to 1 & win_con to False to prevent program stop
    global win_con
    global count
    count = 1
    win_con = False

    print("START TYPING ENTERED")
    sample_text_box.delete(1.0, END)
    sample_text_box.insert(1.0, SAMPLE_TEXT)
    writing_text.delete(1.0, END)
    writing_text.focus()
    #TYPING TEST RUN TIME - counter
    counter = 60
    print(f"start_typing/count= {count}")
    count = counter + 2
    total_duration = counter
    print(f"count before: {count}")
    print(f"win_con: {win_con}")
    count_loop(counter, total_duration)


def extract_typed_text(total_duration):
    global win_con, SAMPLE_TEXT, sample_text_list, sample_text_box, compare_text, removed_text, WPM, CPM, words, characters
    compare_text = writing_text.get(1.0, END)
    # print(sample_text_list)

    # Compare extracted text with sample text every second to compute WPM/CPM
    # Only add +1 to WPM/CPM if it matches sample text
    # Have to account for typing error
    # CPM is easy; just assign every word/character (all seperated by a space) to a list, then compare using index for each word/character?

    # ONLY ADD WORD TO COMPARE IF ITS NOT REMOVED BEFORE
    # print(f"removed: {removed_text_list}")
    compiled_text_list = compare_text.split()
    # print(f"compiled_text_list: {compiled_text_list}")

    compare_text_list = []
    for i in range(len(compiled_text_list)):
        if compiled_text_list[i] not in removed_text_list:
            compare_text_list.append(compiled_text_list[i])

    # print(f"compare_list: {compare_text_list}")
    # print(f"sample_list: {sample_text_list}")

    # print(f"Total Characters = {len(compare_text)}")
    for item in compare_text_list:
        # If both words/characters match, remove from checklist & add 1 to score
        # print(f" i = {i}")
        if item in sample_text_list:
            print(f" Element {item} is typed correctly!")
            removed_text_list.append(item)
            compare_text_list.pop(0)
            # Why is item not removed from sample_text_list?
            sample_text_list.remove(item)
            # print(f"sample_list aft check: {sample_text_list}")

            # print("1X CHECK")
            characters += len(item)
            # print(f"characters: {characters}")
            try:
                CPM = round((characters / (total_duration - count) * 60), 2)
                print(f"CPM: {CPM}")
            except ZeroDivisionError:
                print(f"CPM: ERROR")

            # print(len(item))
            # If element has length >1, it is a word and WPM should be tallied accordingly
            if len(item) > 1:
                print("ADD WORD COUNT")
                words += 1
                print(f"words: {words}")
                try:
                    print(f"count: {count}")
                    WPM = round((words / (total_duration - count) * 60), 2)
                    print(f"WPM: {WPM}")
                except ZeroDivisionError:
                    print(f"WPM: ERROR")
        else:
            # Or else just remove from comparison text (aft checking for the first time)
            removed_text_list.append(compare_text_list[-1])
            compare_text_list.pop()

    # UPDATE CPM/WPM EVEN IF USER STOPS TYPING
    try:
        CPM = round((characters / (total_duration - count) * 60), 2)
    except ZeroDivisionError:
        print(f"CPM: ERROR")
    try:
        WPM = round((words / (total_duration - count) * 60), 2)
    except ZeroDivisionError:
        print(f"WPM: ERROR")

    canvas.itemconfig(words_counter, text=f"WORDS: {words}")
    canvas.itemconfig(wpm_counter, text=f"WPM: {WPM}")
    canvas.itemconfig(char_counter, text=f"CHARACTERS: {characters}")
    canvas.itemconfig(cpm_counter, text=f"CPM: {CPM}")
    # WIN CONDITION: Either sample text all cleared or timer hits 0; but bug from initial countdown timer to let user get ready
    # WORKAROUND: Reinitialize count to 1 & win_con to False
    if len(sample_text_list) == 0 or count == 0:
        writing_text.delete(1.0, END)
        writing_text.insert(1.0,
                            f"ACHIEVEMENT UNLOCKED! IT TOOK YOU ONLY {total_duration-count} SECONDS! \nHERE ARE YOUR STATS:\nWords/min: {WPM} \nChars/min: {CPM} \nAnd typed {words} words correctly!")
        win_con = True

    # print(f"removed?: {removed_text_list}")
    # print(f"sample_list aft check: {sample_text_list}")
    window.after(1000, extract_typed_text, total_duration)


# ------------Countdown mechanism-------------#
def count_loop(counter, total_duration):
    # Main Event Loop
    # PLACE RECURSIVE CALL IN MAIN LOOP INSTEAD OF count_down()
    # Calls itself every sec to display stats per sec
    global count, timer
    print("MAIN LOOP")

    # ONLY COUNTDOWN IF NOT USER HAVENT COMPLETED CHALLENGE/WON
    if not win_con:
        timer = window.after(1000, count_down, counter - 1)

        print(f"count_down: counter bef= {counter}")
        count_down(counter)
        count = counter - 1
        print(f"count after: {count}")
        print(f"count_down: counter aft= {counter}\n")
        extract_typed_text(total_duration)
        if count == 0:
            print(f" typed {words} words correctly!")
            print(f" WPM: {WPM}")
            print(f" CPM: {CPM}")
        print(f"PLEASE STOP RUNNING! {counter}")
        if counter > 0:
            window.after(1000, count_loop, counter - 1, total_duration)
        elif counter == 0:
            return counter


def count_down(counter):
    global timer_text, count
    print(f"count_down:{counter}")
    count_min = math.floor(counter / 60)
    count_sec = counter % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    if counter == 0:
        canvas.itemconfig(timer_text, text="")
        return timer_text
    # return count #ONLY RETURNS AT THE END OF WHOLE COUNTDOWN INSTEAD OF EVERY SECOND, CANT USE TO CALC WPM/CPM


# --------------WINDOW-----------------------#
window = Tk()
window.title("Typing Speed Test")
window.config(padx=0, pady=0)
window.minsize(width=1920, height=1080)
# --------------LABELS-----------------------#
canvas = Canvas(width=1920, height=1080, bg=COLOR_BG, highlightthickness=0)

words_counter = canvas.create_text(120, 100, text="", fill="pink", font=(FONT_NAME, 20, "bold"))
wpm_counter = canvas.create_text(120, 130, text="", fill="red", font=(FONT_NAME, 15, "bold"))
char_counter = canvas.create_text(120, 200, text="", fill="pink", font=(FONT_NAME, 20, "bold"))
cpm_counter = canvas.create_text(120, 230, text="", fill="red", font=(FONT_NAME, 15, "bold"))

start_typing_button = Button(text="ALLOW ME TO DEMONSTRATE MY TYPING SKILLS!", fg="white", bg="purple",
                             font=(FONT_NAME, 15),
                             highlightthickness=0, command=get_ready)

keyboard = PhotoImage(file="KEYBOARD.png")
sample_text_box = Text(window, height=6, width=120, bg=SAMPLE_TEXT_BOX_BG, fg="pink", highlightthickness=0,
                       font=(FONT_NAME, 18, "bold"))
writing_text = Text(window, height=6, width=130, bg=TYPING_TEXT_BOX_BG, fg="purple", highlightthickness=0,
                    font=(FONT_NAME, 16))

# -------------------------------------------#

canvas.place(x=0, y=0)
canvas.create_image(950, 250, image=keyboard)
timer_text = canvas.create_text(950, 425, text="", fill="pink", font=(FONT_NAME, 60, "bold"))

start_typing_button.place(x=700, y=500)

window.mainloop()
