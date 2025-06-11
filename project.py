import math
import time
import random
import requests
import re
import sys

class cardretriever:
    def __init__(self, carddata):
        try:
            carddata['card_faces'][0]['object'] == "card_face"
            faces = 2
        except KeyError:
            faces = 1
        self.faces = faces

        try:
            cardname = "Name: " + carddata['name']
        except KeyError:
            sys.exit("There was an issue finding the card name from Scryfall...exiting..")
        self.cardname = cardname

        cardtype, scryfall_uri = carddata['type_line'],carddata['scryfall_uri']
        self.cardtype, self.scryfall_uri = cardtype, scryfall_uri
        try:
            edhrec = "EDHRec Rank: " + str(carddata['edhrec_rank'])
        except KeyError:
            edhrec = "EDHRec Rank: Not Found"

        self.edhrec = edhrec
        
        if faces == 1:
            try:
                color_identity = "Color Identity: " + str(carddata['color_identity'])
            except KeyError:
                color_identity = "Color Identity: Not Found"
            try:
                manacost = "Mana Cost: " + carddata['mana_cost']
            except KeyError:
                manacost = "Mana Cost: Not Found"
            try:
                oracle = carddata['oracle_text']
            except KeyError:
                oracle = "Oracle Text Not Found" 
            try:
                powertoughness = "Power/Toughness: " + carddata['power'] + "/" + carddata['toughness']
            except KeyError:
                powertoughness = "Power/Toughness: Not Found"
            self.color_identity = color_identity
            self.mana_cost = manacost
            self.oracle = oracle
            self.powertoughness = powertoughness

        elif faces == 2:
            try:
                color_identity_one = carddata['color_identity'][0]
            except KeyError:
                color_identity_one = ""
            try:
                color_identity_two = carddata['color_identity'][1]
            except KeyError:
                color_identity_two = ""
            if color_identity_one == "" and color_identity_two == "":
                color_identity = "Color Identity: Not Found"
            else:
                color_identity = "Color Identity: " + color_identity_one + color_identity_two
            try:
                mana_cost_one = "Mana Cost: " + carddata['card_faces'][0]['mana_cost']
            except KeyError:
                mana_cost_one = "Mana Cost: Not Found"
            try:
                mana_cost_two = "Mana Cost: " + carddata['card_faces'][1]['mana_cost']
            except KeyError:
                mana_cost_two = "Mana Cost: Not Found"
            try:
                card_type_one = carddata['card_faces'][0]['type_line']
            except KeyError:
                card_type_one = "Card Type: Not Found"
            try:
                card_type_two = carddata['card_faces'][1]['type_line']
            except KeyError:
                card_type_two = "Card Type: Not Found"
            try:
                oracle_one = carddata['card_faces'][0]['oracle_text']
            except KeyError:
                oracle_one = "Oracle Text: Not Found"
            try:
                oracle_two = carddata['card_faces'][1]['oracle_text']
            except KeyError:
                oracle_two = "Oracle Text: Not Found"            
            try:
                powertoughness_one = "Power/Toughness: " + carddata['card_faces'][0]['power'] + "/" + carddata['card_faces'][0]['toughness']
            except KeyError:
                powertoughness_one = "Power/Toughness: Not Found"       
            try:
                powertoughness_two = "Power/Toughness: " + carddata['card_faces'][1]['power'] + "/" + carddata['card_faces'][1]['toughness']
            except KeyError:
                powertoughness_two = "Power/Toughness: Not Found"

            self.color_identity = color_identity
            self.mana_cost_one = mana_cost_one
            self.mana_cost_two = mana_cost_two
            self.card_type_one = card_type_one
            self.card_type_two = card_type_two
            self.oracle_one = oracle_one
            self.oracle_two = oracle_two
            self.powertoughness_one = powertoughness_one
            self.powertoughness_two = powertoughness_two
        else:
            sys.exit("An issue obtaining card data has occurred...exiting.")

    def __str__(self):
        if self.faces == 1:
            return f"""
            {self.cardname}
            {self.edhrec}
            {self.color_identity}
            {self.mana_cost}
            {self.cardtype}
            {"-" * len(self.cardtype)}
            {self.oracle}
            {"-" * len(self.cardtype)}
            {self.powertoughness}
            {self.scryfall_uri}
            """
        if self.faces == 2:
            return f"""
            {self.cardname}
            {self.edhrec}
            {self.color_identity}
            {self.cardtype}
            
            ---Side One---
            {self.mana_cost_one}
            {"-" * len(self.card_type_one)}
            {self.oracle_one}
            {"-" * len(self.card_type_one)}
            {self.powertoughness_one}

            ---Side Two---
            {self.mana_cost_two}
            {"-" * len(self.card_type_two)}
            {self.oracle_one}
            {"-" * len(self.card_type_two)}
            {self.powertoughness_one}            

            {self.scryfall_uri}
            """
        else:
            sys.exit("An error has occurred retrieving card data...exiting.")

