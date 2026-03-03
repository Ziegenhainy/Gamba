import random as rd 
import time as t
import threading
import itertools as it
import platformdirs
import json
import os

savefilePath = platformdirs.user_data_dir() + "/ziegenGamba/saveFile"

(platformdirs.user_data_path() / "ziegenGamba").mkdir(exist_ok = True)


MAX_RENT_TIME = 60

data = {
    "money"       : 1000,
    "rentTime"    : MAX_RENT_TIME,
    "timeAlive"   : 0,
    "currentRent" : 500,
    "machines"    : 1
}

def rentTimeLoop():
    global data
    while True:
        data["rentTime"] = data.get("rentTime", MAX_RENT_TIME) - 1
        data["timeAlive"] = data.get("timeAlive", 0) + 1
        if data["rentTime"] < 0:
            break
        print(f"\033[33m\033[s\033[H\x1b[2K\r[{data["rentTime"]}s LEFT!]\033[u\033[39m", end="")
        t.sleep(1)
    print(f"\nYOU DIDNT PAY YOUR RENT! GAME OVER. YOU SURVIVED {data["timeAlive"]} SECONDS")
    with open(savefilePath, "w") as f:
        f.write("")
    os._exit(0)


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
    print("\033c")
    while True:
        rockType = None
        rockQuality = rd.randint(1,100)
        rockReward=1

        if rockQuality >= 100:
            rockType = ("Diamonds","\033[96m")
            rockReward = 100
        elif rockQuality >= 91:
            rockType = ("Gold","\033[93m")
            rockReward = 10
        elif rockQuality >= 81:
            rockType = ("Copper","\033[33m")
            rockReward = 5
        

        for anim in miningAnimation:
            print(f"you have {getMoney()} Money")
            print(end="\033[2K")
            if rockType:
                print(f"Found {rockType[0]}!{rockType[1]}", end="")
            print()
            input(anim)
            print("\033[3A", end="\033[37m")
        setMoney(getMoney()+rockReward)

def slotsLoop() -> None:
    print("\033c")
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

        print("\033c")
        slotMachines = [[rd.randint(0, 100) for _ in range(9)] for _ in range(data["machines"])]
        delay = 0.05
        setMoney(getMoney() - bet)
        for i in it.count():
            if i >= 50:
                if delay > 0.5:
                    delay *= 1+rd.random()
                else:
                    delay *= 1+rd.random()*0.3
            print(end="\033[s")
            for randomSlots in slotMachines:
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
            print("                    |-^^-|", end="\r\033[u")
            t.sleep(delay)
            if delay > 1.5:
                break
        
        winnings = bet
        for randomSlots in slotMachines:
            winnings *= randomSlots[4]/50
        
        winnings = int(winnings)
        
        print(f"\033[{data["machines"]}B")
        if winnings > bet:
            print(f"You Won {winnings-bet}$!")
        elif winnings < bet:
            if winnings == 0:
                print(f"You Lost it all lol :3c")
            else:
                print(f"You Lost {bet-winnings}$ :(")
        else:
            print(f"Nothing Happened Lol :3")
        setMoney(getMoney() + winnings)

def main():
    global data # this is evil and fucked up
    try:
        with open(savefilePath, "r") as f:
            data = json.loads(f.read())
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        with open(savefilePath, "w") as f:
            f.write(json.dumps(data, indent=3))
    
    data["currentRent"] = data.get("currentRent", 500)
    data["machines"] = data.get("machines", 1)

    t = threading.Thread(target=rentTimeLoop)
    t.start()
    while t.is_alive():
        print("What do u wanna do? :3")
        print("[1] Never Stop Gambling")
        print("[2] I Yearn for the mines")
        print(f"[3] Pay Rent  ({data["currentRent"]}$)")
        print("[4] Buy More Slotmachines (100$)")
        menuQuery = input("\x1b[2K")
        try:
            match menuQuery:
                case "1":
                    slotsLoop()
                case "2":
                    minesLoop()
                case "3":
                    if data["money"] < data["currentRent"]:
                        print("\x1b[2K\033[91mYour Too Broke! Get Your Cash Up!", end="\033[37m\r\033[6A")
                    else:
                        data["money"] -= data["currentRent"]
                        data["currentRent"] *= 2
                        data["rentTime"] += MAX_RENT_TIME
                        print("\033c")
                        print(f"Success! New Rent is {data["currentRent"]}")
                        with open(savefilePath, "w") as f:
                            f.write(json.dumps(data, indent=3))
                case "4":
                    if data["money"] < 100:
                        print("\x1b[2K\033[91mYour Too Broke! Get Your Cash Up!", end="\033[37m\r\033[6A")
                    else:
                        data["money"]    -= 100
                        data["machines"] += 1
                        print("\033c")
                        print(f"Success! You Now Have {data["machines"]} Machines!")
                        with open(savefilePath, "w") as f:
                            f.write(json.dumps(data, indent=3))
                case _:
                    print("\x1b[2K\033[91mThats not an option!", end="\033[37m\r\033[6A")
        except KeyboardInterrupt:
            print("\033c")

if __name__ == "__main__":
    print("\033c")
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye Lol")
        os._exit(0)
