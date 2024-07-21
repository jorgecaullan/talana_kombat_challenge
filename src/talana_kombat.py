""" Class with required data to play a game of Talana Kombat """

import re
from typing import List
from itertools import groupby

def fill_list(lst, required_length):
    """ Fill a list with empty strings and replace not string values """
    # replace not string values
    fixed_list = [(str(item) if isinstance(item, str) else "") for item in lst]
    # fill list to make it have same length than required
    return fixed_list + [""] * (required_length - len(lst))


class TalanaKombat():
    """ Class used to analice a match """

    def __init__(self, full_json: dict):
        self.players = {
            "player1": {
                "name": "Tonyn",
                "energy": 6
            },
            "player2": {
                "name": "Arnaldor",
                "energy": 6
            }
        }
        self.full_description = ""
        self.winner = ""

        # fix dict input in case it was needed
        player1 = full_json.get("player1", {"movimientos": [], "golpes": []})
        player2 = full_json.get("player2", {"movimientos": [], "golpes": []})

        if not isinstance(player1, dict):
            player1 = {"movimientos": [], "golpes": []}
        if not isinstance(player2, dict):
            player2 = {"movimientos": [], "golpes": []}

        max_length = max(len(player1.get("movimientos", [])),
                         len(player1.get("golpes", [])),
                         len(player2.get("movimientos", [])),
                         len(player2.get("golpes", [])))

        # fill lists with required max lengths
        player1["movimientos"] = fill_list(player1.get("movimientos", []), max_length)
        player1["golpes"] = fill_list(player1.get("golpes", []), max_length)
        player2["movimientos"] = fill_list(player2.get("movimientos", []), max_length)
        player2["golpes"] = fill_list(player2.get("golpes", []), max_length)

        self.full_json = {"player1": player1, "player2": player2}

        self.set_first_player()


    def set_first_player(self) -> str:
        """ Get player that should move first """
        if len(self.full_json["player1"]["movimientos"]) == 0:
            self.first_player = "player1"
            self.second_player = "player2"
            return "player1"

        p1_movements = self.full_json["player1"]["movimientos"][0]
        p1_hit = self.full_json["player1"]["golpes"][0]
        p2_movements = self.full_json["player2"]["movimientos"][0]
        p2_hit = self.full_json["player2"]["golpes"][0]

        p1_buttons = len(p1_movements) + len(p1_hit)
        p2_buttons = len(p2_movements) + len(p2_hit)

        if (p1_buttons > p2_buttons
            or (p1_buttons == p2_buttons and len(p1_hit) > len(p2_hit))):
            self.first_player = "player2"
            self.second_player = "player1"
            return "player2"

        self.first_player = "player1"
        self.second_player = "player2"
        return "player1"


    def get_hit_description(self, player: str, movement_inputs: List[str], hit: List[str]) -> dict:
        """ Return damage, name of used movement and if exist some previous movement inputs """
        combinations = {
            "Tonyn": {
                "P": { "DSD": { "damage": 3, "name": "conecta un Taladoken" } },
                "K": { "SD": { "damage": 2, "name": "conecta un Remuyuken" } },
            },
            "Arnaldor": {
                "K": { "SA": { "damage": 3, "name": "conecta un Remuyuken" } },
                "P": { "ASA": { "damage": 2, "name": "conecta un Taladoken" } },
            }
        }

        # validate combinations of player
        if (player in combinations
            and hit in combinations[player]):
            if movement_inputs[-3:] in combinations[player][hit]:
                result = combinations[player][hit][movement_inputs[-3:]]
                result["previous_movements"] = movement_inputs[:-3]
                return result
            if movement_inputs[-2:] in combinations[player][hit]:
                result = combinations[player][hit][movement_inputs[-2:]]
                result["previous_movements"] = movement_inputs[:-2]
                return result

        # set damage on case of not match combinations
        if hit == "P":
            return {"damage": 1, "name": "da un puñetazo", "previous_movements": movement_inputs}
        if hit == "K":
            return {"damage": 1, "name": "da una patada", "previous_movements": movement_inputs}

        return {"damage": 0, "name": "", "previous_movements": movement_inputs}


    def get_movement_description(self, player: str, movement_inputs: List[str]) -> str:
        """ Check if arguments should be a special movement_inputs or just movement """
        descriptions = {
            "default": {
                "": "se queda inmóvil",
                "W": "salta",
                "S": "se agacha",
            },
            "Tonyn": {
                "A": "retrocede",
                "D": "avanza",
                "WA": "salta hacia atrás",
                "AW": "salta hacia atrás",
                "WD": "salta hacia adelante",
                "DW": "salta hacia adelante",
            },
            "Arnaldor": {
                "D": "retrocede",
                "A": "avanza",
                "WD": "salta hacia atrás",
                "DW": "salta hacia atrás",
                "WA": "salta hacia adelante",
                "AW": "salta hacia adelante",
            }
        }
        # remove consecutive characters
        movement_inputs = ''.join(key for key, _ in groupby(movement_inputs))
        if movement_inputs in descriptions["default"]:
            movement_description = descriptions["default"][movement_inputs]
        elif player in descriptions and movement_inputs in descriptions[player]:
            movement_description = descriptions[player][movement_inputs]
        else:
            movement_description = "se mueve"

        return movement_description


    def get_turn_description(self, player: str, movement_inputs: list, hit: list) -> str:
        """ Show full description of a player turn """
        player_name = self.players[player]["name"]
        hit_description = self.get_hit_description(player_name, movement_inputs, hit)
        movement_description = self.get_movement_description(player_name,
                                                             hit_description["previous_movements"])

        # no hit_description shown if no damage
        if hit_description['damage'] == 0:
            description = f"{player_name} {movement_description}\n"
            self.full_description += description
            return description

        # reduce respective player life
        if player == "player1":
            self.players["player2"]["energy"] -= hit_description['damage']
        else:
            self.players["player1"]["energy"] -= hit_description['damage']

        # "se queda inmóvil" It only appears if a hit is NOT given
        if movement_description == "se queda inmóvil":
            description = f"{player_name} {hit_description['name']}\n"
            self.full_description += description
            return description

        description = f"{player_name} {movement_description} y {hit_description['name']}\n"
        self.full_description += description
        return description


    def play_turn(self, turn: int) -> bool:
        """ Call turn descriptions in required order of players and return true on end of match """
        first_movements = self.full_json[self.first_player]["movimientos"][turn]
        # upcase inputs and remove characters different than WASD
        first_movements = re.sub(r'[^WASD]', '', first_movements.upper())
        first_hit = self.full_json[self.first_player]["golpes"][turn]

        # attack with first player
        self.get_turn_description(self.first_player, first_movements, first_hit)
        # check life of second player
        if self.players[self.second_player]["energy"] <= 0:
            self.end_game(True)
            return True

        second_movements = self.full_json[self.second_player]["movimientos"][turn]
        # upcase inputs and remove characters different than WASD
        second_movements = re.sub(r'[^WASD]', '', second_movements.upper())
        second_hit = self.full_json[self.second_player]["golpes"][turn]
        # attack with second player
        self.get_turn_description(self.second_player, second_movements, second_hit)
        # check life of first player
        if self.players[self.first_player]["energy"] <= 0:
            self.end_game(True)
            return True

        return False


    def end_game(self, from_ko: bool) -> None:
        """ Called when some player life is less or eq than 0 or time is out """
        # set winner and add message
        if from_ko:
            # life = 0
            if self.players["player1"]["energy"] <= 0:
                self.winner = self.players["player2"]["name"]
                life = self.players["player2"]["energy"]
            else:
                self.winner = self.players["player1"]["name"]
                life = self.players["player1"]["energy"]

            self.full_description += (f"KO! {self.winner} gana la pelea "
                                      f"y aun le queda {life} de energía")
        else:
            if self.players["player1"]["energy"] == self.players["player2"]["energy"]:
                self.winner = "Draw"
                life = self.players["player1"]["energy"]
                self.full_description += (f"Se acabó el tiempo! la pelea terminó en un Empate, "
                                        f"a ambos jugadores les queda {life} de energía")
                return

            if self.players["player1"]["energy"] > self.players["player2"]["energy"]:
                self.winner = self.players["player1"]["name"]
                winner_life = self.players["player1"]["energy"]
                loser_life = self.players["player2"]["energy"]
                loser = self.players["player2"]["name"]
            else:
                self.winner = self.players["player2"]["name"]
                winner_life = self.players["player2"]["energy"]
                loser_life = self.players["player1"]["energy"]
                loser = self.players["player1"]["name"]

            self.full_description += (f"Se acabó el tiempo! {self.winner} gana, "
                                      f"a quien le queda {winner_life} de energía vs a "
                                      f"{loser} a quien le queda {loser_life} de energía")
