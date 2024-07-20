"""Main file to run challenge of talana kombat"""

import logging
from fastapi import FastAPI, HTTPException
from models import MoveRequest, MoveResponse

logging.basicConfig(level=logging.INFO)

class TalanaKombat():
    """ Class with all required  """
    def __init__(self):
        self.p1_energy = 6
        self.p2_energy = 6

    def get_hit(self, player, movement_inputs, hit):
        """ Return damage and name of used movement """
        combinations = {
            "Tonyn": {
                "P": { "DSD": { "damage": 3, "name": "un Taladoken" } },
                "K": { "SD": { "damage": 2, "name": "un Remuyuken" } },
            },
            "Arnaldor": {
                "K": { "SA": { "damage": 3, "name": "un Remuyuken" } },
                "P": { "ASA": { "damage": 2, "name": "un Taladoken" } },
            }
        }

        if (player in combinations
            and hit in combinations[player]):
            if movement_inputs[-3:] in combinations[player][hit]:
                result = combinations[player][hit][movement_inputs[-3:]]
                result["previous_movements"] = movement_inputs[:-3]
                return result
            elif movement_inputs[-2:] in combinations[player][hit]:
                result = combinations[player][hit][movement_inputs[-2:]]
                result["previous_movements"] = movement_inputs[:-2]
                return result
        elif hit == "P":
            return {"damage": 1, "name": "un puñetazo", "previous_movements": movement_inputs}
        elif hit == "K":
            return {"damage": 1, "name": "una patada", "previous_movements": movement_inputs}
        else:
            return {"damage": 0, "name": "", "previous_movements": movement_inputs}

    def get_movement_description(self, player, movement_inputs, hit) -> str:
        """ Check if arguments should be a special movement_inputs or just movement """
        response = f"{player}, {movement_inputs}, {hit}"
        return response

app = FastAPI()

@app.post("/start", response_model=MoveResponse, tags=["Talana Kombat"])
def start_fight(move_request: MoveRequest) -> MoveResponse:
    """ Start a fight of a json file, show fight details and return winner """

    game = TalanaKombat()
    try:
        movements_result = ""
        for player, details in move_request.dict().items():
            for movimiento, golpe in zip(details['movimientos'], details['golpes']):
                movements_result += game.get_movement_description(player, movimiento, golpe) + "\n"
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
