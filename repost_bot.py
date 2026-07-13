# repost_bot.py
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import MemorySession
from config import *

SOURCE_CHANNEL = '@MELINDA_MANTRIMALL'  # 🔁 YAHAN APNA SOURCE DAAL

client = TelegramClient(MemorySession(), API_ID, API_HASH)

async def main():
    await client.start()
    print(f"🔥 Repost bot active! Monitoring {SOURCE_CHANNEL}...")
    
    @client.on(events.NewMessage(chats=SOURCE_CHANNEL))
    async def repost(event):
        try:
            if event.message.media:
                await client.send_file(
                    YOUR_CHANNEL,
                    event.message.media,
                    caption=f"{event.message.text or ''}\n\n🔥 Join: {YOUR_CHANNEL}"
                )
            else:
                await client.send_message(
                    YOUR_CHANNEL,
                    f"{event.message.text}\n\n✅ Register: {REFERRAL_LINK}"
                )
            print(f"✅ Reposted")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    await client.run_until_disconnected()

asyncio.run(main())