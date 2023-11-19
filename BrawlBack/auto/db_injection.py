from apscheduler.schedulers.asyncio import AsyncIOScheduler
from auto.functions import repeater
import asyncio

scheduler = AsyncIOScheduler()

scheduler.add_job(repeater,'interval', minutes=1)

scheduler.start()

async def main():
    while True:
        await asyncio.sleep(1)
    
if __name__== "__main__":
    loop = asyncio.get_event_loop() 
    task = loop.create_task(main())
    try:
        loop.run_until_complete(task)
    except:
        pass