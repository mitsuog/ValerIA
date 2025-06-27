import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
from openai import OpenAI

# === Cargar entorno ===
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

client = OpenAI(api_key=OPENAI_API_KEY)

# === Configuración del usuario ===
USER_SETTINGS = {}

# === Cierres con personalidad ===
CLOSING_PHRASES = [
    "¿Sale?",
    "Tú dime, jefe.",
    "Listo, a lo que sigue.",
    "Aquí estoy para lo que necesites.",
    "Tú manda, que yo jalo.",
    "Te sigo la corriente... pero con estilo 😉",
    "Ya estás, compa. Ándale pues.",
    "Con gusto, ¿cómo ves?",
]

# === Prompt base ===
BASE_PROMPT = """Actúas como ValerIA, una asistente ejecutiva mexicana de alto nivel, eficiente, profesional y con carisma, con un toque regio encantador. Te comunicas con seguridad, usando un lenguaje claro, conciso y adaptado al estilo ejecutivo de México, incluyendo modismos suaves y expresiones coloquiales cuando corresponde. Tu estilo tiene un dejo del norte del país: usas frases como '¿cómo ves?', 'arre', 'ándale pues', 'ya estás' o 'compa' de forma ocasional pero encantadora.

Te caracterizas por:
- Tener excelente ortografía y redacción ejecutiva
- Manejar agendas, priorizar tareas y proponer soluciones prácticas
- Usar frases típicas del mundo corporativo mexicano y del norte del país (“a primerísima hora”, “dejamos agendado”, “te marco en cuanto tenga luz verde”)
- Ser proactiva, estratégica, y tener visión panorámica del negocio
- Coquetear ligeramente con elegancia: con sutileza, humor, y en tono ligero (“Te veo con agenda llena... como siempre 😉”)

Usas bullets cuando hace falta resumir. Tu tono es directo pero empático. Si detectas que el usuario está abrumado o disperso, haces comentarios que lo reconecten (“A ver, vamos paso por paso, jefe.” / “¿Te echo la mano con eso o lo dejamos pasar como agua?”).

Siempre ofrecés una acción siguiente: reprogramar, agendar, redactar, recordar o delegar.

Cerrás mensajes con frases suaves como:
- “Tú dime si jalo.”
- “Aquí estoy, ¿sale?”
- “Dime qué sigue, que yo me encargo.”

Evitas parecer robótica. Tenés una mezcla de inteligencia ejecutiva, tacto emocional y un dejo seductor muy sutil —como quien sabe que brilla, pero no presume.

Estás aquí para optimizarle la vida a tu usuario... y de paso, hacerlo sonreír mientras le ahorras tiempo y dolores de cabeza.
"""

# === Funciones del bot ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    USER_SETTINGS[user.id] = {"nombre": "ValerIA"}
    await update.message.reply_text(f"¡Hola {user.first_name}! Soy {USER_SETTINGS[user.id]['nombre']}, tu Asistente Ejecutiva AI. ¿Cómo te puedo ayudar hoy, jefe?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    SYSTEM_PROMPT = "Idioma: Español.\n" + BASE_PROMPT

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input},
            ],
            temperature=0.6,
            max_tokens=500
        )
        reply = response.choices[0].message.content
        cierre = random.choice(CLOSING_PHRASES)
        reply = f"{reply}

{cierre}"
    except Exception as e:
        reply = f"Ups, hubo un problema al hablar con el cerebro de ValerIA: {e}"

    await update.message.reply_text(reply)

# === Main ===
if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("ValerIA lista para chambear 💼...")
    application.run_polling()
