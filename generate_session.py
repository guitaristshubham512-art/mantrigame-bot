# generate_session_fixed.py
import asyncio
from telethon import TelegramClient, sessions

api_id = 2229165
api_hash = 'f83025572d642ace9b5705142b109fd0'

async def main():
    # 🔑 StringSession use karo (MemorySession nahi)
    client = TelegramClient(sessions.StringSession(), api_id, api_hash)
    
    await client.start()
    print("\n✅ Login successful!\n")
    
    # 🔑 Session string nikaalo
    session_string = client.session.save()
    
    if session_string:
        print("🔑 YOUR SESSION STRING:")
        print("="*60)
        print(session_string)
        print("="*60)
    else:
        print("❌ Session string empty! Trying alternative method...")
        # Alternative: .session file se read karo
        with open('my_session.session', 'r') as f:
            session_string = f.read()
            print("🔑 SESSION FROM FILE:")
            print(session_string)
    
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())