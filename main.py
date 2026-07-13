# main.py – Combined all bots for Render (with Session String)
import asyncio
import random
from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession  # ✅ CHANGE 1: StringSession import
from config import *

# ----- CONFIG -----
SOURCE_CHANNEL = '@MELINDA_MANTRIMALL'  # 🔁 CHANGE IF NEEDED

# ✅ CHANGE 2: StringSession use karo
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# ----- REPOST BOT -----
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
        print(f"✅ Reposted from {SOURCE_CHANNEL}")
    except Exception as e:
        print(f"❌ Repost error: {e}")

# ----- HOURLY POST -----
POSTS = [
    f"📊 **Prediction Update**\n✅ Today's win rate: 95%\n💰 Register: {REFERRAL_LINK}",
    f"🎁 **Exclusive Bonus**\n💵 Recharge 100₹ → Get 50₹ extra\n🔗 {REFERRAL_LINK}",
    f"📢 **Live Signal**\n🟢 Green entry now!\n⏳ Valid for 30 mins\n👉 {REFERRAL_LINK}",
    f"🏆 **Today's Winners**\n✅ 5 members earned 5K+ each\n🔗 {REFERRAL_LINK}",
    f"🔥 **Limited Offer**\n⚡ Double profit on first deposit\n⏳ {REFERRAL_LINK}"
]

async def hourly_post():
    while True:
        await asyncio.sleep(3600)  # 1 hour
        msg = random.choice(POSTS)
        time_now = datetime.now().strftime("%I:%M %p")
        final_msg = f"🕒 {time_now} IST\n{msg}"
        await client.send_message(YOUR_CHANNEL, final_msg)
        print(f"✅ Hourly post sent at {time_now}")

# ----- SCRAPE & DM (Optional - 1 baar chalega) -----
async def scrape_and_dm():
    try:
        target = await client.get_entity('@JASMINE_TCLOTTERY')  # 🔁 CHANGE
        print("📋 Scraping members...")
        users = []
        async for user in client.iter_participants(target, limit=50):
            if user.username:
                users.append(f"@{user.username}")
        
        print(f"✅ {len(users)} members found. Sending DMs...")
        msg = f"🔥 Join {YOUR_CHANNEL} for daily 5K+ profit!\nRegister: {REFERRAL_LINK}"
        
        for username in users[:20]:  # Sirf 20 DMs (safe)
            try:
                entity = await client.get_entity(username)
                await client.send_message(entity, msg)
                print(f"✅ DM sent to {username}")
                await asyncio.sleep(10)
            except Exception as e:
                print(f"❌ Failed: {username}")
    except Exception as e:
        print(f"⚠️ Scrape/DM skipped: {e}")

# ----- MAIN -----
async def main():
    await client.start()
    print("🔥 Mantri Bot started on Render!")
    
    # Optional: Ek baar scrape+DM karo (hatana hai toh comment kar do)
    asyncio.create_task(scrape_and_dm())
    
    # Hourly post background mein
    asyncio.create_task(hourly_post())
    
    # Repost bot (main loop)
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())