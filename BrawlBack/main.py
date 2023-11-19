from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routers import info_player, info_app, info_track
from fastapi.middleware.cors import CORSMiddleware
from hypercorn.asyncio import serve
from hypercorn.config import Config
import asyncio
import signal
import logging
import os

if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(filename="logs/server.log", level=logging.ERROR)

app = FastAPI(
    title="BrawlStatsBack",
    description="Brawl API helps you do awesome stuff",
    summary="Brawl's favorite app. Nuff said.",
    version="1.0",
    contact={
        "name": "TinajaStyle",
        "email": "tinajastyle@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
    docs_url="/documentation",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    try:
        lista = list(exc.errors())
        lis = []
        for i in lista:
            dic = {"field":i["loc"], "type":i["type"], "input":i["input"]}
            lis.append(dic)
        return JSONResponse(status_code=422, content={"Validation Error":{
            "detail":lis
        }})
    except:
        return JSONResponse(status_code=422, content={"detail":"Validation Error"})

app.include_router(info_player.router)
app.include_router(info_app.router)
app.include_router(info_track.router)

config = Config()
config.bind = ["localhost:8000"]

shutdown_event = asyncio.Event()

def _signal_handler(*_:any) -> None:
        shutdown_event.set()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, _signal_handler)
    loop.add_signal_handler(signal.SIGINT, _signal_handler)
    loop.run_until_complete(
        serve(app, config, shutdown_trigger=shutdown_event.wait)
    )