import random as rd 
import time as t
import itertools as it


def main():
    money = 1000
    
    while True:
        bet = -1
        while bet == -1:
            betQuery = input(f"\x1b[2KYou have {money}$ left, how much do you wanna gamba? ")
            try:
                bet = int(betQuery)
            except ValueError:
                print("\033[91mYOU ARE STUPID! ENTER A NUMBER!", end="\033[37m\r\033[A")

            if money < bet:
                print("\033[91mYOU ARE BROKE! BET LESS!", end="\033[37m\r\033[A")
                bet = -1

        randomSlots = [rd.randint(0, 100) for _ in range(9)]
        delay = 0.1
        money -= bet
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

        winnings = int(bet * (randomSlots[4]/50))
        print(f"\n\nYou Won {winnings}$!")
        money += winnings

if __name__ == "__main__":
    main()