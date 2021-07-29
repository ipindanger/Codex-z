# Port by kenzo
import asyncio
from asyncio import sleep

from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChannelParticipantAdmin as admin
from telethon.tl.types import ChannelParticipantCreator as owner
from telethon.tl.types import ChannelParticipantsKicked, ChatBannedRights
from telethon.utils import get_display_name

from usercodex import codex

from ..core.logger import logging
from ..utils import is_admin

plugin_category = "admin"

LOGS = logging.getLogger(__name__)


@codex.cod_cmd(
    pattern="allkick(?:\s|$)([\s\S]*)",
    command=("allkick", plugin_category),
    info={
        "header": "Kick all the members in the group.",
        "description": "This feature is only for Owners and Co-Founders.",
        "usage": [
            "{tr}allkick in ur group.",
        ],
        "examples": "{tr}allkick and see.",
    },
    groups_only=True,
    require_admin=True,
)
async def allkick(event):
    await event.get_chat()
    lynxget = await event.client.get_me()
    user = await event.get_user()
    codadmin = await is_admin(event.client, event.chat_id, event.client.uid)
    if not codadmin:
        await event.edit(
            "`#Disclaimer ❌\nThis plugin is specifically for Owners and Co-Founders.`"
        )
        return
    await event.edit("`in Process...`")

    everyone = await event.client.get_participants(event.chat_id)
    for user in everyone:
        if user.id == lynxget.id:
            pass
        try:
            await event.client(
                EditBannedRequest(
                    event.chat_id,
                    int(user.id),
                    ChatBannedRights(until_date=None, view_messages=True),
                )
            )
        except Exception as e:
            await event.edit(str(e))
        await sleep(0.5)
    await event.edit(f"#Successfully ☑️\nYou have kicked All Members here.")


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


@codex.cod_cmd(
    pattern="alltags(?:\s|$)([\s\S]*)",
    command=("alltags", plugin_category),
    info={
        "header": "Tags all the members in the group.",
        "description": "This feature is only for Admin Group",
        "usage": [
            "{tr}alltags in group.",
        ],
        "examples": "{tr}alltags and see.",
    },
    groups_only=True,
    require_admin=True,
)
async def alltags(event):
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
                users.append(f"👮 [{get_display_name(x)}](tg://user?id={x.id})")
            if isinstance(x.participant, owner):
                users.append(f"🤴 [{get_display_name(x)}](tg://user?id={x.id})")

    mentions = list(user_list(users, 6))
    for mention in mentions:
        try:
            mention = " | ".join(map(str, mention))
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
    pattern="allunban(?:\s|$)([\s\S]*)",
    command=("allunban", plugin_category),
    info={
        "header": "Delete the list of tires in the group.",
        "description": "This feature is only for Admin Group",
        "usage": [
            "{tr}allunban in your groups.",
        ],
        "examples": "{tr}allunban and see.",
    },
    groups_only=True,
)
async def _(event):
    await event.edit("Looking for a List Banning...")
    p = 0
    (await event.get_chat()).title
    async for i in event.client.iter_participants(
        event.chat_id,
        filter=ChannelParticipantsKicked,
        aggressive=True,
    ):
        try:
            await event.client.edit_permissions(event.chat_id, i, view_messages=True)
            p += 1
        except BaseException:
            pass
    await event.edit("Success, The list of all tires in this group has been removed.")
