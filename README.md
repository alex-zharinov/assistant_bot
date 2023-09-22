# Assistant Bot

[![assistant-bot workflow](https://github.com/alex-zharinov/assistant_bot/actions/workflows/main.yml/badge.svg)](https://github.com/alex-zharinov/assistant_bot/actions/workflows/main.yml)

## Telegram-бот для проверки статуса
> Telegram-бот, который обращается к API сервиса и узнаёт статус работы.

## Технологии проекта:
- Python — высокоуровневый язык программирования;
- Telegram Client API — это интерфейс программирования приложений;
- Telegram Bot API — интерфейс к ядру мессенджера, предназначенный для создания ботов;

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/alex-zharinov/assistant_bot.git
```
```
cd assistant_bot
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv
```
* Если у вас Linux/macOS
    ```
    source venv/bin/activate
    ```
* Если у вас windows
    ```
    source venv/scripts/activate
    ```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Запустить бота:
```
python3 homework.py 
```

## Что делает бот:
- раз в 10 минут опрашивает API сервиса и проверяет статус работы;
- при обновлении статуса анализирует ответ API и отправляет соответствующее уведомление в Telegram;
- логирует свою работу и сообщает о важных проблемах сообщением в Telegram.

## Автор
[Жаринов Алексей](https://github.com/alex-zharinov)
