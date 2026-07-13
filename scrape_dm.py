# scrape_dm.py
import asyncio
import random
from telethon import TelegramClient
from telethon.sessions import MemorySession
from config import *

client = TelegramClient(MemorySession(), API_ID, API_HASH)

async def scrape_and_dm():
    await client.start()
    
    # 🔁 YAHAN TARGET CHANNEL DAAL (jahan se members churane hain)
    target = await client.get_entity('@JASMINE_TCLOTTERY')
    
    print("📋 Scraping members...")
    users = []
    async for user in client.iter_participants(target, limit=200):
        if user.username:
            users.append(f"@{user.username}")
    
    print(f"✅ {len(users)} members found. Sending DMs...")
    
    msg = f"🔥 Join {YOUR_CHANNEL} for daily 5K+ profit!\nRegister: {REFERRAL_LINK}"
    
    for i, username in enumerate(users[:100]):
        try:
            entity = await client.get_entity(username)
            await client.send_message(entity, msg)
            print(f"✅ [{i+1}/100] DM sent to {username}")
            await asyncio.sleep(random.randint(8, 15))
        except Exception as e:
            print(f"❌ Failed: {username} - {str(e)[:30]}")

asyncio.run(scrape_and_dm())