import requests
import importlib.resources
from .login import token

class Client:
    def __init__(self, model='gpt-4.1-2025-04-14'):
        self.url = 'http://5.35.46.26:10500/chat'
        self.model = model
        self.system_prompt = (
            'Всегда форматируй все формулы и символы в Unicode или ASCII. '
            'Не используй LaTeX или другие специальные вёрстки. '
            'Пиши по-русски.'
        )

    def get_response(self, message):
        """
        Отправляет запрос на сервер-прокси и возвращает ответ модели.
        """
        messages = [
            {'role': 'system', 'content': self.system_prompt},
            {'role': 'user',   'content': message}
        ]

        headers = {
            "Authorization": f"Bearer {token}",
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': self.model,
            'messages': messages
        }
        
        if self.model == 'o4-mini':
            data['reasoning_effort'] = 'medium'

        try:
            response = requests.post(self.url, headers=headers, json=data, timeout=600) # Увеличен таймаут
            response.raise_for_status() 
            
            jr = response.json()
            return jr['choices'][0]['message']['content']
        
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error occurred:")
            print(f"Status code: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
            raise 
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raw_response = response.text if 'response' in locals() else "N/A"
            print(f"Raw response from server: {raw_response}")
            return f"Error processing request: {e}"

def read_txt_file(file_name):
    """Читает текстовый файл из пакета."""
    with importlib.resources.open_text('danya.data', file_name) as file:
        return file.read()

def ask(message, m=1):
    """
    Отправляет запрос к модели через сервер-прокси и возвращает ответ.

    Параметры:
        message (str): Текст запроса.
        m (int): Номер модели для использования:
                 1 — gpt-4.1-2025-04-14 (мощная модель)
                 2 — o4-mini (облегченная и быстрая модель с reasoning)
    Возвращает:
        str: Ответ модели.
    """
    model_map = {
        1: 'gpt-4.1-2025-04-14',
        2: 'o4-mini'
    }
    
    model_name = model_map.get(m, 'gpt-4.1-2025-04-14')
    
    client = Client(model=model_name)
    return client.get_response(message)

def get(a='м'):
    """
    Возвращает содержимое файла с материалами по автору:
        'а' — artyom,
        'д' — danya,
        'м' — misha.
    """
    authors = {'а': 'artyom', 'д': 'danya', 'м': 'misha'}
    a = a.lower().replace('d', 'д').replace('a', 'а').replace('m', 'м')
    name = authors.get(a, 'misha') 
    return read_txt_file(f"{name}_dl.txt")