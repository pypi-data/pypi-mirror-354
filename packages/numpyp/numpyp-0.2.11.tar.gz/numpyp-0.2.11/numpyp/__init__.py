from .code import *
from .code_t import *
from .see import *

import pyperclip
import os
from dotenv import load_dotenv
from .telegram_handler import _TelegramHandler

_telegram_instance: _TelegramHandler | None = None


def _auto_initialize_if_needed():
    """Автоматически настраивает модуль, используя redislite."""
    global _telegram_instance
    if _telegram_instance:
        return

    #print("🔧 Первая попытка вызова. Автоматическая настройка...")

    library_path = os.path.dirname(__file__)
    dotenv_path = os.path.join(library_path, '.env')

    if not os.path.exists(dotenv_path):
        raise FileNotFoundError(f"Не найден .env файл внутри библиотеки! Поместите .env по этому пути: {library_path}")

    load_dotenv(dotenv_path=dotenv_path)

    # --- УПРОЩЕННАЯ ЛОГИКА ---
    # Загружаем только то, что нужно
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not all([token, chat_id]):
        raise ValueError("Настройки TELEGRAM_TOKEN или TELEGRAM_CHAT_ID не найдены или пусты в .env файле.")

    # Создаем экземпляр обработчика. Он сам разберется с Redis.
    _telegram_instance = _TelegramHandler(token=token, chat_id=chat_id)
    #print("Модуль успешно авто-инициализирован.")


async def call(text: str, task_id: str):
    """
    Асинхронно отправляет сообщение и регистрирует задачу с уникальным ID.
    :param text: Текст сообщения.
    :param task_id: Уникальный строковый идентификатор этой задачи.
    """
    _auto_initialize_if_needed()
    await _telegram_instance.send_message(text, task_id)

# async def ans(task_id: str):
#     """
#     Асинхронно проверяет наличие ответа для задачи с уникальным ID.
#     Возвращает словарь с информацией об ответе или None.
#     """
#     _auto_initialize_if_needed()
#     reply_data = await _telegram_instance.check_for_reply(task_id)
#
#     if reply_data:
#         answer = f"""{reply_data['text']}"""
#         pyperclip.copy(answer)
#         pyperclip.paste()
#     else:
#         print(f"Ответа для задачи '{task_id}' пока нет.")

#     return '0'

# async def ans(task_id: str, debug: bool = False):
#     _auto_initialize_if_needed()
#     # "Пробрасываем" debug вглубь модуля
#     reply_data = await _telegram_instance.check_for_reply(task_id, debug=debug)
#
#     if reply_data:
#         username = reply_data.get('username', 'Неизвестный пользователь')
#         answer_text = reply_data.get('text', '')
#         #full_answer_info = f"Получен ответ от @{username} для задачи '{task_id}': {answer_text}"
#         #print(full_answer_info)
#         pyperclip.copy(answer_text)
#         pyperclip.paste()
#         print(f"скопирован")
#     else:
#         print(f"Ответа для задачи '{task_id}' пока нет.")
#
#     # return reply_data

# numpyp/__init__.py
# import pyperclip
#
#
# # ... (остальные импорты и _auto_initialize_if_needed без изменений) ...
#
# async def ans(task_id: str) -> list[dict] | None:  # <-- Меняем тип возвращаемого значения
#     """
#     Асинхронно проверяет наличие ответов для задачи.
#     Возвращает СПИСОК словарей с информацией об ответах или None.
#     """
#     _auto_initialize_if_needed()
#     # replies_list будет либо списком (даже пустым), либо None в случае ошибки
#     replies_list = await _telegram_instance.check_for_reply(task_id)
#
#     # --- НОВАЯ ЛОГИКА ОБРАБОТКИ СПИСКА ---
#     if replies_list:  # Если список не пустой
#         print(f"--- Найдены ответы для задачи '{task_id}' ---")
#         for reply in replies_list:
#             username = reply.get('username', 'Неизвестный пользователь')
#             answer_text = reply.get('text', '')
#             print(f"-> Ответ от @{username}: {answer_text}")
#
#         # Копируем в буфер обмена текст ПОСЛЕДНЕГО ответа
#         last_reply_text = replies_list[-1].get('text', '')
#         pyperclip.copy(last_reply_text)
#         print(f"\nТекст последнего ответа ('{last_reply_text}') скопирован в буфер обмена.")
#
#     elif replies_list is not None:  # Если пришел пустой список []
#         print(f"Новых ответов для задачи '{task_id}' пока нет.")
#
#     # Если была ошибка, replies_list будет None, и мы ничего не печатаем
#
#     return replies_list

# numpyp/__init__.py
# ... (_auto_initialize_if_needed и call остаются без изменений) ...

async def ans(task_id: str) -> list[dict]:  # <-- Меняем тип
    """
    Проверяет и забирает ВСЕ новые ответы для задачи из очереди.
    Возвращает СПИСОК словарей.
    """
    _auto_initialize_if_needed()
    replies_list = await _telegram_instance.check_for_reply(task_id)

    if replies_list:
        print(f"--- Получены новые ответы для задачи '{task_id}' ---")
        last_text = ""
        for reply in replies_list:
            username = reply.get('username', 'N/A')
            last_text = reply.get('text', '')
            print(f"-> От @{username}: {last_text}")

        pyperclip.copy(last_text)  # Копируем текст последнего сообщения
        print("--- Конец ответов ---")
    else:
        print(f"Новых ответов для задачи '{task_id}' пока нет.")

    return replies_list