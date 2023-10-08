from dotenv import load_dotenv

load_dotenv()
import os

api_key = os.getenv("OPENAI_API_KEY")
print(api_key)  # це повинно вивести ваш ключ API або None, якщо ключ не було знайдено
