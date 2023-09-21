import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

from exceptions import BadHTTPStatus

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Проверка наличия необходимых токенов."""
    return all((PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID))


def send_message(bot, message):
    """Отправка сообщения."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.debug(f'Сообщение: {message} - успешно отправлено!')
    except Exception as error:
        logger.error(f'Сбой в отправке сообщения - {error}')
        raise Exception(f'Сбой в отправке сообщения - {error}')


def get_api_answer(timestamp):
    """Получение ответа api."""
    get_api_dict = {
        'url': ENDPOINT,
        'headers': HEADERS,
        'params': {'from_date': timestamp},
    }
    try:
        response = requests.get(**get_api_dict)
        if response.status_code != HTTPStatus.OK:
            raise BadHTTPStatus(
                f'Нет доступа к API по адресу {response.url}.'
                f'Код HTTP ответа сервера: {response.status_code}.'
            )
    except requests.RequestException as exc:
        response.raise_for_status()
        raise requests.RequestException(exc)
    except Exception as exc:
        raise Exception(f'Ошибка при подключении к эндойнту: {exc}')
    return response.json()


def check_response(response):
    """Проверка новых статусов."""
    if type(response) != dict:
        raise TypeError('type(response) != dict')
    if type(response.get('homeworks')) != list:
        raise TypeError('type(response.get("homeworks")) != list')
    return response.get('homeworks')


def parse_status(homework):
    """Парсинг ответа api."""
    if 'homework_name' not in homework:
        raise KeyError('ключ "homework_name" в списке домашек отсутствует!')
    try:
        verdict = HOMEWORK_VERDICTS[homework.get('status')]
        homework_name = homework['homework_name']
    except Exception as error:
        raise Exception(error)
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logger.critical(
            'Отсутствие переменных окружения во время запуска бота'
        )
        raise SystemExit('Not specified tokens')

    message = ''
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())

    while True:
        try:
            response = get_api_answer(timestamp)
            timestamp = response.get('current_date')
            homework = check_response(response)
            if homework == []:
                new_message = 'Новые статусы отутствуют!'
            else:
                new_message = parse_status(homework[0])
        except Exception as error:
            logger.error(error)
            new_message = f'Сбой в работе программы: {error}'
            send_message(bot, message)
        finally:
            if new_message != message:
                try:
                    send_message(bot, new_message)
                except Exception as error:
                    logger.error(f'Ошибка отправки сообщения - {error}')
                    raise Exception(f'Ошибка отправки сообщения - {error}')
                message = new_message
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
