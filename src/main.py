"""Main file to run challenge of talana kombat"""

import re
import logging
from itertools import groupby
from fastapi import FastAPI, HTTPException
from models import MoveRequest, MoveResponse

logging.basicConfig(level=logging.INFO)

class TalanaKombat():
    """ Class used to analice a match """
    def __init__(self):
        self.p1_energy = 6
        self.p2_energy = 6
        self.full_description = ""
        self.first_player = "player1"

    def set_first_player(self, p1_movements, p1_hit, p2_movements, p2_hit):
        """ Get player that should move first """
        p1_buttons = len(p1_movements) + len(p1_hit)
        p2_buttons = len(p2_movements) + len(p2_hit)

        if (p1_buttons > p2_buttons
            or (p1_buttons == p2_buttons and len(p1_hit) > len(p2_hit))):
            self.first_player = "player2"
            return "player2"

        return "player1"



    def get_hit_description(self, player, movement_inputs, hit) -> dict:
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

    def get_movement_description(self, player, movement_inputs) -> str:
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

    def get_turn_description(self, player, movement_inputs, hit) -> str:
        """ Show full description of a player turn """
        hit_description = self.get_hit_description(player, movement_inputs, hit)
        movement_description = self.get_movement_description(player,
                                                             hit_description["previous_movements"])

        # TODO: "se queda inmóvil" solo aparece si NO se da un hit
        # TODO: no se muestra hit_description si no hay daño
        return f"{player} {movement_description} y {hit_description['name']}"

app = FastAPI()

@app.post("/start", response_model=MoveResponse, tags=["Talana Kombat by Jorge Caullán"])
def start_fight(move_request: MoveRequest) -> MoveResponse:
    """ Start a fight of a json file, show fight details and return winner """

    # game = TalanaKombat()
    try:
        # # upcase inputs and remove characters different than WASD
        # movement_inputs = re.sub(r'[^WASD]', '', movement_inputs.upper())

        for player, details in move_request.dict().items():
            for movimiento, golpe in zip(details['movimientos'], details['golpes']):
                movements_result += f"{player}, {movimiento}, {golpe}\n"
        return MoveResponse(
            details=movements_result,
            winner='You win',
            warnings=[],
        )
    except Exception as e:
        logging.error("Error processing request: %s", e)
        detail = "An error occurred while processing the request"
        raise HTTPException(status_code=500, detail=detail) from e

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
