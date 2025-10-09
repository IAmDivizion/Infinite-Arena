import random
import sys
from random import randint
import os


player = {
    "name": "Player",
    "hp": 100,                   # current hp
    "dmg": [10, 20],             # the range of possible damage
    "heal": 20,                  # how much health the player gains from healing
    "defense": 0.4,              # damage taken is multiplied by this
    "max_hp": 100,               # highest possible hp the player can get
    "heal_cooldown": 0,          # how many turns until the player can use heal again
    "defending": False           # Check if player is defending
}


def create_enemy(round_number):
    hp = 30 + (round_number * 5)
    dmg_increase = round_number // 3
    damage = [10 + dmg_increase, 20 + dmg_increase]
    heal = 10 + round_number
    defense = 0.5
    defending = False
    return {"name": f"Enemy {round_number}", "hp": hp, "dmg": damage, "heal": heal, "defense": defense, "defending": defending}


def create_boss(round_number):
    hp = 100 + (round_number * 5)
    dmg_increase = round_number // 3  # or round_number // 3 if too fast
    damage = [15 + dmg_increase, 30 + dmg_increase]
    heal = 20 + round_number
    defense = 0.5
    defending = False
    return {"name": f"Boss {round_number // 10}", "hp": hp, "dmg": damage, "heal": heal, "defense": defense, "defending": defending}


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
4. Defense {player["defense"]*100:.0f}% -> {(player["defense"]*100)+5:.0f}%
    ''')

    while True:
        upgrade_choice = input("> ")
        if upgrade_choice not in ("1", "2", "3", "4"):
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
        elif upgrade_choice == "3":
            player["max_hp"] = player["max_hp"] + 20
            player["hp"] = player["max_hp"]
            print("Maximum HP upgraded!")
            break
        elif upgrade_choice == "4":
            if player["defense"] == 0.65:
                print("Maximum defense reached!")
                continue
            else:
                player["defense"] = player["defense"] + 0.05
                print("defense upgraded!")



print("Welcome to the infinite arena!")

round_num = 1

while player["hp"] > 0:
    if round_num % 10 != 0:                    # creates a boss every 10 rounds
        opponent = create_enemy(round_num)
    else:
        opponent = create_boss(round_num)

    print(f"You are fighting: {opponent['name']} (HP: {opponent['hp']})")

    while player["hp"] > 0 and opponent["hp"] > 0:

        status(round_num, player["hp"], opponent["hp"], opponent["name"], player["dmg"], opponent["dmg"])
        choice = choices(player["heal_cooldown"])

        if choice not in ("1", "2", "3", "4", "q"):
            print("You must choose one of the options.")
            continue

        if choice == "1":                                                   #  deals damage to the enemy
            if opponent["defending"] and random.random() <= opponent["defense"]:
                opponent["defending"] = False
                clear_screen()
                print(f"{opponent['name']} defended you attack!")

            elif opponent["defending"] and random.random() > opponent["defense"]:
                opponent["defending"] = False
                dmg = randint(player["dmg"][0], player["dmg"][1])
                opponent["hp"] -= dmg
                clear_screen()
                print(f"{opponent['name']}'s defense failed! You dealt {dmg} damage to {opponent['name']}!")
            else:
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
            player["defending"] = True
            clear_screen()
            print("You defended...")

        elif choice == "4":                                                 #  informs the player on what each option does
            print(f'''
1. Attack - Does damage to the enemy. Damage dealt is a random number between {player["dmg"]}.
2. Heal - Heals you by {player["heal"]} HP.
3. Defend - {player["defense"] * 100:.0f}% chance to block your opponents attack.
4. Info - Displays this menu
            ''')
            continue

        elif choice == "q":                                                  #  quits the game
            sys.exit(0)

        if opponent["hp"] > 0:                                                                     #  opponent's turn
            opponent_choice = randint(1,4)
            if opponent_choice in (1, 2):
                if player["defending"] and random.random() <= player["defense"]:
                    print(f"Defend success! You defended {opponent['name']}'s attack!")
                elif player["defending"] and random.random() > player["defense"]:
                    dmg = round(randint(opponent["dmg"][0], opponent["dmg"][1]))
                    player["hp"] -= dmg
                    print(f"Defend failure! {opponent['name']} dealt {dmg} to you!")
                else:
                    dmg = round(randint(opponent["dmg"][0], opponent["dmg"][1]))
                    player["hp"] -= dmg
                    print(f"{opponent['name']} dealt {dmg} to you!")

            elif opponent_choice == 2:
                opponent["hp"] += opponent["heal"]
                print(f"opponent healed for {opponent['heal']} HP")

            elif opponent_choice == 3:
                opponent["defending"] = True
                print("Opponent defending...")

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