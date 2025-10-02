import random
import sys
from random import randint
import os


player = {
    "name": "Player",
    "hp": 100,                   # current hp
    "dmg": [10, 20],             # the range of possible damage
    "heal": 20,                  # how much health the player gains from healing
    "defence": 1.0,              # damage taken is multiplied by this
    "max_hp": 100,               # highest possible hp the player can get
    "heal_cooldown": 0           # how many turns until the player can use heal again
}


def create_enemy(round_number):
    hp = 30 + (round_number * 5)
    dmg_increase = round_number // 3
    damage = [10 + dmg_increase, 20 + dmg_increase]
    return {"name": f"Enemy {round_number}", "hp": hp, "dmg": damage}


def create_boss(round_number):
    hp = 100 + (round_number * 10)
    dmg_increase = round_number // 2  # or round_number // 3 if too fast
    damage = [15 + dmg_increase, 30 + dmg_increase]
    return {"name": f"Boss {round_number // 10}", "hp": hp, "dmg": damage}


def status(round_number, player_hp, opponent_hp, opponent_name, player_dmg, opponent_dmg):   # prints the current status of the game
    print(f'''
Round: {round_number}
You: 
    HP: {player_hp}
    Damage: {player_dmg}
{opponent_name}: 
    HP: {opponent_hp}
    Damage: {opponent_dmg}
    ''')


def choices(cooldown):                                                       #  runs every turn
    if cooldown == 0:
        print("\n Choose a move:")
        print("1. Attack")
        print("2. Heal")
        print("3. Defend")
        print("4. Info")
        print("q. Quit")
        return input("> ")
    else:
        print("\n Choose a move:")
        print("1. Attack")
        print(f"2. Heal ({cooldown})")
        print("3. Defend")
        print("4. Info")
        print("q. Quit")
        return input("> ")


def clear_screen():                                                          #  clears the entire screen with os adaptation
    os.system("cls" if os.name == "nt" else "clear")


def upgrade():                                                               #  gives an upgrade option every 5 rounds
    print(f'''
Choose your upgrade:
1. Damage {player["dmg"]} -> {[x + 10 for x in player["dmg"]]}
2. Healing {player["heal"]} -> {player["heal"] + 10}
3. HP {player["max_hp"]} -> {player["max_hp"] + 20}
    ''')

    while True:
        upgrade_choice = input("> ")
        if upgrade_choice not in ("1", "2", "3"):
            print("You must choose one of the options.")
            continue
        elif upgrade_choice == "1":
            player["dmg"] = [x + 10 for x in player["dmg"]]
            print("Damage upgraded!")
            break
        elif upgrade_choice == "2":
            player["heal"] = player["heal"] + 10
            print("Healing upgraded!")
            break
        else:
            player["max_hp"] = player["max_hp"] + 20
            player["hp"] = player["max_hp"]
            print("Maximum HP upgraded!")
            break


print("Welcome to the infinite arena!")

round_num = 1

while player["hp"] > 0:
    if round_num % 10 != 0:                    # creates a boss every 10 rounds
        opponent = create_enemy(round_num)
    else:
        opponent = create_boss(round_num)

    print(f"You are fighting: {opponent['name']} (HP: {opponent['hp']})")

    while player["hp"] > 0 and opponent["hp"] > 0:

        player["defence"] = 1      # resets the defence option after the turn ends

        status(round_num, player["hp"], opponent["hp"], opponent["name"], player["dmg"], opponent["dmg"])
        choice = choices(player["heal_cooldown"])

        if choice not in ("1", "2", "3", "4", "q"):
            print("You must choose one of the options.")
            continue

        if choice == "1":                                                   #  deals damage to the enemy
            dmg = randint(player["dmg"][0], player["dmg"][1])
            opponent["hp"] -= dmg
            clear_screen()
            print(f"You dealt {dmg} damage to {opponent['name']}!")

        elif choice == "2":                                                 #  heals the player
            if player["heal_cooldown"] == 0:
                player["hp"] += player["heal"]
                if player["hp"] > player["max_hp"]:
                    player["hp"] = player["max_hp"]
                player["heal_cooldown"] = 2
                clear_screen()
                print(f"You healed for {player['heal']} HP! Current HP: {player['hp']}")
            else:
                print(f"Heal on cooldown! Turns left until usable: {player['heal_cooldown']}.")
                continue


        elif choice == "3":                                                 #  decreases damage taken by 50% for 1 turn
            player["defence"] = 0.5

            clear_screen()
            print("You defended, reducing incoming damage by 50% this turn.")

        elif choice == "4":                                                 #  informs the player on what each option does
            print('''
1. Attack - Does damage to the enemy. Damage dealt is a random number between 10-20.
2. Heal - Heals you by 25 HP.
3. Defend - Reduces incoming damage by 50%.
4. Info - Displays this menu
            ''')
            continue

        elif choice == "q":                                                  #  quits the game
            sys.exit(0)

        if opponent["hp"] > 0:                                                                     #  opponent's turn
            dmg = round(randint(opponent["dmg"][0], opponent["dmg"][1]) * player["defence"])
            player["hp"] -= dmg
            if player["defence"] != 1:
                print(f"{opponent['name']} dealt {dmg} to You! (Defend used)")
            else:
                print(f"{opponent['name']} dealt {dmg} to You!")
        else:
            break

        if player["heal_cooldown"] > 0:                                      # reduces the healing cooldown timer by 1
            player["heal_cooldown"] -= 1


    round_num += 1

    if round_num % 5 == 0:
        clear_screen()
        upgrade()

    if player["hp"] > 0:                                                     #  bonus hp after winning
        player["hp"] += 35
        if player["hp"] > player["max_hp"]:
            player["hp"] = player["max_hp"]
        print("35 bonus HP given for winning the round")

print("Game Over!")