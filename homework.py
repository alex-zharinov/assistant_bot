import logging
import os
import requests
import time
import telegram
import sys

from dotenv import load_dotenv


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
    if not(PRACTICUM_TOKEN and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID):
        logger.critical(
            'Отсутствие переменных окружения во время запуска бота'
        )
        raise SystemExit('Not specified tokens')


def send_message(bot, message):
    """Отправка сообщения."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except Exception as error:
        logger.error(f'Сбой в отправке сообщения - {error}')
    logger.debug(f'Сообщение: {message} - успешно отправлено!')


def get_api_answer(timestamp):
    """Получение ответа api."""
    payload = {'from_date': timestamp}

    try:
        homework_statuses = requests.get(
            ENDPOINT, headers=HEADERS, params=payload
        )
        homework_statuses.raise_for_status()
    except requests.RequestException:
        message = f'Код ответа API: {homework_statuses.status_code}'
        logger.error(message)
        raise requests.RequestException(message)
    except Exception as error:
        logger.error(f'Ошибка запроса к эндпоинту - {error}')
    if requests.get(
        ENDPOINT, headers=HEADERS, params=payload
    ).status_code != 200:
        raise('Сервер API недоступен!')
    return homework_statuses.json()


def check_response(response):
    """Проверка новых статусов."""
    if type(response) != dict:
        raise TypeError()
    if type(response.get('homeworks')) != list:
        raise TypeError()
    if response.get('homeworks') == []:
        logger.debug('Новые статусы отутствуют!')
        return False
    return True


def parse_status(homework):
    """Парсинг ответа api."""
    if 'homework_name' not in homework:
        raise KeyError()
    try:
        verdict = HOMEWORK_VERDICTS[homework.get('status')]
        homework_name = homework['homework_name']
    except Exception as error:
        logger.error(f'Ошибка запроса к эндпоинту - {error}')
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    check_tokens()

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())

    while True:
        try:
            response = get_api_answer(timestamp)
            timestamp = response.get('current_date')
            if check_response(response):
                homework = response.get('homeworks')[0]
                send_message(bot, parse_status(homework))

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            send_message(bot, message)
            logger.error(f'Ошибка работы - {error}')
        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
