#!/usr/bin/env python3

import sys
import json
import re
import textwrap

def squash_dict_of_list(padding, to_squash):
    result = padding
    for key in to_squash:
        result += f"\n{padding}{str(key)}: {' '.join(to_squash[key])}"
    return result

card_types = ["attack", "battlegear", "creature", "location", "mugic"]

comparitors = [
        '==', # Is
        '!=', # Is not
        '>>', # Greater than
        '<<', # Less than
        '>=', # Greater than or equal to
        '<=', # Less than or equal to
        '~',  # Contains
        '!~', # Does not contain
        '*',  # Matches regex
        '!*'  # Does not match regex
        ]

keys = {
        "attack": {
            "Name": ['==', '!=', '~', '!~', '!*', '*'],
            "Set": ['==', '!=', '~', '!~', '!*', '*'],
            "Rarity": ['==', '!=', '~', '!~'],
            "ID": ['==', '!=', '>>', '<<', '>=', '<='],
            "BP": ['==', '!=', '>>', '<<', '>=', '<='],
            "Types": ['~', '!~'],
            "Base": ['==', '!=', '>>', '<<', '>=', '<='],
            "Fire": ['==', '!=', '>>', '<<', '>=', '<='],
            "Air": ['==', '!=', '>>', '<<', '>=', '<='],
            "Earth": ['==', '!=', '>>', '<<', '>=', '<='],
            "Water": ['==', '!=', '>>', '<<', '>=', '<='],
            "Ability": ['~', '!~'],
            "Unique": ['==', '!=']
            },
        "battlegear": {
            "Name": ['==', '!=', '~', '!~', '!*', '*'],
            "Set": ['==', '!=', '~', '!~', '!*', '*'],
            "Rarity": ['==', '!=', '~', '!~'],
            "ID": ['==', '!=', '>>', '<<', '>=', '<='],
            "Types": ['~', '!~'],
            "Ability": ['~', '!~'],
            "Unique": ['==', '!='],
            "Loyal": ['==', '!=', '*', '!*'],
            "Legendary": ['==', '!=']
            },
        "creature": {
            "Name": ['==', '!=', '~', '!~', '!*', '*'],
            "Set": ['==', '!=', '~', '!~', '!*', '*'],
            "Rarity": ['==', '!=', '~', '!~'],
            "ID": ['==', '!=', '>>', '<<', '>=', '<='],
            "Types": ['~', '!~'],
            "Tribe": ['==', '!='],
            "Courage": ['==', '!=', '>>', '<<', '>=', '<='],
            "Power": ['==', '!=', '>>', '<<', '>=', '<='],
            "Wisdom": ['==', '!=', '>>', '<<', '>=', '<='],
            "Speed": ['==', '!=', '>>', '<<', '>=', '<='],
            "Energy": ['==', '!=', '>>', '<<', '>=', '<='],
            "Mugicians": ['==', '!=', '>>', '<<', '>=', '<='],
            "Elements": ['~', '!~'],
            "Ability": ['~', '!~'],
            "Brainwashed": ['~', '!~'],
            "Unique": ['==', '!='],
            "Loyal": ['==', '!=', '*', '!*'],
            "Legendary": ['==', '!=']
            },
        "location": {
            "Name": ['==', '!=', '~', '!~', '!*', '*'],
            "Set": ['==', '!=', '~', '!~', '!*', '*'],
            "Rarity": ['==', '!=', '~', '!~'],
            "ID": ['==', '!=', '>>', '<<', '>=', '<='],
            "Types": ['~', '!~'],
            "Initiative": ['~', '!~'],
            "Ability": ['~', '!~'],
            "Unique": ['==', '!=']
            },
        "mugic": {
            "Name": ['==', '!=', '~', '!~', '!*', '*'],
            "Set": ['==', '!=', '~', '!~', '!*', '*'],
            "Rarity": ['==', '!=', '~', '!~'],
            "ID": ['==', '!=', '>>', '<<', '>=', '<='],
            "Cost": ['==', '!=', '>>', '<<', '>=', '<='],
            "Tribe": ['==', '!='],
            "Types": ['~', '!~'],
            "Ability": ['~', '!~'],
            "Unique": ['==', '!=']
            },
        "card": ['==', '!=']
        }

