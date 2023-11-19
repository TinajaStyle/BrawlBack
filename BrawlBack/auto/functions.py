from db.connections import Connections
from db.db_client import r

async def repeater():
    try:
        lista = await Connections.get_tracks()
        for i in lista:
            try:
                await Connections.insert_battles(i)
            except:
                pass
    except:
        pass

async def repeater2():
    try:
        lista = r.lrange("list_deleted_track", 0, -1)
        for i in lista:
            trackId = i.decode('utf-8')
            try:
                await Connections.remove_battles(trackId)
                r.lrem("list_deleted_track", 0, i)
            except:
                continue
    except:
        pass