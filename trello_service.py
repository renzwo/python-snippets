import requests

# Zuerst hier registrieren: https://trello.com/signup
# Dann diesen Schlüssel als api_key in den Einstellungen setzen: https://trello.com/app-key
# Unter dem Schlüssel steht ein Text: "Wenn Sie vorhaben, eine Anwendung für sich selbst zu erstellen, oder lokal testen, können Sie manuell ein Token erstellen."
# In diesem Text das Wort "Token" anklicken, welches als Link hinterlegt ist, auf "Erlauben" drücken und den Token der erscheint in den Einstellungen unter api_token eintragen
# Danach in den Einstellungen trello->activate auf "true" setzen
# Alle Infos findet man auch hier: https://developer.atlassian.com/cloud/trello/guides/rest-api/authorization/

board_name = "My board"

def get_board_id(trellosettings):
    url = "https://api.trello.com/1/members/me/boards?fields=name,url&key=" + trellosettings["api_key"] + "&token=" + trellosettings["api_token"]
    response = requests.request("GET", url)
    json_board_list = response.json()
    for board in json_board_list:
        if board["name"] == board_name:
            return board["id"]
    raise Exception("Board '" + board_name + "' wurde nicht gefunden.")


def create_board(trellosettings):
    url = "https://api.trello.com/1/boards/"
    querystring = {"name": board_name, "key": trellosettings["api_key"], "token": trellosettings["api_token"]}
    response = requests.request("POST", url, params=querystring)
    board_id = response.json()["shortUrl"].split("/")[-1].strip()
    return board_id


def get_board_list_id(trellosettings, board_id, list_name):
    url = "https://api.trello.com/1/boards/" + board_id + "/lists?key=" + trellosettings["api_key"] + "&token=" + trellosettings["api_token"]
    response = requests.request("GET", url)
    json_lists_list = response.json()
    for list_element in json_lists_list:
        if list_element["name"] == list_name:
            return list_element["id"]
    raise Exception("Board Liste '" + list_name + "' wurde nicht gefunden.")


def check_if_card_exists(trellosettings, board_id, card_name):
    url = "https://api.trello.com/1/boards/" + board_id + "/cards?key=" + trellosettings["api_key"] + "&token=" + trellosettings["api_token"]
    response = requests.request("GET", url)
    json_card_list = response.json()
    for card in json_card_list:
        if card["name"] == card_name:
            raise Exception("Board Card '" + card_name + "' wurde gefunden.")


def get_card_id(trellosettings, board_id, card_name):
    url = "https://api.trello.com/1/boards/" + board_id + "/cards?key=" + trellosettings["api_key"] + "&token=" + trellosettings["api_token"]
    response = requests.request("GET", url)
    json_card_list = response.json()
    for card in json_card_list:
        if card["name"] == card_name:
            return card["id"]
    raise Exception("Board Card '" + card_name + "' wurde nicht gefunden.")


def create_new_contact_card(card_name, list_name, trellosettings):

    if not trellosettings["activate"]:
        print("Trello Integration nicht aktiviert.")
        return

    try:
        board_id = get_board_id(trellosettings)
    except:
        board_id = create_board(trellosettings)

    list_id = get_board_list_id(trellosettings, board_id, list_name)

    try:
        check_if_card_exists(trellosettings, board_id, card_name)
        url = "https://api.trello.com/1/cards"
        querystring = {"idList": list_id,
                       "key": trellosettings["api_key"],
                       "token": trellosettings["api_token"],
                       "name": card_name,
                       "desc": "some description",
                       "urlSource": "some url"
                    }
        requests.request("POST", url, params=querystring)
        print("Card '" + card_name + "' wurde angelegt.")
    except:
        print("Card '" + card_name + "' existiert bereits.")


def add_comment_to_card(trellosettings, card_id, comment):

    if not trellosettings["activate"]:
        print("Trello Integration nicht aktiviert.")
        return

    url = "https://api.trello.com/1/cards/" + card_id + "/actions/comments"
    querystring = {"id": card_id,
                   "key": trellosettings["api_key"],
                   "token": trellosettings["api_token"],
                   "text": comment
                   }
    requests.request("POST", url, params=querystring)


def move_contact_card(card_name, list_name, messages, trellosettings):

    if not trellosettings["activate"]:
        print("Trello Integration nicht aktiviert.")
        return

    board_id = get_board_id(trellosettings)
    card_id = get_card_id(trellosettings, board_id, card_name)

    for messagekey in messages.keys():
        add_comment_to_card(trellosettings, card_id, messagekey + ": " + messages[messagekey])

    url = "https://api.trello.com/1/cards/" + card_id
    querystring = {"id": card_id,
                   "key": trellosettings["api_key"],
                   "token": trellosettings["api_token"],
                   "idList": get_board_list_id(trellosettings, board_id, list_name)
                   }
    requests.request("PUT", url, params=querystring)
    print("Card '" + card_name + "' wurde in die Liste verschoben.")
