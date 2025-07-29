import requests
from datetime import datetime
import os
import logging

sound_start_hour = int(os.getenv("TELEGRAM_SOUND_START_HOUR", 9))
sound_end_hour = int(os.getenv("TELEGRAM_SOUND_END_HOUR", 18))
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

if not bot_token or not chat_id:
    raise ValueError("Bot token or chat ID not set. Please check your .env file.")

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

def send(message: str, parse_mode: str = "Markdown") -> None:
    """
    Відправляє повідомлення в Telegram: у робочий час — звичайне, у неробочий — беззвучне
    """
    
    now = datetime.now()
    current_hour = now.hour
    is_work_time = sound_start_hour <= current_hour < sound_end_hour

    telegram_max_symbol = 4096
    if len(message) > telegram_max_symbol:
                message = message[:telegram_max_symbol]

    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": parse_mode,
            "disable_notification": not is_work_time  # Беззвучно, якщо не в робочий час
        }
        my_rez=requests.post(url, json=payload, timeout=10)
            
        if my_rez.status_code == 200:
            logging.info(f"Message sent successfully to chat_id={chat_id}")
        else:
            logging.error(f"Message sent with reason: {my_rez.reason}")
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending message: {e}") # помилки, пов’язані з HTTP-запитами
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    