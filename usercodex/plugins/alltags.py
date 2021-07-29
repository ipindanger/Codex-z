# Port by kenzo
import asyncio
from datetime import datetime

from telethon.tl.types import ChannelParticipantAdmin as admin
from telethon.tl.types import ChannelParticipantCreator as owner
from telethon.utils import get_display_name

from usercodex import codex

from . import BOTLOG, BOTLOG_CHATID

plugin_category = "admin"


class TAGS:
    def __init__(self):
        self.USRTAGS_ON = {}
        self.tags_time = None
        self.tags_start = {}
        self.tags_end = {}
        self.tags_on = False


TAGS_ = TAGS()


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


@codex.cod_cmd(incoming=True, edited=False)
async def set_time(event):
    if TAGS_.tags_on is False:
        return
    tags_start = datetime.now()
    TAGS_.tags_end = tags_start.replace(microsecond=0)
    if TAGS_.tags_start != {}:
        total_tags_time = TAGS_.tags_end - TAGS_.tags_start
        time = int(total_tags_time.seconds)
        d = time // (24 * 3600)
        time %= 24 * 3600
        h = time // 3600
        time %= 3600
        m = time // 60
        time %= 60
        s = time
        endtime = ""
        if d > 0:
            endtime += f"{d}d {h}h {m}m {s}s"
        elif h > 0:
            endtime += f"{h}h {m}m {s}s"
        else:
            endtime += f"{m}m {s}s" if m > 0 else f"{s}s"
    current_message = event.message.message
    if (
        ("endtags" not in current_message) or (f"{tr}endtags" not in current_message)
    ) and ("on" in TAGS_.USRTAGS_ON):
        shite = await event.client.send_message(
            event.chat_id,
            "`Plugin Tag has Stopped for " + endtime + "`",
        )
        TAGS_.USRTAGS_ON = {}
        TAGS_.tags_time = None
        await asyncio.sleep(5)
        await shite.delete()
        TAGS_.tags_on = False
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#TAGS `Has Stopped.\n" + " for " + endtime + "`",
            )


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
    text = (event.pattern_match.group(1)).strip()
    TAGS_.tags_time = None
    TAGS_.tags_end = {}
    start_1 = datetime.now()
    TAGS_.tags_on = True
    TAGS_.tags_start = start_1.replace(microsecond=0)
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

            TAGS_.tags_time = datetime.now()
            TAGS_.tags_on = False
            limit += 6
            await asyncio.sleep(2)
        except BaseException:
            pass

    await event.delete()


@codex.cod_cmd(
    pattern="endtags$",
    outgoing=True,
    edited=False,
    groups_only=True,
)
async def alltags(event):
    TAGS_.tags_start = datetime.now()
    TAGS_.tags_end = TAGS_.tags_start.replace(microsecond=0)
    if TAGS_.tags_on is False:
        msg = await event.edit("Plugin Tags has stopped.")
        await asyncio.sleep(3)
        await msg.delete()
