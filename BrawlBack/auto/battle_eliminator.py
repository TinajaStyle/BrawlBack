from auto.functions import repeater2
import asyncio
    
if __name__== "__main__":
    loop = asyncio.get_event_loop() 
    task = loop.create_task(repeater2())
    try:
        loop.run_until_complete(task)
    except:
        task.cancel()
    finally:
        loop.close()