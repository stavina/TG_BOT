import datetime
import os

from my_loguru import Logger



def log_decorator(sender, user_id, message):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{formatted_time}: {sender} - {message}"
    log_folder = r"D:\LA\TGBOT_Stepanova\app\logs\message_history"

    # Создаем папку, если она не существует
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Создайте файл или откройте существующий для записи
    log_file_path = os.path.join(log_folder, f"user_{user_id}_chat_log.txt")
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(log_entry + "\n")