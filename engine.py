from time import time
from random import random

from api import Api
from ingame import InGame
from selmoteur import SelEngine


class Engine(InGame, Api, SelEngine):
    """
    engine code: https://www.jeu-tarot-en-ligne.com/Memos/IMPJCCFR__1.4.3.7.5.6.js
    A port of the original js engine in python
    """
    codeVersion = "0.0.0.0.3"

    def __init__(self, client: str, password: str):
        Api.__init__(self, client, password)
        InGame.__init__(self)
        SelEngine.__init__(self)

    def search_rooms(self) -> str:
        print("[searching rooms]")
        payload = {
            "etape": "start",
        }
        self.send_request("partiesEnCours.php", payload)

    def join_room(self, is_multiplayer: bool = True, has_player: int = 3):
        if is_multiplayer:
            game_type = "CPU{}"
            if not (4 <= has_player <= 5):
                has_player = 3

        else:
            game_type = "Libre{}"
            if not (3 <= has_player <= 6):
                has_player = 3

        game_mode = game_type.format(has_player)
        uid_game = round(random() * 999999)
        scr_num = f"scr{round(time())}"
        payload = {
            "CV": self.codeVersion,
            "etape": "start",
            "modeJeu": game_mode,
            "s": scr_num,
            "uidG": uid_game,
            "gameMode": game_mode
        }
        self.send_request("jeu.php", payload)

    def send_request(self, endpoint: str, payload: dict):
        with self.session.post(self.url.format(endpoint), data=payload) as r:
            self.on_response(r.text)

    def on_response(self, response: str):
        do_methods = []
        actions = response.splitlines()
        for action in actions:
            sub_actions = action.split(";")
            for sub in sub_actions:
                if sub.strip():
                    do_methods.append(sub.strip())
