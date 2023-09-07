import time
import os
import random

class Arena:
    def __init__(self):
        pass

    def battle(self, heroes:list, enemies:list):
        # shuffle the characters list
        random.shuffle(heroes)
        random.shuffle(enemies)

        def show_summary():
            """
            Clear screen and show updated status of characters.
            """
            if os.name == "nt":
                os.system("cls")  # For Windows
            else:
                os.system("clear")  # For macOS and Linux
            # print()
            max_length = max(len(sublist) for sublist in [heroes, enemies])
            ch_disp = []
            for i in range(max_length):
                row = []
                for sublist in [heroes, enemies]:
                    if i < len(sublist):
                        row.append(sublist[i])
                    else:
                        row.append(None)
                ch_disp.append(row)

            j_val = 44
            # print()
            print (f'{"  HEROES  ":=^{j_val}}' + '|' + f'{"  ENEMIES  ":=^{j_val}}')
            print (f' '.ljust(j_val) + '|' + f' '.ljust(j_val))
            for i in ch_disp:
                print (f'  - {i[0].ch_name} - {i[0].ch_class}'.ljust(j_val) + '|' 
                    if i[0] else ''.ljust(j_val) + '|', end = '')
                print (f'  - {i[1].ch_name} - {i[1].ch_class}'.ljust(j_val) 
                    if i[1] else '')

                print (f'    {i[0].ch_atk} / {i[0].ch_def} / {i[0].ch_acc} / {i[0].ch_luk}'.ljust(
                    j_val) + '|' if i[0] else ''.ljust(j_val) + '|', end = '')
                print (f'    {i[1].ch_atk} / {i[1].ch_def} / {i[1].ch_acc} / {i[1].ch_luk}'.ljust(
                    j_val) if i[1] else '')

                print (f'    {i[0].get_hp_bar()}'.ljust(j_val) + '|' 
                    if i[0] else ''.ljust(j_val) + '|', end = '')
                print (f'    {i[1].get_hp_bar()}'.ljust(j_val) 
                    if i[1] else '')

                print (f'    {i[0].get_mp_bar()}'.ljust(j_val) + '|' 
                    if i[0] else ''.ljust(j_val) + '|', end = '')
                print (f'    {i[0].get_mp_bar()}'.ljust(j_val)
                    if i[1] else '')
                
                print (
                    f'   '.ljust(j_val) + '|' + f'   '.ljust(j_val))
                
            print (f'{"":=^{j_val*2+1}}')
            print("* Stats: ATK / DEF / ACC / LUK")
            print("* Input b to go back, q for quit.")

        def select_choice(isRoot, prompt, choice_dict):
            """
            For showing actions or target list and validating user input. If invalid, loop until it valid.
                - isRoot: if isRoot is true, user can't input b for back
                - prompt: For showing input prompt.
                - action_dict: The dict for choices list. <- { "number": ["name", ... ] }
                - -> output: A validated string of input.
            """
            for choice in choice_dict:
                print(f"  {choice}. {choice_dict[choice][0]}")
            check = True
            while check:
                selection = input(prompt)
                print()
                if isRoot:
                    if selection == "q":
                        check = False
                    elif selection == "b":
                        print("No back! Try again")
                    elif selection.isnumeric() == False:
                        print("Invalid input! Try again")
                    elif int(selection) > len(choice_dict):
                        print("The input exceeds the list! Try again")
                    else:
                        check = False
                else:
                    if selection == "b" or selection == "q":
                        check = False
                    elif selection.isnumeric() == False:
                        print("Invalid input! Try again")
                    elif int(selection) > len(choice_dict):
                        print("The input exceeds the list! Try again")
                    else:
                        check = False
            return selection

        def create_char_dict(team, charObj_list):
            """
            Create char dict from char objects list for showing in input command.
            Parameter:
                - team: Should be 'hero' or 'enemy'.
                - charObj_list: List of character's object.
                - -> Output: { "number": ["name", object] }
            """
            char_dict = {}
            num = 1
            for char in charObj_list:
                if team == "enemy":
                    if char.ch_hp_r > 0:
                        # char_dict = {number : [Name, Object]}
                        char_dict[f"{num}"] = [char.ch_name, char]
                        num += 1
                else:
                    # char_dict = {number : [Name, Object]}
                    char_dict[f"{num}"] = [char.ch_name, char]
                    num += 1
            return char_dict

        game_turn = True  # for checking if user are not quit
        # game loop until one team is all dead
        while any(hero.ch_hp_r > 0 for hero in heroes) and \
              any(mons.ch_hp_r > 0 for mons in enemies):
            # iterate hero turns
            for hero in heroes:
                if hero.ch_hp_r > 0 and any(mons.ch_hp_r > 0 for mons in enemies):
                    show_summary()
                    print(f"\n-> {hero.ch_name}'s turn.\n")

                    # loop until the char's action success
                    while True:
                        sel_action_prompt = f"What will {hero.ch_name} do?: "
                        # select action
                        sel_action = select_choice(True, sel_action_prompt, hero.skill_list)
                        if sel_action == "q":
                            game_turn = False
                            break

                        # check skill mode and setup the 'char_dict' of targets to action with
                        # such as, if the action is 'attack', the list should be enemies
                        # or if 'heal', it shoud be heroes themself
                        action_mode = hero.skill_list[sel_action][1]
                        if action_mode == 0:
                            sel_char_prompt = (f"Which enemy will {hero.ch_name} attack?: ")
                            char_dict = create_char_dict("enemy", enemies)
                        elif action_mode == 2:
                            sel_char_prompt = f"Which one will {hero.ch_name} heal?: "
                            char_dict = create_char_dict("hero", heroes)

                        # select target
                        sel_char = select_choice(False, sel_char_prompt, char_dict)
                        if sel_char == "b":
                            continue
                        elif sel_char == "q":
                            game_turn = False
                            break
                        else:
                            time.sleep(0.5)
                            # get hero's methods to do action
                            # 'skill_list' attr: 
                            #   {skillNum: [skillName, skillMode, manaUsed, method]}
                            #   {"1": ["Attack", 0, 0, attack]}
                            #    ^^^                   ^^^^^^
                            #   sel_action             *[3]*
                            hero_action = getattr(hero, hero.skill_list[sel_action][3])
                            # do action: _.action_method(target_obj)
                            # target_obj <- char_dict:
                            #   {"number": ["name", object]}
                            #    ^^^^^^^^           ^^^^^^
                            #    sel_char           *[1]*
                            success = hero_action(char_dict[sel_char][1])
                            print()
                            if success:
                                input("\nPress Enter to continue...")
                                break
                    if game_turn == False:
                        break
                else:
                    continue
            if game_turn == False:
                break
            show_summary()
            # iterate enemy turns
            for enemy in enemies:
                if any(hero.ch_hp_r > 0 for hero in heroes):
                    if enemy.ch_hp_r > 0:
                        alive_heroes_list = [
                            hero for hero in heroes if hero.ch_hp_r > 0
                        ]
                        hero_target = random.choice(alive_heroes_list)
                        print()
                        enemy.attack(hero_target)
                        time.sleep(1)
                else:
                    break
            if any(mons.ch_hp_r > 0 for mons in enemies):
                input("\nPress Enter to continue...")

        if game_turn == True:
            show_summary()
            if any(hero.ch_hp_r > 0 for hero in heroes):
                print("\nHEROES ARE WIN!\n")
            else:
                print("\nALL HEROES ARE DEAD.")
            print()