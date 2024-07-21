"""Main file to run challenge of talana kombat"""

import logging
from fastapi import FastAPI, HTTPException
from models import MoveRequest, MoveResponse
from talana_kombat import TalanaKombat

app = FastAPI()

@app.post("/start", response_model=MoveResponse, tags=["Talana Kombat by Jorge Caullán"])
def start_fight(move_request: MoveRequest | dict) -> MoveResponse:
    """ Start a fight with a json file, return fight details and winner """

    try:
        # dict is accepted only to make more flexible
        input_dict = move_request
        # if its a MoveRequest, get a dict input
        if not isinstance(move_request, dict):
            input_dict = move_request.model_dump()
        game = TalanaKombat(input_dict)

        is_ended = False
        length = len(game.full_json["player1"]["movimientos"])
        for i in range(length):
            is_ended = game.play_turn(i)
            if is_ended:
                break

        if not is_ended:
            game.end_game(False)

        return MoveResponse(
            detail=game.full_description,
            winner=game.winner,
        )
    except Exception as e:
        logging.error("Error processing request: %s", e)
        detail = "An error occurred while processing the request"
        raise HTTPException(status_code=500, detail=detail) from e

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