syntax = f"""Syntax:
{sys.argv[0]} --search '[key][comparitor][value]'
Note: the [key][comparitor][value] MUST be in single-quotes. Bash does not
handle this well otherwise due to the presence of reserved symbols.

comparitor is one of:
        =   Is
        !=  Is not
        >   Greater than
        <   Less than
        >=  Greater than or equal to
        <=  Less than or equal to
        ~   Contains
        !~  Does not contain
        *   Matches regex
        !*  Does not match regex
Note: not all comparitors work with each key

key can be one of:
    Attack keys: {squash_dict_of_list('		', keys['attack'])}
    Battlegear keys: {squash_dict_of_list('		', keys['battlegear'])}
    Creature keys: {squash_dict_of_list('		', keys['creature'])}
    Location keys: {squash_dict_of_list('		', keys['location'])}
    Mugic keys: {squash_dict_of_list('		', keys['mugic'])}

Additionally, you can filter for card type:
    'card=Attack'
"""

if len(sys.argv) < 2 or sys.argv[1] == "--help":
    print(syntax)
    exit(1)

if sys.argv[1] != "--search" or len(sys.argv) < 3:
    print(f"Incorrect invocation: {' '.join(sys.argv[1:])}\n{syntax}")
    exit(1)

with open('cards.json', 'r') as cards_json:
    cards = json.loads(cards_json.read())

comparitors_escaped = [re.escape(c) for c in comparitors]
splitter = re.compile(f"({'|'.join(comparitors_escaped)})")
args = []
for i, arg in enumerate(sys.argv[2:]):
    arg_split = splitter.split(arg)
    for comparitor in comparitors:
        if comparitor in arg_split:
            args.append(arg_split)

sections_without_results = []
for arg in args:
    if arg[0] == 'card':
        pop = []
        if arg[1] == keys['card'][0]:
            for card_type in cards:
                if card_type != arg[2]:
                    pop.append(card_type)
        else:
            for card_type in cards:
                if card_type == arg[2]:
                    pop.append(card_type)
        for card_type in pop:
            cards.pop(card_type)
    else:
        cards_to_elim = {
                "attack": [],
                "battlegear": [],
                "creature": [],
                "location": [],
                "mugic": []
                }
        print(f"{arg}")
        for card_type in cards:
            print(f"{card_type}")
            print("Got here 1")
            if arg[0] in keys[card_type]:
                print("Got here 2")
                if arg[1] in keys[card_type][arg[0]]:
                    print("Got here 3")
                    for card in cards[card_type]:
                        if arg[1] == '==':
                            if card[arg[0]] != arg[2]:
                                cards_to_elim[card_type].append(card)
                        elif arg[1] == '!=':
                            if card[arg[0]] == arg[2]:
                                cards_to_elim[card_type].append(card)
                        elif arg[1] == '>>':
                            if card[arg[0]] <= arg[2]:
                                cards_to_elim[card_type].append(card)
                        elif arg[1] == '<<':
                            if card[arg[0]] >= arg[2]:
                                cards_to_elim[card_type].append(card)
                        elif arg[1] == '>=':
                            if card[arg[0]] < arg[2]:
                                cards_to_elim[card_type].append(card)
                        elif arg[1] == '<=':
                            if card[arg[0]] > arg[2]:
                                cards_to_elim[card_type].append(card)
                        elif arg[1] == '~':
                            if arg[2] not in card[arg[0]]:
                                print(f"{arg[2]} - {card[arg[0]]}")
                                cards_to_elim[card_type].append(card)
                        elif arg[1] == '!~':
                            if arg[2] in card[arg[0]]:
                                cards_to_elim[card_type].append(card)
                        elif arg[1] == '*':
                            pass
                        elif arg[1] == '!*':
                            pass

                    for card_type in cards_to_elim:
                        for card_cards_to_elim in cards_to_elim[card_type]:
                            for card in cards[card_type]:
                                if card_cards_to_elim["Name"] == card["Name"]:
                                    cards[card_type].remove(card)
            else:
                if card_type not in sections_without_results:
                    sections_without_results.append(card_type)

cards = {section:cards[section] for section in cards if section not in sections_without_results}

for card_type in cards:
    for card in cards[card_type]:
        print(f"{card['Name']}")
        for stat in card:
            if stat != "Name":
                print(textwrap.indent(f"{stat}: {card[stat]}", '    '))

