from mistralai import Mistral
import random
import pyperclip

api_keys = [
    'uQwjntCIJ9omN9z8jLTV1VOUvYlbaDIv',
    'ZYftAsAwcHaPptlLhjwulyP3Sp966uVU',
    'Z0XHjxUHj6QXJblxACLxDhJoQAUreqt4',
    'iOSObqKAYAliBWRglH4gpZb7JN0KF91j',
    'E42w9TME0Ykm1WMsVwdzS6DxV9q2Xhgx',
    'uQmDdzM1nrw3cbmksP1BWhRnjOKGLWi1',
    'mtddNQsqAMbL5GNHroRNRsSOwOr8vusH',
    'tpxt5xsU7jetD1x9u9r0IiKxqwajlTXO',
    'bSJCJVsREAKubT9AgGfgYL6pojIzoK11',
    'icjd6jfH7hmPxNMSEyD70UKg13kbtaB5',
    'Oxz67oTMVHw48CJhJZOKLkHw1eAlTwki',
    'zVrmIUh4z2wEjS1ze9XpJtfbGQTGognI',
    'ez9voi9pZb7CwPbqrglrTSL59GgUZFCX',
    'BQUqloQ3WynP4ySfHhTOxz44Diidniq1',
    '0CYYJStJ3MrRB4Cvr7Z4GN2jXHG7hDmW',
    '3Hsc7xt2LjQsikCrKPOymzbCY8uAHjFp',
    '3w1mKshwprtQ0sqjNONIyC9quXysSEY0',
    'ueLqSHuosWQUUfcCyOdGYRojXkGGjsA6',
    'XasVSUM1K3c61JJyVb2fli6jF8alw8Qh',
    'XWuKPhFWuxSvyQMn3SOXl4afxCY0Aw58'
]

model = "mistral-large-latest"

def get(message: str):
    api_key = random.choice(api_keys)
    client = Mistral(api_key=api_key)

    try:
        chat_response = client.chat.complete(
            model=model,
            messages=[{"role": "user", "content": message}]
        )
        response_content = chat_response.choices[0].message.content
    except Exception as e:
        response_content = f'Ошибка: {e}'

    try:
        pyperclip.copy(response_content)
    except Exception as e:
        response_content += f"\n\n[!] Буфер обмена недоступен: {e}"

    return response_content

class get_cl:
    def __init__(self, message: str):
        api_key = random.choice(api_keys)
        client = Mistral(api_key=api_key)

        try:
            chat_response = client.chat.complete(
                model=model,
                messages=[{"role": "user", "content": message}]
            )
            self.answer = chat_response.choices[0].message.content
        except Exception as e:
            self.answer = f'Ошибка: {e}'

    @property
    def __doc__(self):
        return self.answer

