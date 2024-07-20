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

    def get_hit_description(self, player, movement_inputs, hit):
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

        return {"damage": 0, "name": "no golpea", "previous_movements": movement_inputs}

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
            }
        }

        # upcase inputs, remove characters different than WASD
        movement_inputs = re.sub(r'[^WASD]', '', movement_inputs.upper())
        # remove consecutive characters
        movement_inputs = ''.join(key for key, _ in groupby(movement_inputs))
        if movement_inputs in descriptions["default"]:
            movement_description = descriptions["default"][movement_inputs]
        elif player in descriptions and movement_inputs in descriptions[player]:
            movement_description = descriptions[player][movement_inputs]
        else:
            movement_description = "se mueve"

        response = f"{player} {movement_description}"
        return response

app = FastAPI()

@app.post("/start", response_model=MoveResponse, tags=["Talana Kombat by Jorge Caullán"])
def start_fight(move_request: MoveRequest) -> MoveResponse:
    """ Start a fight of a json file, show fight details and return winner """

    # game = TalanaKombat()
    try:
        movements_result = ""
        for player, details in move_request.dict().items():
            for movimiento, golpe in zip(details['movimientos'], details['golpes']):
                movements_result += f"{player}, {movimiento}, {golpe}\n"
        return MoveResponse(
            details=movements_result,
            winner='You win',
            warnings=['No warnings'],
        )
    except Exception as e:
        logging.error("Error processing request: %s", e)
        detail = "An error occurred while processing the request"
        raise HTTPException(status_code=500, detail=detail) from e

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
