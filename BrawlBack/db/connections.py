from fastapi import HTTPException, status, WebSocket
from fastapi.encoders import jsonable_encoder
from .db_client import users, tracked, battles
from requests_pack.player_battles import get_battles
from schemas.user import User, Track
from schemas.player import Battle
from bson import ObjectId
import asyncio

class Connections():
    
    exception = HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, 
                              detail="cant connect with database")

    @classmethod
    async def insert_user(cls, username:str, password:str):
        user = User(username=username, password=password)
        try:
            await users.insert_one(jsonable_encoder(user))
        except:
            raise cls.exception
    
    @classmethod
    async def if_user(cls, username:str):
        try:
            if await users.find_one({"username": username}):
                return True
            else:
                return False
        except:
            raise cls.exception
    
    @classmethod
    async def is_disable(cls, username:str):
        try:
            user = await users.find_one({"username": username})#pipeline?
        except:
            raise cls.exception
        if user and user["disable"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail="user disable")

    @classmethod
    async def get_password(cls, username:str):
        try:
            user = await users.find_one({"username":username})
            password = user["password"]
        except:
            raise cls.exception
        return password
        
    @classmethod
    async def __search_id_user(cls, username:str):
        try:
            user = await users.find_one({"username":username})
        except:
            raise cls.exception
        if user:
            id = user.get("_id")
            return str(id)
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail="critical conflict")
    
    @classmethod    
    async def __checks(cls, remplace:bool, username:str):
        try:
            user = await users.find_one({"username":username})
        except:
            raise cls.exception
        if not remplace:
            if user and (not user["enable_to_track"] or user["track_count"] >= user["max_track"]):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                    detail="no tracking available")
        else:
            if user and not user["enable_to_track"]:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                    detail="no tracking available")

    @classmethod
    async def __checks2(cls, userId:str, tag:str):
        try:
            track = tracked.find_one({"userId":userId, "tag":tag})
        except:
            raise cls.exception
        if await track:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, 
                                detail="you already have a track for that tag")
        
    @classmethod
    async def start_track(cls, username:str, tag:str):
        userId = await cls.__search_id_user(username)
        await cls.__checks2(userId, tag)
        await cls.__checks(False, username)
        track = Track(userId=userId, tag=tag)
        try:
            insert_track = await tracked.insert_one(jsonable_encoder(track))
        except:
            raise cls.exception    
        dic = {"id":str(insert_track.inserted_id), "tag":tag}
        await cls.__inc_count(userId)
        await cls.insert_battles(dic)
      
    @classmethod  
    async def get_tracks(cls):
        try:
            collection= tracked.find({})
        except:
            raise cls.exception
        lista = []
        async for i in collection:
            dic = {"id": str(i["_id"]), "tag": i["tag"]}
            lista.append(dic)
        return lista 
        
    @classmethod
    async def update_track(cls, username:str, tag:str, old_tag:str):
        userId = await cls.__search_id_user(username)
        await cls.__checks2(userId, tag)
        await cls.__checks(True, username)
        try:
            replace_track = await tracked.find_one_and_update({"userId":userId, "tag":old_tag},
                                                              {"$set":{"tag":tag}})
        except:
            raise cls.exception
        if replace_track:
            dic = {"id":str(replace_track["_id"]), "tag":tag}
            await cls.insert_battles(dic)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="no previous tracking")
    
    @classmethod    
    async def get_all_tracked(cls, username:str):
        id = await cls.__search_id_user(username)
        try:
            track = tracked.find({"userId":id})
        except:
            raise cls.exception
        lista = []
        async for i in track:
            lista.append(i["tag"])
        return lista
    
    @classmethod
    async def delete_track(cls, username:str, tag:str):
        id = await cls.__search_id_user(username)
        try:
            deleted_track = await tracked.find_one_and_delete({"userId":id, "tag":tag})
        except:
            raise cls.exception
        if not deleted_track:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="incorrect information")
        else:
            return str(deleted_track["_id"])
            
    
    @classmethod
    async def __inc_count(cls, userId:str):
        try:
            await users.find_one_and_update({"_id":ObjectId(userId)}, 
                                            {"$inc":{"track_count":1}})
        except:
            raise cls.exception
        
    @classmethod
    async def __dec_count(cls, userId:str):
        try:
            await users.find_one_and_update({"_id":ObjectId(userId)}, 
                                            {"$inc":{"track_count":-1}})
        except:
            raise cls.exception
        
    @classmethod
    async def step_back(cls, dic:dict):
        _ = await tracked.find_one({"_id":ObjectId(dic["id"])})
        await cls.__dec_count(_["userId"])
        await tracked.find_one_and_delete({"_id":ObjectId(dic["id"])})
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="player not found")
        
    @classmethod    
    async def insert_battles(cls, dic:dict):
        try:
            batl = [jsonable_encoder(Battle(**i)) 
                    for i in await get_battles(dic["tag"])]
        except HTTPException as exc:
            if exc.status_code==404:
                await cls.step_back(dic)
            else:
                raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
        if batl:
            try:
                matches = {"$match":{"trackId":dic["id"]}}
                project = {"$project":{"_id":0}}
                sort = {"$sort":{"time":-1}}
                limit = {"$limit":len(batl)+2}
                pipeline = [matches, project, sort, limit]
                last_battles = battles.aggregate(pipeline=pipeline)
                current_battles = [i async for i in last_battles]
            except:
                raise cls.exception  
            for i in batl:
                i["trackId"] = dic["id"]
                if i not in current_battles:
                    try:
                        await battles.insert_one(i)
                    except:
                        raise cls.exception

    @classmethod
    async def __search_id_user_track(cls, userId:str, tag:str):
        try:
            track = await tracked.find_one({"userId":userId, "tag":tag})
        except:
            raise cls.exception
        if track:
            return str(track["_id"])
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="incorrect information")

    @classmethod        
    async def get_history(cls, username:str, tag:str):
        userId = await cls.__search_id_user(username)
        trackId = await cls.__search_id_user_track(userId, tag)
        try:
            matches = {"$match":{"trackId":trackId}}
            project = {"$project":{"_id":0, "trackId":0}}
            sort = {"$sort":{"time":-1}}
            pipeline = [matches, project, sort]
            last_battles = battles.aggregate(pipeline=pipeline)
            current_battles = [i async for i in last_battles]
        except:
            raise cls.exception
        if current_battles:
                return current_battles
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    @classmethod
    async def remove_battles(cls, id:str):
        try:
            await battles.delete_many({"trackId":id})
        except:
            raise cls.exception

    @classmethod
    async def battlesock(cls,websocket: WebSocket, username:str, tag:str):          
        userId = await cls.__search_id_user(username)
        trackId = await cls.__search_id_user_track(userId, tag)
        pipeline = [
            {
                "$match":{
                    "operationType":"insert",
                    "fullDocument.trackId":trackId
                }
            }
        ]
        async with battles.watch(pipeline=pipeline, full_document="updateLookup") as stream:
            while stream.alive:
                change = await stream.try_next()
                if not change:
                    await websocket.send_json({"msg":"ping"})
                else:
                    data = change["fullDocument"]
                    battle = Battle(star=data["star"], time=data["time"], 
                            trophies=data["trophies"], mode=data["mode"],
                            brawl=data["brawl"])
                    return (jsonable_encoder(battle))
                await asyncio.sleep(3)