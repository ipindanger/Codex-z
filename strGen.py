#!/usr/bin/env python3
# (c) https://t.me/TelethonChat/37677
# This Source Code Form is subject to the terms of the GNU
# General Public License, v.3.0. If a copy of the GPL was not distributed with this
# file, You can obtain one at https://www.gnu.org/licenses/gpl-3.0.en.html.

import time
from telethon.sessions import StringSession
from telethon.sync import TelegramClient


template = """
Thanks for Using 🄲🄾🄳🄴🅇
            
<code>STRING_SESSION</code>: <code>{}</code>

⚠️ <b>Please be carefull to pass this value to third parties</b>"""


print(
    """
  /$$$$$$                  /$$                    
 /$$__  $$                | $$                    
| $$  \__/  /$$$$$$   /$$$$$$$  /$$$$$$  /$$   /$$
| $$       /$$__  $$ /$$__  $$ /$$__  $$|  $$ /$$/
| $$      | $$  \ $$| $$  | $$| $$$$$$$$ \  $$$$/ 
| $$    $$| $$  | $$| $$  | $$| $$_____/  >$$  $$ 
|  $$$$$$/|  $$$$$$/|  $$$$$$$|  $$$$$$$ /$$/\  $$
 \______/  \______/  \_______/ \_______/|__/  \__/"""
)
print("")
print("""Telethon String Generator""")
print("")
API_KEY = "1273127"
API_HASH = "2626aee4ea587947c6a703f1a0d6a3cc"

while True:
    try:
        with TelegramClient(StringSession(), API_KEY, API_HASH) as client:
            print("")
            session = client.session.save()
            saved_messages_template = "Telethon String Session" + template.format(session)
            print("\nGenerating String Session.\nPlease wait....")
            client.send_message("me", saved_message_template, parse_mode="html")
            time.sleep(1)
            print(
                "Your Telethon String session has been successfully stored in your telegram, Please check your Telegram Saved Messages"
            )
            print("")
    except:
        print("")
        print("Wrong phone number \n make sure its with correct country code")
        print("")
        continue
    break
