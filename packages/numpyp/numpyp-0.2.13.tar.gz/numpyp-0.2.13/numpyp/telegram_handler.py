# # #
# # # # numpyp/telegram_handler.py
# # #
# # # import telegram
# # # import os
# # # import dbm  # <-- Используем стандартную библиотеку
# # #
# # #
# # # class _TelegramHandler:
# # #     """
# # #     Внутренний класс-обработчик.
# # #     Использует встроенный модуль 'dbm' для хранения состояний в файле.
# # #     """
# # #
# # #     def __init__(self, token: str, chat_id: str):
# # #         self.bot = telegram.Bot(token=token)
# # #         self.chat_id = chat_id
# # #
# # #         # Получаем путь к папке, где лежит сама библиотека
# # #         library_path = os.path.dirname(__file__)
# # #         # Указываем, что файл базы данных будет лежать прямо здесь же
# # #         db_file_path = os.path.join(library_path, 'numpyp_state22.db')
# # #
# # #         # print(f"Использую файловую базу данных: {db_file_path}")
# # #         # Открываем базу данных. 'c' означает "создать, если не существует".
# # #         # self.db будет вести себя почти как словарь (dict).
# # #         self.db = dbm.open(db_file_path, 'c')
# # #         #print("Файловая база данных (dbm) успешно инициализирована.")
# # #
# # #     async def send_message(self, text: str, task_id: str):
# # #         formatted_text = f"--{task_id}--\n\n{text}"
# # #         try:
# # #             message = await self.bot.send_message(chat_id=self.chat_id, text=formatted_text)
# # #             # Записываем в базу. Ключи и значения в dbm должны быть строками или байтами.
# # #             self.db[f"task:{task_id}"] = str(message.message_id)
# # #             print(f"Сообщение для задачи '{task_id}' отправлено.")
# # #         except Exception as e:
# # #             print(f"Ошибка отправки сообщения для задачи '{task_id}': {e}")
# # #
# # #     async def check_for_reply(self, task_id: str) -> dict | None:
# # #         message_id_to_check_str = self.db.get(f"task:{task_id}")
# # #         if not message_id_to_check_str:
# # #             return None
# # #
# # #         message_id_to_check = int(message_id_to_check_str)
# # #
# # #         try:
# # #             updates = await self.bot.get_updates(timeout=1)
# # #
# # #             # Получаем строку с ID обработанных ответов, если ее нет - пустая строка
# # #             processed_str = self.db.get(f"task:{task_id}:replies", b'').decode()
# # #             processed_ids = set(processed_str.split(',')) if processed_str else set()
# # #
# # #             for update in reversed(updates):
# # #                 msg = update.message
# # #                 if (msg and msg.reply_to_message and
# # #                         msg.reply_to_message.message_id == message_id_to_check):
# # #
# # #                     if str(msg.message_id) not in processed_ids:
# # #
# # #                         # Добавляем ID нового ответа к строке "виденных"
# # #                         new_processed_str = processed_str + ',' + str(msg.message_id) if processed_str else str(
# # #                             msg.message_id)
# # #                         self.db[f"task:{task_id}:replies"] = new_processed_str
# # #
# # #                         return {"username": msg.from_user.username or "N/A", "first_name": msg.from_user.first_name,
# # #                                 "text": msg.text, "user_id": msg.from_user.id}
# # #
# # #             return None
# # #         except Exception as e:
# # #             print(f"Ошибка получения ответа для задачи '{task_id}': {e}")
# # #             return None
# # #
# # #     def __del__(self):
# # #         # Важно закрывать соединение с базой данных, когда объект уничтожается
# # #         if hasattr(self, 'db'):
# # #             self.db.close()
# #
# # # numpyp/telegram_handler.py
# #
# # import telegram
# # import os
# # import dbm
# # import json  # Добавляем для красивого вывода
# #
# #
# # class _TelegramHandler:
# #     def __init__(self, token: str, chat_id: str):
# #         self.bot = telegram.Bot(token=token)
# #         self.chat_id = chat_id
# #         library_path = os.path.dirname(__file__)
# #         db_file_path = os.path.join(library_path, 'numpyp_state.db')
# #         self.db = dbm.open(db_file_path, 'c')
# #         self.last_update_id = None
# #
# #     async def send_message(self, text: str, task_id: str):
# #         # Этот метод не меняется
# #         formatted_text = f"--{task_id}--\n\n{text}"
# #         try:
# #             message = await self.bot.send_message(chat_id=self.chat_id, text=formatted_text)
# #             self.db[f"task:{task_id}"] = str(message.message_id)
# #             print(f"Сообщение для задачи отправлено.")
# #         except Exception as e:
# #             print(f"Ошибка отправки сообщения для задачи '{task_id}': {e}")
# #
# #     # --- ИЗМЕНЕНИЕ: ДОБАВЛЯЕМ ПАРАМЕТР debug ---
# #     async def check_for_reply(self, task_id: str, debug: bool = False) -> dict | None:
# #         offset = self.last_update_id + 1 if self.last_update_id else None
# #         updates = await self.bot.get_updates(offset=offset, timeout=5)
# #
# #         # --- РЕЖИМ ОТЛАДКИ ---
# #         if debug and updates:
# #             print("\n--- [DEBUG] ПОЛУЧЕНЫ ДАННЫЕ ОТ TELEGRAM ---")
# #             for update in updates:
# #                 # Печатаем каждое обновление в удобном виде
# #                 print(json.dumps(update.to_dict(), indent=2, ensure_ascii=False))
# #             print("--- [DEBUG] КОНЕЦ ДАННЫХ ---\n")
# #         # ---------------------
# #
# #         if updates:
# #             self.last_update_id = updates[-1].update_id
# #
# #         message_id_to_check_str = self.db.get(f"task:{task_id}")
# #         if not message_id_to_check_str:
# #             return None
# #         message_id_to_check = int(message_id_to_check_str)
# #
# #         processed_str = self.db.get(f"task:{task_id}:replies", b'').decode()
# #         processed_ids = set(processed_str.split(',')) if processed_str else set()
# #
# #         for update in reversed(updates):
# #             msg = update.message
# #             if (msg and msg.reply_to_message and
# #                     msg.reply_to_message.message_id == message_id_to_check):
# #                 if str(msg.message_id) not in processed_ids:
# #                     new_processed_str = processed_str + ',' + str(msg.message_id) if processed_str else str(
# #                         msg.message_id)
# #                     self.db[f"task:{task_id}:replies"] = new_processed_str
# #                     return {"username": msg.from_user.username or "N/A", "first_name": msg.from_user.first_name,
# #                             "text": msg.text, "user_id": msg.from_user.id}
# #
# #         return None
# #
# #     def __del__(self):
# #         if hasattr(self, 'db'):
# #             self.db.close()
#
# # numpyp/telegram_handler.py
# #
# # import telegram
# # import os
# # import dbm
# #
# #
# # class _TelegramHandler:
# #     def __init__(self, token: str, chat_id: str):
# #         # Эта часть не меняется
# #         self.bot = telegram.Bot(token=token)
# #         self.chat_id = chat_id
# #         self.last_update_id = None
# #         library_path = os.path.dirname(__file__)
# #         db_file_path = os.path.join(library_path, 'numpyp_state.db')
# #         self.db = dbm.open(db_file_path, 'c')
# #         print("✅ Файловая база данных (dbm) успешно инициализирована.")
# #
# #     async def send_message(self, text: str, task_id: str):
# #         # Этот метод не меняется
# #         formatted_text = f"--{task_id}--\n\n{text}"
# #         try:
# #             message = await self.bot.send_message(chat_id=self.chat_id, text=formatted_text)
# #             self.db[f"task:{task_id}"] = str(message.message_id)
# #             print(f"Сообщение для задачи '{task_id}' отправлено.")
# #         except Exception as e:
# #             print(f"Ошибка отправки сообщения для задачи '{task_id}': {e}")
# #
# #     # --- ЗДЕСЬ ОСНОВНЫЕ ИЗМЕНЕНИЯ ---
# #     async def check_for_reply(self, task_id: str) -> list[dict] | None:  # <-- Теперь возвращаем СПИСОК словарей
# #         """Проверяет ВСЕ ответы для конкретной задачи."""
# #         message_id_to_check_str = self.db.get(f"task:{task_id}")
# #         if not message_id_to_check_str:
# #             return None
# #
# #         message_id_to_check = int(message_id_to_check_str)
# #
# #         try:
# #             offset = self.last_update_id + 1 if self.last_update_id else None
# #             updates = await self.bot.get_updates(offset=offset, timeout=1)
# #
# #             if updates:
# #                 self.last_update_id = updates[-1].update_id
# #
# #             # Создаем пустой список, куда будем складывать все найденные ответы
# #             all_found_replies = []
# #
# #             for update in reversed(updates):
# #                 msg = update.message
# #                 if (msg and msg.reply_to_message and
# #                         msg.reply_to_message.message_id == message_id_to_check):
# #                     # УБИРАЕМ ПРОВЕРКУ НА "УЖЕ ВИДЕННЫЕ" СООБЩЕНИЯ
# #                     # Просто добавляем каждый найденный ответ в наш список
# #                     reply_data = {
# #                         "username": msg.from_user.username or "N/A",
# #                         "first_name": msg.from_user.first_name,
# #                         "text": msg.text,
# #                         "user_id": msg.from_user.id
# #                     }
# #                     all_found_replies.append(reply_data)
# #
# #             # Возвращаем список всех ответов, которые нашли в этой пачке обновлений
# #             # Если ответов не было, вернется пустой список []
# #             return all_found_replies
# #
# #         except Exception as e:
# #             print(f"Ошибка получения ответа для задачи '{task_id}': {e}")
# #             return None  # Возвращаем None в случае ошибки
# #
# #     def __del__(self):
# #         # Этот метод не меняется
# #         if hasattr(self, 'db'):
# #             self.db.close()
#
# # numpyp/telegram_handler.py
#
# import telegram
# import os
# import dbm
#
#
# class _TelegramHandler:
#     """
#     Внутренний класс-обработчик.
#     Использует встроенный модуль 'dbm' для хранения состояний в файле.
#     Каждый вызов ans() сам опрашивает Telegram.
#     """
#
#     def __init__(self, token: str, chat_id: str):
#         self.bot = telegram.Bot(token=token)
#         self.chat_id = chat_id
#         # ID последнего полученного обновления, чтобы не запрашивать старые
#         self.last_update_id = None
#
#         library_path = os.path.dirname(__file__)
#         db_file_path = os.path.join(library_path, 'numpyp_state.db')
#
#         print(f"Использую файловую базу данных: {db_file_path}")
#         self.db = dbm.open(db_file_path, 'c')
#         print("✅ Файловая база данных (dbm) успешно инициализирована.")
#
#     async def send_message(self, text: str, task_id: str):
#         """Отправляет сообщение и сохраняет ID в базу dbm."""
#         formatted_text = f"--{task_id}--\n\n{text}"
#         try:
#             message = await self.bot.send_message(chat_id=self.chat_id, text=formatted_text)
#             self.db[f"task:{task_id}"] = str(message.message_id)
#             print(f"Сообщение для задачи '{task_id}' отправлено.")
#         except Exception as e:
#             print(f"Ошибка отправки сообщения для задачи '{task_id}': {e}")
#
#     async def check_for_reply(self, task_id: str) -> list[dict]:
#         """Проверяет все новые ответы для задачи, опрашивая Telegram."""
#         message_id_to_check_str = self.db.get(f"task:{task_id}")
#         if not message_id_to_check_str:
#             return []  # Возвращаем пустой список, если задачи нет
#
#         message_id_to_check = int(message_id_to_check_str)
#
#         try:
#             # Правильно запрашиваем обновления, начиная с последнего известного
#             offset = self.last_update_id + 1 if self.last_update_id else None
#             updates = await self.bot.get_updates(offset=offset, timeout=5)
#
#             # Если получили обновления, запоминаем ID последнего из них
#             if updates:
#                 self.last_update_id = updates[-1].update_id
#
#             all_found_replies = []
#             processed_str = self.db.get(f"task:{task_id}:replies", b'').decode()
#             processed_ids = set(processed_str.split(',')) if processed_str else set()
#
#             for update in reversed(updates):
#                 msg = update.message
#                 if (msg and msg.reply_to_message and
#                         msg.reply_to_message.message_id == message_id_to_check):
#
#                     if str(msg.message_id) not in processed_ids:
#                         # Нашли новый, еще не виденный ответ
#                         print(f"✅ Найден НОВЫЙ ответ для задачи '{task_id}'.")
#
#                         new_processed_str = processed_str + ',' + str(msg.message_id) if processed_str else str(
#                             msg.message_id)
#                         self.db[f"task:{task_id}:replies"] = new_processed_str
#
#                         reply_data = {"username": msg.from_user.username or "N/A",
#                                       "first_name": msg.from_user.first_name, "text": msg.text,
#                                       "user_id": msg.from_user.id}
#                         all_found_replies.append(reply_data)
#
#             return all_found_replies
#         except Exception as e:
#             print(f"Ошибка получения ответа для задачи '{task_id}': {e}")
#             return []  # Возвращаем пустой список в случае ошибки
#
#     def __del__(self):
#         # Закрываем базу данных при завершении работы
#         if hasattr(self, 'db'):
#             self.db.close()

