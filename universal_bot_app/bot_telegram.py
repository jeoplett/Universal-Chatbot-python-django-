# coding: utf8 

import telebot
import app_log
import sys

__MESSENGER_TYPE__ = "telegram"
__DEFAULT_TEXT_MESSAGE_LENGTH__ = 1024
__BOT_API_RUNTIME__ = {}

# Возвращает API бота
def getCurBotAPIRuntime(bot_config):
    global __BOT_API_RUNTIME__
    if __BOT_API_RUNTIME__.get(bot_config['api_token']) == None:
        __BOT_API_RUNTIME__[bot_config['api_token']] = telebot.TeleBot(bot_config['api_token'])
    return __BOT_API_RUNTIME__[bot_config['api_token']]
    
# Стартует боты данного типа, создавая их привязку к url обработчиков
def runBot(bot_config):
    if __MESSENGER_TYPE__ != bot_config['type']:
        return None
    if bot_config['start'] == "yes":
        # Создаем экземпляр API для бота
        bot = getCurBotAPIRuntime(bot_config)

        # Устанавливаем webhook
        if bot_config['web_hook_url'] != bot.get_webhook_info().url:
            print 'Hooking bot "' + bot_config['name'] + '": ' + bot_config['api_token']
            if bot_config['web_hook_ssl_sert'] != "":
                bot.set_webhook(url = bot_config['web_hook_url'], certificate = open(bot_config['web_hook_ssl_sert'], 'r'))
            else:
                bot.set_webhook(url = bot_config['web_hook_url'])

# Создает унифицированное сообщение по сообщениям, пришедшим от ботов данного типа
def createUnifiedMessage(json_object, bot_api_token, cur_bot_config):
    if __MESSENGER_TYPE__ != cur_bot_config['type']:
        return None
    # Тип мессенджера
    messenger_type = cur_bot_config['type']
    # Тип сообщения
    message_type = getBotMessageType(json_object, bot_api_token, cur_bot_config)
    # Конфигурация приложения
    if message_type == "text":
        # Длина текстового сообщения
        module_text_message_length = getModuleParam(json_object, bot_api_token, cur_bot_config, 'text_message_length')
        # Идентификатор чата
        chat_id = json_object['message']['chat']['id']
        # Сообщение, пришедшее из чата
        try:
            new_chat_message = json_object['message']['text'] 
            new_chat_message = new_chat_message.lower()
            new_chat_message = new_chat_message[0:module_text_message_length]
        except Exception:
            # Если что-то пошло совсем не так, то считаем, что пришла команда неизвестности
            json_object['message']['text'] = "/UNKNOWN" 
            new_chat_message = json_object['message']['text']
        # Фамилия отправителя
        try:
            last_name = json_object['message']['chat']['last_name']
        except Exception:
            last_name = "_empty_"
        # Имя отправителя
        try:
            first_name = json_object['message']['chat']['first_name']
        except Exception:
            first_name = "_empty_"
        # Создание унифицированного ТЕКСТОВОГО сообщения
        unified_message = {
            'messenger_type': messenger_type,
            'request_type': message_type, # text, sound, picture, video, mixed
            'request_text': [new_chat_message],
            'request_sound': [],
            'request_picture': [],
            'request_video': [],
            'request_json': json_object,
            'chat_id': chat_id,
            'response_text': [],
            'response_commands': [],
            'response_sound': [],
            'response_picture': [],
            'response_video': [],
            'response_markup': {},
            'response_json' : None,
            'first_name': first_name,
            'last_name': last_name,
            'bot_api_token': bot_api_token,
            'bot_config' : cur_bot_config
        }
        return unified_message
    return None

# По унифицированному сообщению создает сообщение специфичное для данного типа ботов
def dispatchUnifiedMessage(unified_message):
    if __MESSENGER_TYPE__ != unified_message['bot_config']['type']:
        return None
    try:
        bot = getCurBotAPIRuntime(unified_message['bot_config'])
        response_markup = telebot.types.ReplyKeyboardMarkup(row_width = unified_message['response_markup']['row_width'], one_time_keyboard = unified_message['response_markup']['one_time_keyboard'])
        response_text = ""
        response_command_text = ""
        for text in unified_message['response_text']:
            response_text = response_text + u'\r\n' + text
        for response_command in unified_message['response_commands']:
            if response_command.lower() not in response_command_text.lower(): 
                markup_button = telebot.types.KeyboardButton(response_command)
                response_markup.add(markup_button)
            response_command_text = response_command_text + response_command
        # Отправка сообщения боту 
        bot.send_message(unified_message['chat_id'], response_text, reply_markup = response_markup)
    except Exception as exc: 
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog("*** Exception caught during message dispatch: " + str(exc) + ', line ' + str(tb.tb_lineno))
        bot.send_message(unified_message['chat_id'], "Ууууп-с.. похоже что-то пошло не так.. дай-ка мне немного времени, я смогу ответить на твои вопросы позже.")
    return unified_message

# Распознает тип сообщения, пришедшего от данного типа ботов
def getBotMessageType(json_object, bot_api_token, cur_bot_config):
    if __MESSENGER_TYPE__ != cur_bot_config['type']:
        return None
    return "text"

# Возвращает параметр конфигурации модуля бота
def getModuleParam(json_object, bot_api_token, cur_bot_config, module_param_name):
    try:
        return int(str(cur_bot_config['module_config'][module_param_name]))
    except Exception as exc:
        if module_param_name == "text_message_length":
            return __DEFAULT_TEXT_MESSAGE_LENGTH__
        return None
