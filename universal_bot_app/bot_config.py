# coding: utf8 

import universal_bot_app.models
import universal_bot_app.app_config
import universal_bot_app.app_log
import importlib
import sys

__BOT_RUNTIME__ = {}

# Возвращает список API токенов всех доступных ботов
def getAllBotAPITokens():
    return models.getAllBotAPITokens()

# Возвращает конфиг конкретного бота
def getBotConfigByAPIToken(bot_api_token):
    cur_bot_config = models.getBotConfigByAPIToken(bot_api_token)
    cur_bot_config['app_config'] = app_config.getAppConfig()
    return cur_bot_config

# Запускает все боты из конфигурации    
def runBotsFromConfig():
    all_bot_api_tokens = getAllBotAPITokens()
    for bot_api_token in all_bot_api_tokens:
        try:
            cur_bot_config = getBotConfigByAPIToken(bot_api_token)
            app_log.appendLog("Initializing bot #" + bot_api_token + " with the following configuration: " + str(cur_bot_config))
            bot_module = __getBotRuntime(bot_api_token)
            bot_module.runBot(cur_bot_config)
        except Exception as exc:
            exc_type, exc_obj, tb = sys.exc_info()
            app_log.appendLog(u"*** Bot initialization error (#" + str(bot_api_token) + '): ' + str(exc) + ', line ' + str(tb.tb_lineno))

# Системная функция на уровне модуля - вызывается только из него, снаружи ее вызывать не надо
def __getBotRuntime(bot_api_token):
    global __BOT_RUNTIME__
    cur_bot_config = getBotConfigByAPIToken(bot_api_token)
    bot_module = __BOT_RUNTIME__.get(bot_api_token)
    if bot_module == None:
        bot_module = importlib.import_module('universal_bot_app.'  + cur_bot_config['module'])
        __BOT_RUNTIME__[bot_api_token] = bot_module
    return bot_module

# Возвращает загруженный ранее API бота
def getBotRuntimeByAPIToken(bot_api_token):
    global __BOT_RUNTIME__
    return __BOT_RUNTIME__.get(bot_api_token)
