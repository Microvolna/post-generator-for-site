import g4f.Provider
from g4f.client import Client
import g4f
import random
from loguru import logger

from config import rubricks_text, example

def do_post():
    rubrick = rubricks_text[random.randint(0, len(rubricks_text)-1)]
    with open('used_themes.ini', 'r', encoding='UTF-8') as f:
        used_themes = ', '.join(f.read().split('\n'))[0:-2]

    # Генерируем тему поста
    client = Client()
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        provider=g4f.Provider.Aichatos,
        messages=[{"role": "system", "content": f'Привет, я веду телеграм канал, пожалуйста, попробуй сгенерировать ОДНУ тему для поста в рубрике: {rubrick}. Пиши только тему, без каких либо пояснений, без кавычек! НЕ используй эти темы: {used_themes}. Отвечай на русском языке (за исключением профессиональных терминов).'}])

    topic = response.choices[0].message.content
    logger.debug(f'Тема поста - {topic}')

    logger.debug(f'Генерирую тест поста - {topic}')

    if topic == '流量异常,请尝试更换网络环境':
        topic = 'Ненормальный трафик, пожалуйста, попробуйте изменить сетевую среду'
    else:

        with open('used_themes.ini', 'a', encoding='UTF-8') as f:
            f.write(f'{topic}\n')

        # Генерируем пост
        client = Client()
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            provider=g4f.Provider.Aichatos,
            messages=[{"role": "system", "content": f'Ты всемогущий программист Иван, который c рождения пишет посты в своем телеграмм канале, попробуй сгенерировать пост для канала на тему - {topic}. Пример поста: {example}. Отвечай на русском языке (за исключением профессиональных терминов).'}])
        print(response.provider)

        post = response.choices[0].message.content

        return f'''```
Пост сгенерирован chatgpt [проект на гитхаб](https://example.com)

Рубрика поста - {rubrick}
Тема (генерируется автоматически) - {topic}
```
{post}'''