class edhrecdata:
    def __init__(self, edhreclink, themedata):
        self.edhreclink = edhreclink
        self.themedata = themedata
        #return ([themedata[0]['value'], themedata[0]['count']],[themedata[1]['value'], themedata[1]['count']],[themedata[2]['value'], themedata[2]['count']], edhreclink)
        try:
            theme1 = "Theme 1: " + themedata[0]['value']
            count1 = "No. Decks: " + str(themedata[0]['count'])
        except KeyError:
            theme1 = ""
            count1 = ""
        try:
            theme2 = "Theme 2: " + themedata[1]['value']
            count2 = "No. Decks: " + str(themedata[1]['count'])
        except KeyError:
            theme2 = ""
            count2 = ""
        try:
            theme3 = "Theme 3: " + themedata[2]['value']
            count3 = "No. Decks: " + str(themedata[2]['count'])
        except KeyError:
            theme3 = ""
            count3 = ""            
        self.theme1 = theme1
        self.theme2 = theme2
        self.theme3 = theme3
        self.count1 = count1
        self.count2 = count2
        self.count3 = count3

    def __str__(self):
        return f"""
        ---EDHREC---
        EDHRec Link: {self.edhreclink}
        {self.theme1}
            {self.count1}
        {self.theme2}
            {self.count2}
        {self.theme3}
            {self.count3}
        """

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
    r = requests.get(url)
    response = r.json()
    carddata = response['data'][0]
    scryfall_uri = carddata['scryfall_uri']
    edhrecresponse = get_edhrec(scryfall_uri)

    cardoutput = cardretriever(carddata)

    totaloutput = f"""
    {cardoutput}

    {edhrecresponse}
    """

    return totaloutput

def get_edhrec(scryfall_uri):

    card_error = 403
    print(scryfall_uri)
    cardname = re.search(r'\d/([a-z|\-]*)', scryfall_uri).group(1)
    if cardname[:2] == "A-":
        cardname = cardname[2:]
    edhrecnamelist = cardname.split("-")
    loop_attempt = 1
    max_loop = len(edhrecnamelist)

    while card_error == 403:
        if loop_attempt > max_loop:
            return f"EDHRec attempt failed at loop attempt {loop_attempt}"
        edhrecname = "-".join(edhrecnamelist[:loop_attempt])
        url = "https://json.edhrec.com/pages/commanders/" + edhrecname + ".json"
        print(url)
        r = requests.get(url)
        card_error = r.status_code
        print(card_error)
        loop_attempt += 1


    response = r.json()
    try:
        themedata = response['panels']['taglinks']
    except KeyError:
        return ""
    edhreclink = "https://edhrec.com/commanders/"+cardname
    return edhrecdata(edhreclink, themedata)

if __name__ == "__main__":
    main()
