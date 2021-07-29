# Port by kenzo
import asyncio
from datetime import datetime

from telethon.tl.types import ChannelParticipantAdmin as admin
from telethon.tl.types import ChannelParticipantCreator as owner
from telethon.utils import get_display_name

from usercodex import codex

plugin_category = "admin"


class TAGS:
    def __init__(self):
        self.tags_time = None
        self.tags_start = {}
        self.tags_end = {}


TAGS_ = TAGS()


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


@codex.cod_cmd(
    pattern="alltags(?:\s|$)([\s\S]*)",
    command=("alltags", plugin_category),
    info={
        "header": "Tag all members in the group.",
        "description": "This feature is to tag members in the group, including owner and admin.",
        "usage": [
            "{tr}alltags in group.",
        ],
        "examples": "{tr}alltags and see.",
    },
    groups_only=True,
)
async def alltags(event):
    TAGS_.tags_time = None
    TAGS_.tags_end = {}
    start_1 = datetime.now()
    TAGS_.tags_on = True
    TAGS_.tags_start = start_1.replace(microsecond=0)
    text = (event.pattern_match.group(1)).strip()
    users = []
    limit = 0

    if event.fwd_from:
        return

    async for x in event.client.iter_participants(event.chat_id):
        if not (x.bot or x.deleted):
            if not (
                isinstance(x.participant, admin) or isinstance(x.participant, owner)
            ):
                users.append(f"[{get_display_name(x)}](tg://user?id={x.id})")
            if isinstance(x.participant, admin):
                users.append(f"👮 Admin: [{get_display_name(x)}](tg://user?id={x.id})")
            if isinstance(x.participant, owner):
                users.append(f"🤴 Owner: [{get_display_name(x)}](tg://user?id={x.id})")

    mentions = list(user_list(users, 6))
    for mention in mentions:
        try:
            mention = "  |  ".join(map(str, mention))
            if text:
                mention = f"{text}\n{mention}"
            if event.reply_to_msg_id:
                await event.client.send_message(
                    event.chat_id, mention, reply_to=event.reply_to_msg_id
                )
            else:
                await event.client.send_message(event.chat_id, mention)

            limit += 6
            await asyncio.sleep(2)
        except BaseException:
            pass

    await event.delete()


@codex.cod_cmd(
    pattern="endtags$",
    edited=False,
    groups_only=True,
)
async def endtags(event):
    if TAGS_.tags_on is False:
        return
    TAGS_.tags_start = datetime.now()
    TAGS_.tags_end = TAGS_.tags_start.replace(microsecond=0)
    msg = await event.edit("Plugin Tags has stopped.")
    await asyncio.sleep(3)
    await msg.delete()
