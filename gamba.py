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
        delay = 0.05
        money -= bet
        for i in it.count():
            if i >= 50:
                if delay > 0.5:
                    delay *= 1+rd.random()
                else:
                    delay *= 1+rd.random()*0.3
            print("[", end="")
            randomSlots.pop(0)
            randomSlots.append(rd.randint(0,100))
            for n in randomSlots:
                if n > 90:
                    print("\033[35m", end="")
                elif n > 75:
                    print("\033[34m", end="")
                elif n > 50:
                    print("\033[32m", end="")
                else:
                    print("\033[31m", end="")
                print(str(n).center(4), end="\033[37m|")
            print("\b]")
            print("                    |-^^-|", end="\r\033[A")
            t.sleep(delay)
            if delay > 1.5:
                break

        winnings = int(bet * (randomSlots[4]/50))
        if winnings > bet:
            print(f"\n\nYou Won {winnings-bet}$!")
        elif winnings < bet:
            if winnings == 0:
                print(f"\n\nYou Lost it all lol :3c")
            else:
                print(f"\n\nYou Lost {bet-winnings}$ :(")
        else:
            print(f"\n\nNothing Happened Lol :3")
        money += winnings

if __name__ == "__main__":
    main()