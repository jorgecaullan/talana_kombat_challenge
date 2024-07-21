""" Models o inputs required by API """
from typing import List
from pydantic import BaseModel

class Player(BaseModel):
    """ Data required for every player """
    movimientos: List[str]
    golpes: List[str]

class MoveRequest(BaseModel):
    """ Players required for a fight """
    player1: Player
    player2: Player

class MoveResponse(BaseModel):
    """ Standard response from start of a kombat """
    detail: str
    winner: str
