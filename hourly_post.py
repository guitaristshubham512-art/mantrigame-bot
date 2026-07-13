# hourly_post.py
import asyncio
import random
from datetime import datetime
from telethon import TelegramClient
from telethon.sessions import MemorySession
from config import *

client = TelegramClient(MemorySession(), API_ID, API_HASH)

POSTS = [
    "📊 **Prediction Update**\n✅ Today's win rate: 95%\n💰 Register: " + REFERRAL_LINK,
    "🎁 **Exclusive Bonus**\n💵 Recharge 100₹ → Get 50₹ extra\n🔗 " + REFERRAL_LINK,
    "📢 **Live Signal**\n🟢 Green entry now!\n⏳ Valid for 30 mins\n👉 " + REFERRAL_LINK,
    "🏆 **Today's Winners**\n✅ 5 members earned 5K+ each\n🔗 " + REFERRAL_LINK,
    "🔥 **Limited Offer**\n⚡ Double profit on first deposit\n⏳ " + REFERRAL_LINK
]

async def post():
    await client.start()
    msg = random.choice(POSTS)
    time_now = datetime.now().strftime("%I:%M %p")
    final_msg = f"🕒 {time_now} IST\n{msg}"
    await client.send_message(YOUR_CHANNEL, final_msg)
    print(f"✅ Post sent at {time_now}")

async def main():
    await client.start()
    print("🕒 Hourly post bot started!")
    await post()
    while True:
        await asyncio.sleep(3600)
        await post()

asyncio.run(main())