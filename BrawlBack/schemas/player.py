from pydantic import BaseModel

class Player(BaseModel):
    name : str
    trophies : str
    
class Battle(BaseModel):
    star : bool | None = False
    time : str
    trophies : str 
    mode : str
    brawl : str | None = None
    
class Battle_list(BaseModel):
    battles : list[Battle]