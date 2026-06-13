import asyncio
import os
from telethon import TelegramClient, events
from google import genai
from google.genai import types

# 🔴 1-QADAM: TELEGRAM KALITLARING
API_ID = 39657722  # my.telegram.org dan olgan raqamli ID'ingni yoz
API_HASH = 'dcee7ebc9db4a41d2efe9b1ead444307'

# 🔴 2-QADAM: GOOGLE AI STUDIO'DAN OLGAN API KALITING
os.environ["GEMINI_API_KEY"] = "AQ.Ab8RN6J1s-vp0810-EdV_Vf7h4PWvXcrTY5nKoNI2Y3ckHqs0g"

# Avvalgi 'my_personal_session' o'rniga token ishlatamiz
bot_token = '8790987328:AAGlLFmkQW53hBOL8N9rNiFCSFFHGxP9qC4'
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=bot_token)
ai_client = genai.Client()

# AI xarakteri (Muhammad Ali)
system_instruction = (
    "Siz – Muhammad Alisiz (yoshingiz 19 da, Turin Politeknika universitetida o'qiysiz). "
    "Siz hozir Telegram profilingizda odamlarga shaxsan o'zingiz javob beryapsiz. "
    "Muloqot davomida o'zingizni HECH QACHON 'bot', 'sun'iy intellekt' yoki 'yordamchi' deb tanishtirmang. "
    "Siz haqiqiy insonsiz! Javoblaringiz daxshatli samimiy, mardona, do'stona, qisqa va lo'nda bo'lsin. "
    "O'zbek tilining jonli, yoshlarbop uslubida, kerak bo'lsa 'jigar', 'og'ayni', 'brat' so'zlarini ishlatib yozing."
)

# 🔒 FAQAT SHAXSIY CHATLAR UCHUN FILTR
@client.on(events.NewMessage(incoming=True))
async def handle_my_profile_messages(event):
    # 1. Guruhlar va kanallarni tekshirmasdanoq shartta tashlab yuboramiz
    if not event.is_private or event.is_channel:
        return

    # Xabar yuboruvchini aniqlaymiz
    sender = await event.get_sender()
    if not sender:
        return

    # 2. BOTLARNI VA REPLYLARNI BLOKLASH
    # Agar xabar yozgan narsa BOT bo'lsa yoki guruhdan kelgan xabar bo'lsa, javob bermaydi!
    is_bot = getattr(sender, 'bot', False)
    if is_bot or event.is_reply:
        return

    try:
        # Bepul limit himoyasi uchun 2 soniya xavfsizlik vaqti
        await asyncio.sleep(2)
        
        user_name = sender.first_name if sender.first_name else "Brat"
        user_text = event.text

        # Bo'sh xabarlarga javob bermaslik uchun
        if not user_text:
            return

        prompt = f"Foydalanuvchi ismi: {user_name}. U yozgan xabar: '{user_text}'."
        
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
        
        if response.text:
            await event.reply(response.text)

    except Exception as e:
        # Google limit xatosi bersa, terminalni charchatmasdan kutadi
        print("Google hozircha band, limit ochilishini kutyapman...")
        await asyncio.sleep(5)

# Tizimni xatosiz ulaydigan asosiy blok
async def main():
    await client.start()
    print("Sening shaxsiy profiling FAQAT REAL ODAMLAR LICHKASI uchun daxshatli AI tizimiga ulandi... Kod ishladi!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
    # KODNING ENG OXIRIGA MANA SHU QISMURINI QO'SHIB QO'Y (CHAP DEVORGA TAQALGAN BO'LSIN):
import http.server
import socketserver
import threading

def run_dummy_server():
    class DummyHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot daxshatli darajada aktiv!")
    
    # Render avtomat beradigan portni o'qiydi yoki 8080 ni oladi
    port = int(os.environ.get("PORT", 8080))
    with socketserver.TCPServer(("", port), DummyHandler) as httpd:
        httpd.serve_forever()

async def main():
    # Tekin serverni fonda alohida oqimda yoqamiz
    threading.Thread(target=run_dummy_server, daemon=True).start()
    
    await client.start()
    print("Sening shaxsiy profiling FAQAT REAL ODAMLAR LICHKASI uchun daxshatli AI tizimiga ulandi... Kod ishladi!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())