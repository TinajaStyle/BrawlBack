from fastapi import (APIRouter, Path, Depends, status, 
                     WebSocket, Query, HTTPException, WebSocketException)
from typing import Annotated
from requests_pack import player_login as pl
from db.connections import Connections
from schemas.player import Player, Battle_list
from security.dependence import Security
from pydantic import ValidationError
import logging

router = APIRouter(
    prefix="/player", tags=["player"], 
)

responss = {
    401:{"description":"expired or invalid jwt"},
    404:{"description":"player not found"}
}

@router.get("/{tag}", response_model = Player,
            dependencies=[Depends(Security.verify_token)],
            status_code=status.HTTP_200_OK,
            responses={**responss, 202:{
                "     description":"Brawl Stars server under maintenance or unauthorized server"},
                      409:{"description":"The following exception has been thrown: {status_code} please contact with support"}})
async def profile(tag: Annotated[str, Path(max_length=12)]):
    """
    Call the function that requests the information
    of the player from API of brawl stars. Requires a tag.

    --> return a Player(name,trophies) object
    """
    return await pl.get_player(tag)

@router.get("/battlelog/{tag}", response_model = Battle_list, 
            status_code=status.HTTP_200_OK,
            responses={**responss, 424:{"description":"cant connect with database"},
                       400:{"description":"incorrect information"},})
async def battle(username: Annotated[str, Depends(Security.verify_token)],
                 tag: Annotated[str, Path(max_length=12)]):
    """
    Call the function that requests the battle log from the database. 
    Requires a tag.

    --> returns a list of Battle(star,time,trophies,mode) objects.

    """
    try:
        tag = tag.lower()
        returned = Battle_list(battles = await Connections.get_history(username, tag))
    except ValidationError as e:
        logging.error(e.error())
    return returned

@router.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket, tag: Annotated[str, Query()]):
    await websocket.accept() 
    token = websocket.headers["bearer"]
    username = await Security.verify_token_ws(token=token)
    try:    
        tag = tag.lower()
        while True:
            send = await Connections.battlesock(websocket, username, tag)
            await websocket.send_json(send)
    except HTTPException as e:
        if e.status_code == 424:
            raise WebSocketException(code=status.WS_1013_TRY_AGAIN_LATER, 
                                 reason="user or tag error")
        else:
            raise WebSocketException(code=status.WS_1003_UNSUPPORTED_DATA, 
                                 reason="user or tag error")
    except:
        await websocket.close()