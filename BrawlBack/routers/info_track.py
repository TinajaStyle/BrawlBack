from fastapi import (APIRouter, Path, Body, Depends,
                    HTTPException, status, Response)
from db.connections import Connections
from db.db_client import r
from security.dependence import Security
from typing import Annotated

router = APIRouter(
    prefix="/track",
    tags=["track"],
    dependencies=[Depends(Security.verify_token)]
)

responss = {
    424: {"description":"cant connect with database"},
    401:{"description":"expired or invalid jwt"}
}

@router.post("/start_track/{tag}",
             status_code=status.HTTP_201_CREATED,
             responses={**responss, 403:{"description":"no tracking available"},
                        406:{"description":"there is already a track for that tag"},
                        404:{"description":"player not found"}})
async def start(username: Annotated[str, Depends(Security.verify_token)],
                tag: Annotated[str, Path()], response: Response):
    tag = tag.lower()
    await Connections.start_track(username, tag)
    response.status_code = status.HTTP_201_CREATED
 
@router.put("/update_track", 
            status_code=status.HTTP_200_OK,
            responses={**responss, 400:{"description":"no previous tracking"},
                       403:{"description":"no tracking available"},
                       404:{"description":"player not found"}})
async def update(username: Annotated[str, Depends(Security.verify_token)],
                 tag: Annotated[str, Body()],                
                 old_tag: Annotated[str, Body()]):
    tag = tag.lower()
    old_tag = old_tag.lower()
    await Connections.update_track(username, tag, old_tag)
    return f"nuevo seguimiento para {username}"

@router.get("/get_all_tracked",
            status_code=status.HTTP_200_OK,
            responses=responss)
async def all_tracked(username: Annotated[str, Depends(Security.verify_token)]):
    lista = await Connections.get_all_tracked(username)
    return {"tags":lista}

@router.delete("/delete_track/{tag}", 
               status_code=status.HTTP_204_NO_CONTENT,
               responses={**responss, 400:{"description":"incorrect information"}})
async def delete(username: Annotated[str, Depends(Security.verify_token)],
                 tag: Annotated[str, Path()]):
    tag = tag.lower()
    deleted_track_id = await Connections.delete_track(username, tag)
    await stack_to_remove(deleted_track_id)
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

async def stack_to_remove(id:str):
    try:
        r.lpush("list_deleted_track", id)
    except:
        pass