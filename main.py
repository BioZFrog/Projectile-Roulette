import random

print("""
    =================
    Projectile Roulette
    =================\n""")

items = ["Beer", "Hand Saw", "HandCuffs", "Cigarette", "Inverter", "Expired Medicine", "Adrenaline"]
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

    if not player_shotgun:
        print("No more shots left in the shotgun!")
        return

    print(f"\n{name}'s shotgun: {player_shotgun}")
    print(f"{name}'s turn: ({player_items}) Choose an action or item: ", end="")
    player_choice = input().strip()
    
    # Shotgun
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

        # Beer
        if player_choice == "Beer":
            if player_shotgun:
                removed_item = player_shotgun[0]
                player_shotgun.pop(0)
                print(f"Removed item from {name}'s shotgun: {removed_item}")

        # Hand Saw
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

        # Inverter
        elif player_choice == "Inverter":
            if player_shotgun[0] == "Live Round":
                player_shotgun[0] = "Blank"
            elif player_shotgun[0] == "Blank":
                player_shotgun[0] = "Live Round"

        # HandCuffs
        elif player_choice == "HandCuffs":
            return "HandCuffs"
        
        # Adrenaline
        elif player_choice == "Adrenaline":
            steal = input(f"\nPick one of Dealer's items: {dealer_items} ").strip()

            if steal in dealer_items:
                if steal == "Adrenaline":
                    print("Can't Use That!")

                elif steal == "Inverter":
                    dealer_items.remove("Inverter")
                    if player_shotgun[0] == "Live Round":
                        player_shotgun[0] = "Blank"
                    elif player_shotgun[0] == "Blank":
                        player_shotgun[0] = "Live Round"

                elif steal == "HandCuffs":
                    dealer_items.remove("HandCuffs")
                    return "HandCuffs"
                
                elif steal == "Hand Saw":
                    dealer_items.remove("Hand Saw")
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

                elif steal == "Beer":
                    if player_shotgun:
                        removed_item = player_shotgun[0]
                        player_shotgun.pop(0)
                        print(f"Removed item from {name}'s shotgun: {removed_item}")

                elif steal == "Expired Medicine":
                    chances = [4,7]
                    percentage = [60, 40]
                    
                    player_health_change = random.choices(chances, weights=percentage, k=1)[0]
                    dealer_items.remove("Expired Medicine")

                    if player_health_change == 7:
                        print(f"{name} gained 2 lives because of Expired Medicine!")
                        player_health += 2
                    elif player_health_change == 4:
                        print(f"{name} lost 1 life because of Expired Medicine!")
                        player_health -= 1
                    print(f"{name}'s Health after Expired Medicine: {player_health}")

                elif steal == "Cigarette":
                    dealer_items.remove("Cigarette")
                    if player_health < 4:
                        player_health += 1
                        print(f"{name}'s Health after Cigarette: {player_health}")
                    else:
                        print("Can't Use That!")
            else:
                print("Invalid Input!")

        # Expired Medicine
        elif player_choice == "Expired Medicine":
            chances = [4,7]
            percentage = [60, 40]
            
            player_health_change = random.choices(chances, weights=percentage, k=1)[0]

            if player_health_change == 7:
                print(f"{name} gained 2 lives because of Expired Medicine!")
                player_health += 2
            elif player_health_change == 4:
                print(f"{name} lost 1 life because of Expired Medicine!")
                player_health -= 1
            print(f"{name}'s Health after Expired Medicine: {player_health}")

        # Cigarette
        elif player_choice == "Cigarette" and player_health < 4:
            player_health += 1
            print(f"{name}'s Health after Cigarette: {player_health}")
        else:
            print("Invalid Input!")
    
    return None

def dealer_turn_action():
    global dealer_shotgun
    global dealer_health
    global player_health
    global shotgun_damage
    global dealer_items

    if not dealer_shotgun:
        print("No more shots left in the shotgun!")
        return

    if dealer_shotgun[0] == "Live Round" and "Hand Saw" in dealer_items:
        dealer_choice = "Hand Saw"
    else:
        dealer_choice = random.choice(dealer_items)
    
    print(f"\nDealer's turn: Dealer chooses {dealer_choice}")

    # Shotgun
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
        
        # Beer
        if dealer_choice == "Beer":
            if dealer_shotgun:
                removed_item = dealer_shotgun[0]
                dealer_shotgun.pop(0)
                print(f"Removed item from dealer's shotgun: {removed_item}")
        
        # Hand Saw
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

        # Inverter
        elif dealer_choice == "Inverter":
            if dealer_shotgun[0] == "Live Round":
                dealer_shotgun[0] = "Blank"
            elif dealer_shotgun[0] == "Blank":
                dealer_shotgun[0] = "Live Round"

        # HandCuffs
        elif dealer_choice == "HandCuffs":
            return "HandCuffs"

        # Adrenaline
        elif dealer_choice == "Adrenaline":
            if "Expired Medicine" in player_items:
                player_items.remove("Expired Medicine")
                dealer_items.append("Expired Medicine")
                chances = [4,7]
                percentage = [60, 40]
                
                dealer_health_change = random.choices(chances, weights=percentage, k=1)[0]

                if dealer_health_change == 7:
                    print("Dealer gained 2 lives because of Expired Medicine!")
                    dealer_health += 2
                elif dealer_health_change == 4:
                    print("Dealer lost 1 life because of Expired Medicine!")
                    dealer_health -= 1
                print(f"Dealer's Health after Expired Medicine: {dealer_health}")

        # Expired Medicine
        elif dealer_choice == "Expired Medicine":
            chances = [4,7]
            percentage = [60, 40]
            
            dealer_health_change = random.choices(chances, weights=percentage, k=1)[0]

            if dealer_health_change == 7:
                print("Dealer gained 2 lives because of Expired Medicine!")
                dealer_health += 2
            elif dealer_health_change == 4:
                print("Dealer lost 1 life because of Expired Medicine!")
                dealer_health -= 1
            print(f"Dealer's Health after Expired Medicine: {dealer_health}")

        # Cigarette
        elif dealer_choice == "Cigarette" and dealer_health < 4:
            dealer_health += 1
            print(f"Dealer's Health after Cigarette: {dealer_health}")
        else:
            print("Invalid Input!")

    return None

def check_health():
    if player_health <= 0:
        print("Dealer wins!")
        return True
    elif dealer_health <= 0:
        print(f"{name} wins!")
        return True
    return False

while player_health > 0 and dealer_health > 0:
    handcuffs = player_turn_action()
    if check_health():
        break

    if handcuffs == "HandCuffs":
        print(f"\n{name} used HandCuffs to skip the dealer's turn!")
        continue

    handcuffs = dealer_turn_action()
    if check_health():
        break

    if handcuffs == "HandCuffs":
        print("Dealer used HandCuffs to skip your turn!")
        continue
