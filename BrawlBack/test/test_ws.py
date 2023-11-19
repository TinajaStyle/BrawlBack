from decouple import config
import websockets
import json
import pytest
#import ssl  #if you use a self-signed certificate uncomment and comment respectively

url = "ws://127.0.0.1:8000/player/ws/"
token = config("TEST_TOKEN")
tag = ""

@pytest.mark.asyncio
async def test_socks():
    #ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    #ssl_context.verify_mode = ssl.CERT_NONE

    full_url = f"{url}?tag={tag}"
    #async with websockets.connect(full_url, extra_headers={"bearer":token}, ssl=ssl_context) as ws:
    async with websockets.connect(full_url, extra_headers={"bearer":token}) as ws:
        resp = await ws.recv()
        data = json.loads(resp)
        assert data == {'msg': 'ping'}