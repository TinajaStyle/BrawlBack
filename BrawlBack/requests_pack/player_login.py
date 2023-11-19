from fastapi import HTTPException, status
from aiohttp import ClientSession
from security.config import url, header

async def get_player(tag: str) -> dict:
    tag2 = f"%23{tag}".lower()
    async with ClientSession() as session:
        async with session.get(url=f"{url}players/{tag2}", headers=header) as response:
            status_code = response.status
            match status_code:
                case 200:
                    content = await response.json()
                case 404:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="player not found",
                    )
                case 403:
                    raise HTTPException(
                        status_code=status.HTTP_202_ACCEPTED,
                        detail="unauthorized server",
                    )
                case 503:
                    raise HTTPException(
                        status_code=status.HTTP_202_ACCEPTED,
                        detail="Brawl Stars server under maintenance",
                    )
                case _:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"The following exception has been thrown: {status_code} please contact with support")
    data = {"name":str(content["name"]), "trophies":str(content["trophies"])}
    return data