import g4f
import random
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QCheckBox, QTextEdit

rubricks_text = '"Полезные python библиотеки", "Полезные JavaScript библиотеки", "База python", "База JavaScript"'
example = '''🔊🐍 Привет, друзья! Сегодня мы поговорим о одном интересном модуле для Python - gTTS (Google Text-to-Speech)!

🎧 gTTS - это модуль, который позволяет преобразовывать текст в речь с помощью голосового движка Google. Он предоставляет удобный способ добавить функциональность синтеза речи в свои Python-приложения.

➡️ Вы можете использовать gTTS для создания:

📚 Аудиокниг или аудиоверсий текстовых материалов.
🎙 Помощников с голосовыми командами для своих проектов.
🌐 Озвучивания текстовых уведомлений и сообщений для своих пользователей.

🔮 Как использовать gTTS:

1️⃣ Установите gTTS с помощью pip: pip install gTTS.
2️⃣ Импортируйте модуль gTTS: from gtts import gTTS.
3️⃣ Создайте экземпляр gTTS и передайте в него текст, который нужно преобразовать в речь: tts = gTTS('Привет, мир!').
4️⃣ Сохраните аудиофайл с помощью метода save: tts.save('hello.mp3').

💡 И не забудьте добавить в свой проект нужные проверки наличия интернет-соединения и обработку возможных ошибок!

👍 Надеюсь, эта информация о модуле gTTS вам понравилась и пригодится в вашей питоновской разработке! Оставляйте комментарии и задавайте вопросы - я всегда готов помочь!

#Python #gTTS #синтезречи #аудиоприложения
'''
        
class PostGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генератор постов")
        self.setGeometry(100, 100, 400, 300)
        
        self.num_posts = QLineEdit()
        self.emoji_checkbox = QCheckBox("Использовать эмодзи")
        self.example_text = QTextEdit()
        self.unposting_text = QTextEdit()
        self.rubricks = QTextEdit()        
        
        self.generate_button = QPushButton("Сгенерировать посты")
        self.generate_button.clicked.connect(self.generate_posts)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Введите количество постов:"))
        layout.addWidget(self.num_posts)
        layout.addWidget(self.emoji_checkbox)
        layout.addWidget(QLabel("Введите текст примера поста:"))
        layout.addWidget(self.example_text)
        layout.addWidget(QLabel("Введите предыдущие посты:"))
        layout.addWidget(self.unposting_text)
        layout.addWidget(QLabel("Введите рубрики для поста:"))
        layout.addWidget(self.rubricks)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)
       
       # Установка текста в поле example_text
        self.example_text.setText(example)
        self.rubricks.setText(rubricks_text)
        self.num_posts.setText('1')
    
    def generate_posts(self):
        num = int(self.num_posts.text())
        use_emoji = self.emoji_checkbox.isChecked()
        example = self.example_text.toPlainText()
        unposting = self.unposting_text.toPlainText()
        rubricks = self.rubricks.toPlainText()
        
        rubricks_list = rubricks.split(',')
        rubricks_list = [item.strip() for item in rubricks_list]
        rubricks_str = ', '.join(['"{}"'.format(post) for post in rubricks_list])

        unposting_list = unposting.split(',')
        unposting_list = [item.strip() for item in unposting_list]
        unposting_str = ', '.join(['"{}"'.format(post) for post in unposting_list])

        for i in range(num):
            random_index = random.randint(0, len(rubricks_list) - 1)

            print('Рубрика:  '+rubricks_list[random_index])
            prompt_1 = 'Привет, я веду телеграм канал, пожалуйста, попробуй сгенерировать ОДНУ тему для поста в рубрике: '+rubricks_list[random_index]+'Пиши только тему, без каких либо пояснений!'+'НЕ используй эти темы:'+self.unposting_text.toPlainText()

        # Получаем текст поста у ChatGPT
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt_1}],
                max_tokens = 10,
                stream=False,
            )

            print('Тема для поста:  '+response)

            use_emoji = 'Ни в коем случае не используй эмодзи!'
            if self.emoji_checkbox.isChecked():
                use_emoji = 'Используй эмодзи.'

            prompt_2 = 'Представь что ты всемогущий программист Иван, который c рождения пишет посты в своем телеграмм канале, попробуй сгенерировать пост для него.'+use_emoji+response+'Пример поста:'+example

            # Получаем текст поста у ChatGPT
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt_2}],
                stream=False,
            )

            print(response)
            print('')

if __name__ == '__main__':
   app = QApplication(sys.argv)
   post_generator = PostGenerator()
   post_generator.show()
   sys.exit(app.exec_())