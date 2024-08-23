import random

print("""
    =================
    Projectile Roulette
    =================\n""")

items = ["Beer", "Hand Saw", "HandCuffs", "Cigarette"]
chambers = 6  

name = input("Name: ")

player_items = random.choices(items, k=8)
dealer_items = random.choices(items, k=8)

player_health = 5
dealer_health = 5

shotgun_damage = 1

def generate_shotgun(chambers):
    rounds = ["Blank", "Live Round"]
    return random.choices(rounds, k=chambers)

player_shotgun = generate_shotgun(chambers)
dealer_shotgun = generate_shotgun(chambers)

def player_turn_action():
    global player_shotgun
    global dealer_health
    global player_health
    global shotgun_damage
    global player_items
    global dealer_handcuffs_used

    if not player_shotgun:
        print("No more shots left in the shotgun!")
        return

    print(f"\n{name}'s shotgun: {player_shotgun}")
    print(f"{name}'s turn: ({player_items}) Choose an action or item: ", end="")
    player_choice = input().strip()

    if player_choice == "Shotgun":
        if not player_shotgun:
            print("No more shots left in the shotgun!")
            return

        shoot = input("Shoot at (You/Dealer): ").strip()
        if shoot == "You":
            if player_shotgun[0] == "Live Round":
                print(f"{name} fired a Live Round on Themselves!")
                player_health -= shotgun_damage
                print(f"{name}'s Health: {player_health}")
            else:
                print(f"{name} fired a Blank on Themselves!")
        elif shoot == "Dealer":
            if player_shotgun[0] == "Live Round":
                print(f"{name} fired a Live Round on Dealer!")
                dealer_health -= shotgun_damage
                print(f"Dealer's Health: {dealer_health}")
            else:
                print(f"{name} fired a Blank on Dealer!")
        player_shotgun.pop(0)

    elif player_choice in player_items:
        player_items.remove(player_choice)

        if player_choice == "Beer":
            if player_shotgun:
                removed_item = player_shotgun[0]
                player_shotgun.pop(0)
                print(f"Removed item from {name}'s shotgun: {removed_item}")

        elif player_choice == "Hand Saw":
            if player_shotgun and player_shotgun[0] == "Live Round":
                print(f"Shotgun damage increased to 2 due to Hand Saw!")
                shotgun_damage = 2
                dealer_health -= shotgun_damage
                if dealer_health < 0:
                    dealer_health = 0
                print(f"Dealer's Health after Hand Saw: {dealer_health}")
            else:
                shotgun_damage = 1
                print("Can't Use That!")
            if player_shotgun:
                player_shotgun.pop(0)

        elif player_choice == "HandCuffs":
            if "HandCuffs" in player_items:
                player_items.remove("HandCuffs")
                return "HandCuffs"
    
        elif player_choice == "Cigarette" and player_health < 4:
            if player_health < 4:
                player_health += 1
                print(f"{name}'s Health after Cigarette: {player_health}")
            else:
                print("Can't Use That!")
        else:
            print("Invalid Input!")
    
    return None

def dealer_turn_action():
    global dealer_shotgun
    global dealer_health
    global player_health
    global shotgun_damage
    global dealer_items
    global player_handcuffs_used

    if not dealer_shotgun:
        print("No more shots left in the shotgun!")
        return

    if dealer_shotgun[0] == "Live Round" and "Hand Saw" in dealer_items:
        dealer_choice = "Hand Saw"
    else:
        dealer_choice = random.choice(dealer_items)
    
    print(f"\nDealer's turn: Dealer chooses {dealer_choice}")

    if dealer_choice == "Shotgun":
        if not dealer_shotgun:
            print("No more shots left in the shotgun!")
            return

        shoot = random.choice(["You", "Dealer"])
        if shoot == "You":
            if dealer_shotgun[0] == "Live Round":
                print(f"Dealer fired a Live Round on {name}!")
                player_health -= shotgun_damage
                dealer_shotgun.pop(0)
            else:
                print(f"Dealer fired a Blank on {name}!")
                dealer_shotgun.pop(0)
        elif shoot == "Dealer":
            if dealer_shotgun[0] == "Live Round":
                print(f"Dealer fired a Live Round on Themselves!")
                dealer_health -= shotgun_damage
                dealer_shotgun.pop(0)
            else:
                print(f"Dealer fired a Blank on Themselves!")
                dealer_shotgun.pop(0)

    elif dealer_choice in dealer_items:
        dealer_items.remove(dealer_choice)

        if dealer_choice == "Beer":
            if dealer_shotgun:
                removed_item = dealer_shotgun[0]
                dealer_shotgun.pop(0)
                print(f"Removed item from dealer's shotgun: {removed_item}")

        elif dealer_choice == "Hand Saw":
            if dealer_shotgun and dealer_shotgun[0] == "Live Round":
                print(f"Shotgun damage increased to 2 due to Hand Saw!")
                shotgun_damage = 2
                player_health -= shotgun_damage 
                if player_health < 0:
                    player_health = 0
                print(f"{name}'s Health after Hand Saw: {player_health}")
            else:
                shotgun_damage = 1
                print("Can't Use That!")
            if dealer_shotgun:
                dealer_shotgun.pop(0)

        elif dealer_choice == "HandCuffs":
            if "HandCuffs" in dealer_items:
                dealer_items.remove("HandCuffs")
                return "HandCuffs"
            else:
                print("Dealer has already used HandCuffs.")
    
        elif dealer_choice == "Cigarette" and dealer_health < 4:
            dealer_health += 1
            print(f"Dealer's Health after Cigarette: {dealer_health}")
    
    return None

player_handcuffs_used = False
dealer_handcuffs_used = False
current_turn = "player"


if player_health < 0:
        player_health = 0

if dealer_health < 0:
        dealer_health = 0

while player_health > 0 and dealer_health > 0:
    if current_turn == "player":
        player_choice = player_turn_action()
        if player_choice == "HandCuffs":
            print(f"{name} used HandCuffs! Skipping dealer's turn and taking another turn.")
            dealer_handcuffs_used = True
            continue 

        if player_health <= 0:
            print(f"{name} has been eliminated!")
            break
        elif dealer_health <= 0:
            print(f"Dealer has been eliminated!")
            break
        
        current_turn = "dealer"
        
    elif current_turn == "dealer":
        dealer_choice = dealer_turn_action()
        if dealer_choice == "HandCuffs":
            print("Dealer used HandCuffs! Skipping player's turn and taking another turn.")
            player_handcuffs_used = True
            continue 

        if player_health <= 0:
            print(f"{name} has been eliminated!")
            break
        elif dealer_health <= 0:
            print(f"Dealer has been eliminated!")
            break
        
        current_turn = "player"

print("The game has ended.")
