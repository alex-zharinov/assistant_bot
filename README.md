# Homework Bot

[![homework-bot workflow](https://github.com/alex-zharinov/homework_bot/actions/workflows/main.yml/badge.svg)](https://github.com/alex-zharinov/homework_bot/actions/workflows/main.yml)

## Telegram-бот для проверки домашки
> Telegram-бот, который обращаться к API сервиса Практикум.Домашка и узнаваёт статус домашней работы: взята ли домашка в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.

## Технологии проекта:
- Python — высокоуровневый язык программирования;
- Telegram Client API — это интерфейс программирования приложений;
- Telegram Bot API — интерфейс к ядру мессенджера, предназначенный для создания ботов;
- API Практикум.Домашка — API, через который можно отслеживать статуса домашней работы.

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/alex-zharinov/homework_bot.git
```
```
cd homework_bot
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
Запустить проект:
```
python3 homework.py 
```

## Что делает бот:
- раз в 10 минут опрашивает API сервиса Практикум.Домашка и проверяет статус отправленной на ревью домашней работы;
- при обновлении статуса анализирует ответ API и отправляет соответствующее уведомление в Telegram;
- логирует свою работу и сообщает о важных проблемах сообщением в Telegram.

## Автор
[Жаринов Алексей](https://github.com/alex-zharinov)