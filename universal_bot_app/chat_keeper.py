# coding: utf8

import cPickle  
import copy
from . import bot_config


# ФУНКЦИИ МОДУЛЯ

# Конструктор
def initChatsKeeper():
    global __HISTORY_DICTOBJECT
    all_bot_api_tokens = bot_config.getAllBotAPITokens()
    for bot_api_token in all_bot_api_tokens:
        cur_bot_config = bot_config.getBotConfigByAPIToken(bot_api_token)
        file_fullname = getRecordsFullFileName(cur_bot_config)
        try:
            file = open(file_fullname, "rb")
            __HISTORY_DICTOBJECT[cur_bot_config['name']] = cPickle.load(file)
            file.close()
        except Exception:
            # Если ошибка открытия файла, то попытаемся его создать с пустым словарем
            file = open(file_fullname, "wb")
            cPickle.dump(__HISTORY_EMPTYRECORD, file)
            file.close()
            # После создания загружаем пустой словарь
            file = open(file_fullname, "rb")
            __HISTORY_DICTOBJECT[cur_bot_config['name']] = cPickle.load(file)
            file.close()

# Замена крайнего состояния чата
def editLastChatRecord(unified_message):
    chat_id = unified_message['chat_id']
    new_chat_record = unified_message['new_chat_record']
    __HISTORY_DICTOBJECT[unified_message['bot_config']['name']][str(chat_id)] = copy.deepcopy(__HISTORY_EMPTYRECORD)
    for key in new_chat_record:
        __HISTORY_DICTOBJECT[unified_message['bot_config']['name']][str(chat_id)][key] = copy.deepcopy(new_chat_record[key])
    # Сохраняем состояния всех чатов при изменении состояния любого из них
    saveLastChatsRecords(unified_message)
    return unified_message

# Возврат крайнего состояния чата
def getLastChatRecord(unified_message):
    try:
        file_fullname = getRecordsFullFileName(unified_message['bot_config'])
        file = open(file_fullname, "rb")
        __HISTORY_DICTOBJECT[unified_message['bot_config']['name']] = cPickle.load(file)
        file.close()
    except Exception:
        chat_id = unified_message['chat_id']

    chat_id = unified_message['chat_id']
    try:
        last_chat_record = copy.deepcopy(__HISTORY_EMPTYRECORD)
        # Заполнить пустотой отсутствующие обязательные блоки
        for key in __HISTORY_DICTOBJECT[unified_message['bot_config']['name']][str(chat_id)]:
            last_chat_record[key] = copy.deepcopy(__HISTORY_DICTOBJECT[unified_message['bot_config']['name']][str(chat_id)][key])
        unified_message['last_chat_record'] = last_chat_record
    except Exception:
        unified_message['last_chat_record'] = __HISTORY_EMPTYRECORD
    return unified_message
    
# Обнуление крайнего состояния чата
def emptyLastChatRecord(unified_message):
    chat_id = unified_message['chat_id']
    __HISTORY_DICTOBJECT[unified_message['bot_config']['name']][str(chat_id)] = copy.deepcopy(__HISTORY_EMPTYRECORD)
    unified_message['last_chat_record'] = copy.deepcopy(__HISTORY_EMPTYRECORD)
    # Сохраняем состояния всех чатов при изменении состояния любого из них
    saveLastChatsRecords(unified_message)
    return unified_message
    
# Сохранение состояний всех активных чатов
def saveLastChatsRecords(unified_message):
    try:
        file_fullname = getRecordsFullFileName(unified_message['bot_config'])
        file = open(file_fullname, "wb")
        cPickle.dump(__HISTORY_DICTOBJECT[unified_message['bot_config']['name']], file)
        file.close()
    except Exception:
        return ""

def getRecordsFullFileName(bot_config):
    file_fullname = './' + bot_config['name'] + __HISTORY_FILENAME_ENDING
    return file_fullname
    
# ИНИЦИАЛИЗАЦИЯ МОДУЛЯ

# "Скрытые" переменные
__HISTORY_DICTOBJECT = {}
__HISTORY_EMPTYRECORD = {"last_chat_state": "", "last_chat_message": "", "last_chat_command": ""}
__HISTORY_FILENAME_ENDING = '_bot_history.dmp'

# Вызов конструктора
initChatsKeeper()