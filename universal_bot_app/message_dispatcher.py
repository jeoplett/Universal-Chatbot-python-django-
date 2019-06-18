# coding: utf8

import universal_bot_app.app_log
import importlib
import universal_bot_app.app_config
import universal_bot_app.message_analyzer
import universal_bot_app.bot_config
import sys

# Подготовка унифицированного сообщения по json-объекту
def createUnifiedMessageByRequest(json_object, bot_api_token):
    # Получение конфигурации бота текущего сообщения
    cur_bot_config = bot_config.getBotConfigByAPIToken(bot_api_token)
    try:
        bot_module = bot_config.getBotRuntimeByAPIToken(bot_api_token)
        unified_message = bot_module.createUnifiedMessage(json_object, bot_api_token, cur_bot_config)
        return unified_message
    except Exception as exc:
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog(u"*** Unable to create unified message from #" + bot_api_token + ": " + str(exc) + ", line " + str(tb.tb_lineno))
    return None
    
# Сборка и отправка сообщения для конкретного чата
def dispatchUnifiedMessage(unified_message):
    try:
        bot_module = bot_config.getBotRuntimeByAPIToken(unified_message['bot_api_token'])
        bot_module.dispatchUnifiedMessage(unified_message)
        return unified_message
    except Exception as exc:
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog(u"*** Unable to dispatch unified message to #" + unified_message['bot_api_token'] + ": " + str(exc) + ", line " + str(tb.tb_lineno))
    return None

# Создаем универсальный ответ на универсальное сообщение
def createUnifiedAnswer(unified_message):
    try:
        # Если бот неактивен, то не будем обрабатывать запросы
        if unified_message['bot_config']['state'] != "running":
            return None
        # Определение типа входящего сообщения
        unified_message_type = unified_message['request_type']
        # Входящее сообщение будет проанализировано только если бот принимает этот тип сообщений
        if unified_message['bot_config']['accept_' + unified_message_type + '_messages'] == 'yes':
            unified_message = message_analyzer.createUnifiedAnswer(unified_message)

        return unified_message        
    except Exception as exc:
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog(u"*** Unable to create unified answer to #" + unified_message['bot_api_token'] + ": " + str(exc) + ", line " + str(tb.tb_lineno))
    return None
