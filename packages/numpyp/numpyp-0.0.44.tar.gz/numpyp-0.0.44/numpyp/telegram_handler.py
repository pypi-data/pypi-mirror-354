
# numpyp/telegram_handler.py

import telegram
import os
import dbm  # <-- Используем стандартную библиотеку


class _TelegramHandler:
    """
    Внутренний класс-обработчик.
    Использует встроенный модуль 'dbm' для хранения состояний в файле.
    """

    def __init__(self, token: str, chat_id: str):
        self.bot = telegram.Bot(token=token)
        self.chat_id = chat_id

        # Получаем путь к папке, где лежит сама библиотека
        library_path = os.path.dirname(__file__)
        # Указываем, что файл базы данных будет лежать прямо здесь же
        db_file_path = os.path.join(library_path, 'numpyp_state.db')

        # print(f"Использую файловую базу данных: {db_file_path}")
        # Открываем базу данных. 'c' означает "создать, если не существует".
        # self.db будет вести себя почти как словарь (dict).
        self.db = dbm.open(db_file_path, 'c')
        #print("Файловая база данных (dbm) успешно инициализирована.")

    async def send_message(self, text: str, task_id: str):
        formatted_text = f"--{task_id}--\n\n{text}"
        try:
            message = await self.bot.send_message(chat_id=self.chat_id, text=formatted_text)
            # Записываем в базу. Ключи и значения в dbm должны быть строками или байтами.
            self.db[f"task:{task_id}"] = str(message.message_id)
            print(f"Сообщение для задачи '{task_id}' отправлено.")
        except Exception as e:
            print(f"Ошибка отправки сообщения для задачи '{task_id}': {e}")

    async def check_for_reply(self, task_id: str) -> dict | None:
        message_id_to_check_str = self.db.get(f"task:{task_id}")
        if not message_id_to_check_str:
            return None

        message_id_to_check = int(message_id_to_check_str)

        try:
            updates = await self.bot.get_updates(timeout=1)

            # Получаем строку с ID обработанных ответов, если ее нет - пустая строка
            processed_str = self.db.get(f"task:{task_id}:replies", b'').decode()
            processed_ids = set(processed_str.split(',')) if processed_str else set()

            for update in reversed(updates):
                msg = update.message
                if (msg and msg.reply_to_message and
                        msg.reply_to_message.message_id == message_id_to_check):

                    if str(msg.message_id) not in processed_ids:

                        # Добавляем ID нового ответа к строке "виденных"
                        new_processed_str = processed_str + ',' + str(msg.message_id) if processed_str else str(
                            msg.message_id)
                        self.db[f"task:{task_id}:replies"] = new_processed_str

                        return {"username": msg.from_user.username or "N/A", "first_name": msg.from_user.first_name,
                                "text": msg.text, "user_id": msg.from_user.id}

            return None
        except Exception as e:
            print(f"Ошибка получения ответа для задачи '{task_id}': {e}")
            return None

    def __del__(self):
        # Важно закрывать соединение с базой данных, когда объект уничтожается
        if hasattr(self, 'db'):
            self.db.close()