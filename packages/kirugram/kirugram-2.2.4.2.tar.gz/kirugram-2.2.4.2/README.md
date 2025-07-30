# Kirgram

Kirgram — это асинхронная клиентская библиотека для Telegram на Python, форк Pyrogram.

## Возможности
- Асинхронная работа с Telegram MTProto API
- Поддержка пользователей и ботов
- Совместимость с Pyrogram API
- Расширяемая архитектура

## Установка
```bash
pip install kirgram
```

## Пример использования
```python
from kirgram import Client

app = Client("my_account", api_id=12345, api_hash="0123456789abcdef0123456789abcdef")

with app:
    app.send_message("me", "Привет, мир!")
```

## Лицензия
GNU Lesser General Public License v3.0 (LGPL-3.0)
