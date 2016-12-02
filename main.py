"""
Выполняет обмен с EDI провайдером 'Контур' с помощью веб-интерфейса
Перед запуском необходимо передать параметры с типами сообщений, по которым необходимо сделать обмен
Например: python exchange_kontur.py -i orders recadv
    -i - означает импорт данных
    -e - означает экспорт данных
"""

import configparser
import sys
import json
from io import StringIO
from kontur_api import KonturApi


def get_token(api):
    """
    Получим токен и по нему дальше будем проходить авторизацию
    Метод веб-сервиса Authenticate
    """
    try:
        result = api.run_requests('/V1/Authenticate', 'post')
    except:
        show_message('Не удалось получить токен!')
        raise SystemExit

    return result.text


def get_boxes(api):
    """Получим id транспортного ящика
        Метод веб-сервиса GetBoxesInfo"""
    try:
        result = api.run_requests('/V1/Boxes/GetBoxesInfo', 'get')
        io = StringIO(result.text)
        data = json.load(io)
        for box in data['Boxes']:
            if box['BoxSettings']['IsMain']:
                print(box)
            else:
                # Здесь надо удалить вложенный справочник из родительского
                data['Boxes'].remove(box)
        io.close()
    except:
        show_message('Не удалось получить список организаций')
        raise SystemExit

    return data['Boxes']


def show_message(message):
    print("ERROR: "+message)


def exchange():
    """"
    Основной метод. Здесь реализована вся логика скрипта
    Получает настройки для аутентификации, получает осн. транспортные ящики, выполняет обмен сообщениями
    """
    cfg = init_config()
    if not cfg["URL"] or not cfg['LOGIN'] or not cfg['PASSW'] or not cfg['KEY']:
        print('Не найдены стандартные настройки!')
        return None
    # Инициализация класса KonturApi
    kontur_api = KonturApi(cfg["URL"], cfg['LOGIN'], cfg['PASSW'], cfg['KEY'])
    # Получение токена для упрощенной схемы аутентификации при HTTP запросе
    kontur_api.token = get_token(kontur_api)
    # Получение активных транспортных ящиков, в которых хранятся наши сообщения
    boxes = get_boxes(kontur_api)


def init_config():
    cfg = {}
    config = configparser.ConfigParser()
    try:
        config.read('api_config.ini')
    except config.error as e:
        print("ERROR: %s" % e)
        return False
    else:
        cfg = {'URL': config['DEFAULT']['url'],
               'LOGIN': config['DEFAULT']['login'],
               'PASSW': config['DEFAULT']['password'],
               'KEY': config['DEFAULT']['api_key'],
               }

        return cfg


#argv = sys.argv

#if len(argv) == 1:
    #raise SystemExit  # пробросим исключение о завершении работы скрипта

exchange()

