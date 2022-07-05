import pydantic
from pydantic import Field


class Score(pydantic.BaseModel):
    player1: int
    player2: int

    def as_tuple(self):
        return self.player1, self.player2


class Player(pydantic.BaseModel):
    id: int
    full_name_international: str


class Match(pydantic.BaseModel):
    score: Score
    status: str
    player1: Player
    player2: Player


class Set(pydantic.BaseModel):
    score: Score
    status: str
    number: int
    active_player_id: int
    reverse_position: int
    active_player_id: int


class Data(pydantic.BaseModel):
    match: Match
    set: Set


class Event(pydantic.BaseModel):
    data: Data
    status: int = Field(200, const=True)
    uid: str = Field("incident-feed", const=True)
