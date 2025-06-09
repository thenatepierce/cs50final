import math
import time
import random
import requests
import re


def main():

    colors = get_colors()
    commander = get_commander(colors)
    print(get_commander_info(commander))


def get_colors():

    colors = {"w","u","b","r","g","c"}
    user_colors = "x"

    while set(user_colors).issubset(colors) == False:
        user_colors = str(input("What colors are you interested in (expressed in wubrgc)? "))

        if set(user_colors).issubset(colors) == False:
            print("Please enter colors in wubrgc format")

    # Case: only c is used
    if user_colors == "c":
        return "+id=0"

    # Case: colors and colorless are used
    elif "c" in user_colors:
        user_colors = re.sub("c", "", user_colors)
        return "+(id<=" + user_colors + " or id=0)"

    # Case: w,u,b,r, or g and not c is used
    else:
        return "+(id<=" + user_colors + ")"


def get_commander(colors):

    commanders = []
    j = 1
    r_prefix = "https://api.scryfall.com/cards/search?format=json&include_extras=false&include_multilingual=false&include_variations=false&order=name&unique=cards&page="
    r_suffix = "&q=is%3Acommander"
    url = r_prefix + str(j) + r_suffix + colors
    r = requests.get(url)

    response = r.json()
    total_cards = response["total_cards"]
    pages = math.ceil(int(total_cards) / 175)


    while j < pages + 1:
        print("Querying Scryfall...")
        url = r_prefix + str(j) + r_suffix + colors
        #print(url)
        rq = requests.get(url)
        rq_response = rq.json()
        for i in rq_response["data"]:
            commanders.append(i["name"])
        j += 1
        time.sleep(1/10)

    valid_commander = False

    while valid_commander != True:
        commander_choice = random.randrange(0, len(commanders))
        valid_commander = validate_commander(commanders[commander_choice])

    return commanders[commander_choice]

def validate_commander(commander):
    r_prefix = "https://api.scryfall.com/cards/search?format=json&include_extras=false&include_multilingual=false&include_variations=false&order=name&unique=cards&q="
    url = r_prefix + commander
    print(url)
    r = requests.get(url)
    response = r.json()
    carddata = response['data'][0]
    if carddata['legalities']['commander'] == "legal" and carddata['type_line'] != "Legendary Enchantment — Background":
        return True
    else:
        print("Not-legal commander randomly chosen")
        return False

def get_commander_info(commander):
    print("\n" + commander + " has been chosen!  Querying Scryfall for details")
    r_prefix = "https://api.scryfall.com/cards/search?format=json&include_extras=false&include_multilingual=false&include_variations=false&order=name&unique=cards&q="
    url = r_prefix + commander
    print(url)
    r = requests.get(url)
    response = r.json()
    carddata = response['data'][0]
    cardname, cardtype, scryfall_uri = carddata['name'], carddata['type_line'], carddata['scryfall_uri']

    try:
        edhrec = str(carddata['edhrec_rank'])
    except KeyError:
        edhrec = "n/a"

    edhrecresponse = get_edhrec(scryfall_uri)

    try:
        carddata['card_faces'][0]['object'] == "card_face"
        faces = 2
    except KeyError:
        faces = 1

    if faces == 1:
        color_identity = carddata['color_identity']
        manacost = carddata['mana_cost']
        oracle = carddata['oracle_text']
        power = carddata['power']
        toughness = carddata['toughness']
        scryfall_output = f"""
        Name: {cardname}
        EDHRec Rank: {edhrec}
        Color Identity: {color_identity}
        Mana Cost: {manacost}
        {cardtype}
        {"-" * len(cardtype)}
        {oracle}
        {"-" * len(cardtype)}
        Power/Toughness: {power}/{toughness}
        Scryfall URL: {scryfall_uri}

        ---EDHREC---
        EDHRec Link: {edhrecresponse[3]}
        Theme1: {edhrecresponse[0][0]}
        Decks: {edhrecresponse[0][1]}
        Theme2: {edhrecresponse[1][0]}
        Decks: {edhrecresponse[1][1]}
        Theme3: {edhrecresponse[2][0]}
        Decks: {edhrecresponse[2][1]}
        """
        return scryfall_output

    elif faces == 2:
        color_identity = carddata['color_identity'][0] + carddata['color_identity'][1]
        face_one, face_two = carddata['card_faces'][0],carddata['card_faces'][1]
        name_one, name_two = face_one['name'], face_two['name']
        mana_cost_one = face_one['mana_cost']
        try:
            mana_cost_two = face_two['mana_cost']
        except KeyError:
            mana_cost_two = ""
        oracle_one, oracle_two = face_one['oracle_text'], face_two['oracle_text']
        cardtype_one, cardtype_two = face_one['type_line'], face_two['type_line']
        power_one, toughness_one = face_one['power'], face_one['toughness']
        try:
            power_two = face_two['power']
            toughness_two = face_two['toughness']
        except KeyError:
            power_two = ""
            toughness_two = ""
        scryfall_output = f"""
        Name: {cardname}
        EDHRec Rank: {edhrec}
        Color Identity: {color_identity}
        Card Type: {cardtype}
        --- Side One---
        Name: {name_one}
        Mana Cost: {mana_cost_one}
        {cardtype_one}
        {"-" * len(cardtype_one)}
        {oracle_one}
        {"-" * len(cardtype_one)}
        Power/Toughness: {power_one}/{toughness_one}

        --- Side Two---
        Name: {name_two}
        Mana Cost: {mana_cost_two}
        {cardtype_two}
        {"-" * len(cardtype_two)}
        {oracle_two}
        {"-" * len(cardtype_two)}
        Power/Toughness: {power_two}/{toughness_two}

        Scryfall URL: {scryfall_uri}

        ---EDHREC---
        EDHRec Link: {edhrecresponse[3]}
        Theme1: {edhrecresponse[0][0]}
            Decks: {edhrecresponse[0][1]}
        Theme2: {edhrecresponse[1][0]}
            Decks: {edhrecresponse[1][1]}
        Theme3: {edhrecresponse[2][0]}
            Decks: {edhrecresponse[2][1]}
        """
        return scryfall_output

def get_edhrec(scryfall_uri):

    card_error = "403"

    while card_error == "403":
        cardname = re.search(r'\d/([a-z|\-]*)', scryfall_uri).group(1)
        print(cardname)
        if cardname[:2] == "A-":
            cardname = cardname[2:]
        url = "https://json.edhrec.com/pages/commanders/" + cardname + ".json"
        r = requests.get(url)
        card_error = r.status_code

    response = r.json()
    themedata = response['panels']['taglinks']
    edhreclink = "https://edhrec.com/commanders/"+cardname

    return ([themedata[0]['value'], themedata[0]['count']],[themedata[1]['value'], themedata[1]['count']],[themedata[2]['value'], themedata[2]['count']], edhreclink)


if __name__ == "__main__":
    main()
