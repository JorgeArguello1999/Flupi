from dotenv import load_dotenv
load_dotenv()

import requests
import os 

bot_token = os.getenv('TELEGRAM_TOKEN') 
chat_id = os.getenv('CHAT_ID') 
url = f'https://api.telegram.org/bot{bot_token}/sendMessage' 

def send_message(message:str) -> bool:
    params = {'chat_id': chat_id, 'text': message}

    try:
        requests.post(url, params=params)
        return True

    except Exception as e:
        print("Error: ", e)
        print("Revisar el Token e ID del chat sean correctos")
        return False

if __name__ == "__main__":
    send_message("Bienvenido")