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

#
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

# async def ans(task_id: str) :
#     """
#     Асинхронно проверяет наличие ответа для задачи с уникальным ID.
#     Возвращает словарь с информацией об ответе или None.
#     """
#     _auto_initialize_if_needed()
#     reply_data = await _telegram_instance.check_for_reply(task_id)
#
#     if reply_data:
#         # --- УЛУЧШЕННАЯ ЛОГИКА ---
#         # Формируем красивый вывод и копируем его в буфер обмена
#         username = reply_data.get('username', 'N/A')
#         answer_text = reply_data.get('text', '')
#
#         full_answer_info = f"Ответ от @{username}: {answer_text}"
#         #print(full_answer_info)
#
#         # Копируем в буфер обмена только сам текст ответа
#         pyperclip.copy(answer_text)
#         pyperclip.paste()
#
#         #print(f"Текст ответа ('{answer_text}') скопирован в буфер обмена.")
#     else:
#         print(f"Ответа для задачи '{task_id}' пока нет.")
#
#     # Возвращаем словарь с данными, чтобы вызывающий код мог с ним работать
#     # return reply_data

# numpyp/__init__.py

async def ans(task_id: str, debug: bool = False) -> dict | None:
    _auto_initialize_if_needed()
    # "Пробрасываем" debug вглубь модуля
    reply_data = await _telegram_instance.check_for_reply(task_id, debug=debug)

    if reply_data:
        username = reply_data.get('username', 'Неизвестный пользователь')
        answer_text = reply_data.get('text', '')
        full_answer_info = f"Получен ответ от @{username} для задачи '{task_id}': {answer_text}"
        print(full_answer_info)
        pyperclip.copy(answer_text)
        print(f"Текст ответа ('{answer_text}') скопирован в буфер обмена.")
    else:
        print(f"Ответа для задачи '{task_id}' пока нет.")

    return reply_data