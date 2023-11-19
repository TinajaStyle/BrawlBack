from fastapi import HTTPException, status
from aiohttp import ClientSession
from security.config import url, header


async def get_battles(tag: str) -> dict:
    tag2 = f"%23{tag}".lower()
    async with ClientSession() as session:
        async with session.get(
            url=f"{url}players/{tag2}/battlelog", headers=header) as response:
            status_code = response.status
            match status_code:
                case 200:
                    json = await response.json()
                    lista = list(json["items"])
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
    lista_dicc = []
    for battle in lista:
        dicc = {}
        try:
            trophies = battle["battle"]["trophyChange"]
        except:
            continue
        try:
            tag3 = battle["battle"]["starPlayer"]["tag"]
            tag3 = tag[1:].lower()
            if tag3 == tag:
                dicc["star"] = True
        except:
            pass
        dicc["time"] = battle["battleTime"]
        dicc["trophies"] = str(trophies)
        dicc["mode"] = battle["battle"]["mode"]
        if dicc["mode"] == "soloShowdown":
            brawl = [i["brawler"]["name"] for i in battle["battle"]["players"] 
                        if i["tag"][1:].lower() == tag.lower()]
            if brawl:
                dicc["brawl"] = str(brawl[0])
        else:
            for j in range(len(battle["battle"]["teams"])):
                brawl =  [i["brawler"]["name"] for i in battle["battle"]["teams"][j] 
                        if i["tag"][1:].lower() == tag.lower()]
                if brawl:
                    dicc["brawl"] = str(brawl[0])
                    break
        lista_dicc.append(dicc)
    return lista_dicc