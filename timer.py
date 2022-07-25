# LOCALIZE THE PROBLEM; TACKING CODE SNIPPETS SECTION BY SECTION
# ENGINEER YOUR OWN SOLUTIONS

import math
import time

# HOW TO CHANGE GLOBAL VARIABLE EVERY SECOND THROUGH A FUNCTION CALL?

count = 10


# TRYING TO MAKE IT PASS VARIABLE count EVERY SEC INSTEAD OF ONLY AT THE END OF count_down_per_sec...
# SO THAT ABLE TO DISPLAY STATS PER SEC
# Maybe instead of recursive count_down_per_sec, use time.sleep in count_transfer_variable so that variable can be accessed every second
# Make count_transfer_variable implement recursive calls to count_down instead
def count_transfer_variable():
    global count
    counter = 5
    count = counter

    print(f"count before: {count}")
    for i in range(counter):
        time.sleep(1)
        print(f"count_down: counter bef= {counter}")
        count_down(counter)
        count = counter - 1
        print(f"count after: {count}")
        counter-=1
        print(f"count_down: counter aft= {counter}\n")



def count_down(counter):
    global count
    print("TOP OF TIMER")
    print(f"count_down: counter = {counter}")
    count_min = math.floor(counter / 60)
    count_sec = counter % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    print(f"{count_min}:{count_sec}")

    if counter == 0:
        print("RESET! 00:00")


def count_down_per_sec(counter):
    global count
    print("TOP OF TIMER")
    print(f"count_down: counter = {counter}")
    count_min = math.floor(counter / 60)
    count_sec = counter % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    print(f"{count_min}:{count_sec}")

    # Recursive when counter >0 -- timer will countdown to 0 by calling itself
    if counter > 0:
        # timer = window.after(1000, count_down, counter - 1)
        time.sleep(1)
        print(f"count_down: counter aft= {counter}")
        count = counter - 1
        print(f"count :{count}")
        print("CALLING ITSELF\n")
        count_down(counter - 1)
    if counter == 0:
        print("RESET! 00:00")


count_transfer_variable()
print(f"count outside function call: {count}")
