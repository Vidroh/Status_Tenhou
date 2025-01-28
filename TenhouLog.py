import requests
import urllib.parse

def get_log(log):

    ENDPOINT = "https://tenhou.net/5/mjlog2json.cgi?"

    HEADERS = {
        "User-Agent": "Sexo :O",
        "Referer": f"https://tenhou.net/5/?log={log}&tw=0"
    }

    response = requests.get(f'{ENDPOINT}{log}', headers=HEADERS)
    data = response.json()
    return data

def get_lobby_log(id_lobby):

    ENDPOINT = "https://nodocchi.moe/api/lobby.php?lobby="

    response = requests.get(f'{ENDPOINT}{id_lobby}')
    data = response.json()
    return data

def get_historico(nick):

    ENDPOINT = "https://nodocchi.moe/api/listuser.php?name="
    d = urllib.parse.quote(nick)

    response = requests.get(f'{ENDPOINT}{d}')
    data = response.json()
    return data