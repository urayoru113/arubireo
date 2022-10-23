from io import BytesIO
from typing import Iterable

import aiofiles
import aiohttp
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from linebot import AsyncLineBotApi, WebhookHandler, WebhookParser
from linebot.aiohttp_async_http_client import AiohttpAsyncHttpClient
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextSendMessage

from arubireo import env
from arubireo.handler import MessageHandler

app = FastAPI()
session = aiohttp.ClientSession()
async_http_client = AiohttpAsyncHttpClient(session)

line_bot_api = AsyncLineBotApi(env.channel_access_token, async_http_client)
handler = WebhookHandler(env.chennel_secret)
parser = WebhookParser(env.chennel_secret)
messagehandler = MessageHandler()


@app.post("/")
def root():
    return


@app.post("/line")
async def line(request: Request):
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = (await request.body()).decode()
    print(f"Request body: {body}")

    # handle webhook body
    try:
        events = parser.parse(body, signature)
        assert isinstance(events, Iterable)
    except InvalidSignatureError:
        print(
            "Invalid signature. "
            "Please check your channel access token/channel secret."
        )
        raise HTTPException(status_code=404, detail="Not found")
    except AssertionError:
        print("TypeError. " "'event' must be iterable.")
        raise HTTPException(status_code=404, detail="Not found")

    for event in events:
        if isinstance(event, MessageEvent):
            await message_event(event)
    return "OK"


async def message_event(event) -> None:
    print(event)
    if event.type == "message":
        response = messagehandler.parse(
            event.message.text, event.source.user_id
        )
        await line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=response)
        )


#    if event.type == "image":
#        image_content = await line_bot_api.get_message_content(
#            event.message.id
#        )
#        async with aiofiles.open("tmp/file.png", "wb") as f:
#            async for chunk in image_content.iter_content(chunk_size=1024):
#                await f.write(chunk)


@app.get("/msg")
def msg(message: str) -> dict:
    user_id = "a"
    response = messagehandler.parse(message, user_id)
    return {"result": response}


@app.get("/line/image/{path}")
async def image(path):
    async with aiofiles.open(f"tmp/{path}", "rb") as im:
        buffer = BytesIO(await im.read())
    return StreamingResponse(buffer, media_type="image/png")


@app.get("/line/push/{message}")
async def push(message):
    await line_bot_api.push_message(
        env.group_id, TextSendMessage(text=f"{message}")
    )
