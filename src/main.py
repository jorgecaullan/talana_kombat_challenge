"""Main file to run challenge of talana kombat"""

import logging
from fastapi import FastAPI, HTTPException
from models import MoveRequest, MoveResponse
from talana_kombat import TalanaKombat

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.post("/start", response_model=MoveResponse, tags=["Talana Kombat by Jorge Caullán"])
def start_fight(move_request: MoveRequest) -> MoveResponse:
    """ Start a fight with a json file,
        return fight details, winner and warnings (in case they exist) """

    game = TalanaKombat()
    try:
        # # upcase inputs and remove characters different than WASD
        # movement_inputs = re.sub(r'[^WASD]', '', movement_inputs.upper())
        input_dict = move_request.model_dump()
        player1 = input_dict["player1"]
        p1_movements = player1["movimientos"]
        logging.info('p1_movements')
        logging.info(p1_movements)
        p1_hits = player1["golpes"]
        logging.info('p1_hits')
        logging.info(p1_hits)

        player2 = input_dict["player2"]
        p2_movements = player2["movimientos"]
        logging.info('p2_movements')
        logging.info(p2_movements)
        p2_hits = player2["golpes"]
        logging.info('p2_hits')
        logging.info(p2_hits)

        return MoveResponse(
            details=game.full_description,
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
