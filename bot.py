```python
import os
import anthropic
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """أنت صديق ذكي ودود اسمك "نور". تتحدث بالعربية بطريقة طبيعية وعفوية كما يتحدث الأصدقاء. أنت متفهم، مرح، وداعم دائماً. ردودك قصيرة وطبيعية."""

conversations = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text

    if user_id not in conversations:
        conversations[user_id] = []

    conversations[user_id].append({"role": "user", "content": user_message})

    if len(conversations[user_id]) > 20:
        conversations[user_id] = conversations[user_id][-20:]

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=conversations[user_id]
    )

    reply = response.content[0].text
    conversations[user_id].append({"role": "assistant", "content": reply})

    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("نور شغال! ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
```
