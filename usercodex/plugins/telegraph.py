# telegraph utils for codexuserbot
import os
import random
import string
from datetime import datetime

from PIL import Image
from telegraph import Telegraph, exceptions, upload_file
from telethon.utils import get_display_name

from usercodex import codex

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_or_reply
from . import BOTLOG, BOTLOG_CHATID, mention

LOGS = logging.getLogger(__name__)
plugin_category = "utils"


telegraph = Telegraph()
r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")


@codex.cod_cmd(
    pattern="(t(ele)?g(raph)?) ?(m|t|media|text)(?:\s|$)([\s\S]*)",
    command=("telegraph", plugin_category),
    info={
        "header": "To get telegraph link.",
        "description": "Reply to text message to paste that text on telegraph you can also pass input along with command \
            So that to customize title of that telegraph and reply to media file to get sharable link of that media(atmost 5mb is supported)",
        "options": {
            "m or media": "To get telegraph link of replied sticker/image/video/gif.",
            "t or text": "To get telegraph link of replied text you can use custom title.",
        },
        "usage": [
            "{tr}tgm",
            "{tr}tgt <title(optional)>",
            "{tr}telegraph media",
            "{tr}telegraph text <title(optional)>",
        ],
    },
)  # sourcery no-metrics
async def _(event):
    "To get telegraph link."
    codevent = await edit_or_reply(event, "`processing........`")
    if BOTLOG:
        await event.client.send_message(
