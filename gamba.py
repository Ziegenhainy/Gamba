import random as rd 
import time as t
import itertools as it


def main():
    randomSlots = [rd.randint(0, 100) for _ in range(9)]
    
    delay = 0.1

    for i in it.count():
        if i >= 20:
            delay *= 1+rd.random()*0.5
        print("[", end="")
        randomSlots.pop(0)
        randomSlots.append(rd.randint(0,100))
        for n in randomSlots:
            print(str(n).center(4), end="|")
        print("\b]")
        print("                      ^^", end="\r\033[A")
        t.sleep(delay)
        if delay > 1.5:
            break
    print(f"\n\nYou Won {randomSlots[4]}!")

if __name__ == "__main__":
    main()