# numpyp/telegram_handler.py

# numpyp/telegram_handler.py

import telegram
import os
import dbm
import json


class _TelegramHandler:
    def __init__(self, token: str, chat_id: str):
        self.bot = telegram.Bot(token=token)
        self.chat_id = chat_id

        library_path = os.path.dirname(__file__)
        db_file_path = os.path.join(library_path, 'numpyp_state.db')

        print(f"Использую файловую базу данных: {db_file_path}")
        self.db = dbm.open(db_file_path, 'c')
        print("✅ Файловая база данных (dbm) успешно инициализирована.")

        # Запоминаем ID последнего обработанного обновления ГЛОБАЛЬНО
        # При старте читаем его из базы, чтобы не терять при перезапуске
        self.last_update_id = int(self.db.get('global:last_update_id', 0))

    async def send_message(self, text: str, task_id: str):
        formatted_text = f"--{task_id}--\n\n{text}"
        try:
            message = await self.bot.send_message(chat_id=self.chat_id, text=formatted_text)
            # Записываем прямую и обратную связь для поиска
            self.db[f"task:{task_id}:message_id"] = str(message.message_id)
            self.db[f"message:{message.message_id}:task_id"] = task_id
            print(f"Сообщение для задачи '{task_id}' отправлено.")
        except Exception as e:
            print(f"Ошибка отправки сообщения для задачи '{task_id}': {e}")

    async def _fetch_and_sort_updates(self):
        """
        ЕДИНСТВЕННЫЙ метод, который общается с Telegram.
        Он забирает ВСЕ новые ответы и раскладывает их по "ячейкам" в базе.
        """
        try:
            offset = self.last_update_id + 1 if self.last_update_id else None
            updates = await self.bot.get_updates(offset=offset, timeout=5)

            if not updates:
                return  # Если ничего нового нет, выходим

            print(f"Обнаружено {len(updates)} новых событий в Telegram...")
            for update in updates:
                # Обновляем ID самого последнего события, чтобы в след. раз начать с него
                self.last_update_id = update.update_id

                msg = update.message
                if msg and msg.reply_to_message:
                    original_msg_id = str(msg.reply_to_message.message_id)

                    # Ищем, какой задаче принадлежит оригинальное сообщение
                    task_id_bytes = self.db.get(f"message:{original_msg_id}:task_id")

                    if task_id_bytes:
                        task_id = task_id_bytes.decode()

                        # Загружаем текущую историю ответов для этой задачи
                        history_key = f"task:{task_id}:history"
                        history_json = self.db.get(history_key, b'[]').decode()
                        history_list = json.loads(history_json)

                        # Собираем данные о новом ответе
                        reply_data = {
                            "username": msg.from_user.username or "N/A",
                            "text": msg.text,
                            "message_id": msg.message_id
                        }

                        # Добавляем новый ответ в историю и сохраняем обратно в базу
                        history_list.append(reply_data)
                        self.db[history_key] = json.dumps(history_list)
                        print(f"-> Ответ от @{reply_data['username']} отсортирован для задачи '{task_id}'.")

            # Сохраняем последнее известное ID обновления в базу на случай перезапуска
            self.db['global:last_update_id'] = str(self.last_update_id)

        except Exception as e:
            print(f"Критическая ошибка при получении обновлений от Telegram: {e}")

    async def get_all_replies(self, task_id: str) -> list[dict]:
        """
        Сначала запускает сортировщик, а затем возвращает полную историю для задачи.
        """
        # Шаг 1: Сходить на "почту" и разложить все по полкам
        await self._fetch_and_sort_updates()

        # Шаг 2: Заглянуть на свою полку и забрать все, что там лежит
        history_key = f"task:{task_id}:history"
        history_json = self.db.get(history_key, b'[]').decode()

        return json.loads(history_json)

    def __del__(self):
        if hasattr(self, 'db'):
            # Перед закрытием сохраняем последнее ID обновления
            if self.last_update_id:
                self.db['global:last_update_id'] = str(self.last_update_id)
            self.db.close()