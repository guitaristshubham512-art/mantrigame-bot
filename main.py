# main.py – Combined bot + dummy HTTP server for Render
import asyncio
import random
from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from aiohttp import web
from config import *

# ----- CONFIG -----
SOURCE_CHANNEL = '@MELINDA_MANTRIMALL'  # 🔁 CHANGE IF NEEDED
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

# ----- SCRAPE & DM (Optional) -----
async def scrape_and_dm():
    try:
        target = await client.get_entity('@JASMINE_TCLOTTERY')
        print("📋 Scraping members...")
        users = []
        async for user in client.iter_participants(target, limit=50):
            if user.username:
                users.append(f"@{user.username}")
        print(f"✅ {len(users)} members found. Sending DMs...")
        msg = f"🔥 Join {YOUR_CHANNEL} for daily 5K+ profit!\nRegister: {REFERRAL_LINK}"
        for username in users[:20]:
            try:
                entity = await client.get_entity(username)
                await client.send_message(entity, msg)
                print(f"✅ DM sent to {username}")
                await asyncio.sleep(10)
            except Exception:
                print(f"❌ Failed: {username}")
    except Exception as e:
        print(f"⚠️ Scrape/DM skipped: {e}")

# ----- BOT MAIN -----
async def bot_main():
    await client.start()
    print("🔥 Mantri Bot started on Render!")
    asyncio.create_task(scrape_and_dm())
    asyncio.create_task(hourly_post())
    await client.run_until_disconnected()

# ----- DUMMY HTTP SERVER (for Render port scan) -----
async def handle_health(request):
    return web.Response(text="Bot is running!")

async def start_http_server():
    app = web.Application()
    app.router.add_get('/', handle_health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()
    print("✅ Health check server on port 10000")
    await asyncio.Event().wait()  # keep running

# ----- FINAL RUNNER -----
if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot_task = loop.create_task(bot_main())
    http_task = loop.create_task(start_http_server())
    loop.run_until_complete(asyncio.gather(bot_task, http_task))