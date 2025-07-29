import time

def write(text, delay):
    try:
        for word in (text).split():
            print(word, end=' ', flush=True)
            time.sleep(delay)

    except:
        print("")
        print("Useless Error message here. You fucked up somehow")

def write_letters(text, delay):
    try:
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)

    except:
        print("")
        print("Useless Error message here. You fucked up somehow")