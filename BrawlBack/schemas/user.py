from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    disable: bool | None = False
    enable_to_track: bool | None = False
    track_count: int | None = 0
    max_track: int | None = 0
    
class Track(BaseModel):
    userId: str
    tag: str