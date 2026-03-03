import random as rd 
import time as t
import itertools as it
import platformdirs
import json
import os

savefilePath = platformdirs.user_data_dir() + "/ziegenGamba/saveFile"

(platformdirs.user_data_path() / "ziegenGamba").mkdir(exist_ok = True)

data = {
    "money" : 1000
}


def setMoney(newMoney: int) -> None:
    data["money"] = newMoney
    with open(savefilePath, "w") as f:
        f.write(json.dumps(data, indent=3))

def getMoney() -> int:
    return data["money"]


miningAnimation = [
    "[ ]⛏",
    "[.]⛏",
    "[,]⛏",
    "[-]⛏",
    "[x]⛏",
    "[#]⛏"
]

def minesLoop() -> None:
    while True:
        for anim in miningAnimation:
            print(f"you have {getMoney()} Money")
            input(anim)
            print("\033[A\033[A", end="")
        setMoney(getMoney()+1)

def slotsLoop() -> None:
    while True:
        bet = -1
        while bet == -1:
            betQuery = input(f"\x1b[2KYou have {getMoney()}$ left, how much do you wanna gamba? ")
            try:
                bet = int(betQuery)
            except ValueError:
                print("\x1b[2K\033[91mYOU ARE STUPID! ENTER A NUMBER!", end="\033[37m\r\033[A")
            if getMoney() < bet:
                print("\x1b[2K\033[91mYOU ARE BROKE! BET LESS!", end="\033[37m\r\033[A")
                bet = -1

        randomSlots = [rd.randint(0, 100) for _ in range(9)]
        delay = 0.05
        setMoney(getMoney() - bet)
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
        setMoney(getMoney() + winnings)

def main():
    try:
        with open(savefilePath, "r") as f:
            data = json.loads(f.read())
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        with open(savefilePath, "w") as f:
            f.write(json.dumps(data, indent=3))
    
    while True:
        print("What do u wanna do? :3")
        print("[1] Never Stop Gambling")
        print("[2] I Yearn for the mines")
        menuQuery = input("\x1b[2K")
        try:
            match menuQuery:
                case "1":
                    slotsLoop()
                case "2":
                    minesLoop()
                case _:
                    print("\x1b[2K\033[91mThats not an option!", end="\033[37m\r\033[A\033[A\033[A\033[A")
        except KeyboardInterrupt:
            print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye Lol")
        exit()
