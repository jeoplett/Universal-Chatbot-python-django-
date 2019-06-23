# coding: utf8 

from viberbot import Api
from . import app_log
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import (
    TextMessage,
    ContactMessage,
    PictureMessage,
    VideoMessage,
    RichMediaMessage
)
from viberbot.api.messages.data_types.contact import Contact
import copy
import sys

# КОНСТАНТЫ КОННЕКТОРА

__MESSENGER_TYPE__ = "viber"

__BOT_API_RUNTIME__ = {}

__DEFAULT_TEXT_MESSAGE_LENGTH__ = 1024

__KEYBOARD_TEMPLATE__ = {
    "DefaultHeight": True,
    "BgColor": "#FFFFFF",
    "Type": "keyboard",
    "Buttons": []
}

__KEYBOARD_BUTTON_TEMPLATE__ = {
    "Columns": 6,
    "Row": 1,
    "BgColor": "#2db9b9",
    "ActionType": "reply",
    "ActionBody": u"Помощь",
    "Text": u"Помощь",
    "TextVAlign": "middle",
    "TextHAlign": "center",
    "TextOpacity": 60,
    "TextSize": "regular"
}


# ФУНКЦИИ КОННЕКТОРА

# Возвращает API бота
def getCurBotAPIRuntime(bot_config):
    global __BOT_API_RUNTIME__
    if __BOT_API_RUNTIME__.get(bot_config['api_token']) == None:
        # Создаем экземпляр API для бота
        bot_configuration = BotConfiguration (
            name = bot_config['name'],
            avatar = '',
            auth_token = bot_config['api_token']
        )
        # Создание API для запуска бота
        __BOT_API_RUNTIME__[bot_config['api_token']] = Api(bot_configuration) 
    return __BOT_API_RUNTIME__[bot_config['api_token']]

# Запускает бот (вешает хук)
def runBot(bot_config):
    try:
        if bot_config['type'] == __MESSENGER_TYPE__ and bot_config['start'] == "yes":
            bot = getCurBotAPIRuntime(bot_config)
            # Установка веб-хука на обработчик бота
            bot.set_webhook(bot_config['web_hook_url'])
    except Exception as exc:
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog(u"*** Exception caught during runBot: " + str(exc) + ", line " + str(tb.tb_lineno))

# Создает унифицированное сообщение по сообщениям, пришедшим от ботов данного типа
def createUnifiedMessage(json_object, bot_api_token, cur_bot_config):
    if __MESSENGER_TYPE__ != cur_bot_config['type']:
        return None
    # Тип мессенджера
    messenger_type = cur_bot_config['type']
    # Тип сообщения
    message_type = getBotMessageType(json_object, bot_api_token, cur_bot_config)

    # Обработка текстового сообщения
    if message_type == "text":
        # Длина текстового сообщения
        module_text_message_length = getModuleParam(json_object, bot_api_token, cur_bot_config, 'text_message_length')
        # Идентификатор чата
        chat_id = ""
        try:
            chat_id = json_object['sender']['id']
        except Exception:
            pass
        try:
            chat_id = json_object['user']['id']
        except Exception:
            pass
        # Сообщение, пришедшее из чата
        try:
            new_chat_message = json_object['message']['text'] 
            new_chat_message = new_chat_message.lower()
            new_chat_message = new_chat_message[0:module_text_message_length]
        except Exception:
            # Если что-то пошло совсем не так, то считаем, что пришла команда неизвестности
            new_chat_message = "/unknown"
        # Фамилия отправителя
        try:
            last_name = json_object['sender']['last_name']
        except Exception:
            last_name = "_empty_"
        # Имя отправителя
        try:
            first_name = json_object['sender']['name']
        except Exception:
            first_name = "_empty_"
        # Создание унифицированного ТЕКСТОВОГО сообщения
        unified_message = {
            'messenger_type': messenger_type,
            'event_id': '',
            'event_message': '',
            'request_type': message_type, # text, event, sound, picture, video, mixed
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

    # Обработка события
    if message_type == "event":
        # Длина текстового сообщения
        module_text_message_length = getModuleParam(json_object, bot_api_token, cur_bot_config, 'text_message_length')
        # Идентификатор чата
        chat_id = ""
        try:
            chat_id = json_object['sender']['id']
        except Exception:
            pass
        try:
            chat_id = json_object['user']['id']
        except Exception:
            pass
        # Если идентификатор чата пуст, то, вероятно, пришло 
        # событие от пользователя, например, conversation_started,
        # в этом случае в качестве текста универсального сообщения
        # используется название события
        event_id = ""
        try:
            event_id = json_object['event']
        except Exception:
            pass
        # Сообщение, пришедшее из чата
        try:
            new_chat_message = json_object['message']['text'] 
            new_chat_message = new_chat_message.lower()
            new_chat_message = new_chat_message[0:module_text_message_length]
        except Exception:
            new_chat_message = ""
        # Фамилия отправителя
        try:
            last_name = json_object['sender']['last_name']
        except Exception:
            last_name = "_empty_"
        # Имя отправителя
        try:
            first_name = json_object['sender']['name']
        except Exception:
            first_name = "_empty_"
        # Создание унифицированного СОБЫТИЙНОГО сообщения
        unified_message = {
            'messenger_type': messenger_type,
            'event_id': event_id,
            'event_message': new_chat_message,
            'request_type': message_type, # text, event, sound, picture, video, mixed
            'request_text': ['/event'],
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

	# Если есть адресат, то осмысленно отвечаем ему
        if unified_message['chat_id'] != "":
            # Инициализация клавиатуры
            response_keyboard = copy.deepcopy(__KEYBOARD_TEMPLATE__)

            # Подготовка текстового сообщения
            response_text = ""
            response_command_text = ""
            for text in unified_message['response_text']:
                response_text = response_text + u'\r\n' + text

            # Подготовка комманд (кнопок)
            for response_command in unified_message['response_commands']:
                if response_command.lower() not in response_command_text.lower():
                    response_keyboard_button = copy.deepcopy(__KEYBOARD_BUTTON_TEMPLATE__)
                    response_keyboard_button['Text'] = response_command
                    response_keyboard_button['ActionBody'] = response_command
                    response_keyboard['Buttons'] = response_keyboard['Buttons'] + [response_keyboard_button]
                response_command_text = response_command_text + response_command

            # Отправка сообщения боту
            if len(response_keyboard['Buttons']) > 0:
                bot.send_messages(unified_message['chat_id'], 
                    [TextMessage(text = response_text, keyboard = response_keyboard)]
                )
            else:
                bot.send_messages(unified_message['chat_id'], 
                    [TextMessage(text = response_text)]
                )

	# Если прищло нечто без адресата (скорее всего событие), то ответим только статусом 200 ОК
        if unified_message['chat_id'] == "":
            return unified_message

    except Exception as exc: 
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog(u"*** Exception caught during message dispatch: " + str(exc) + ", line " + str(tb.tb_lineno))
        bot.send_messages(unified_message['chat_id'], [
            TextMessage(text = "Ууууп-с.. похоже что-то пошло не так.. дай-ка мне немного времени, я смогу ответить на твои вопросы позже.")
        ])

    return unified_message

# Распознает тип сообщения, пришедшего от данного типа ботов
def getBotMessageType(json_object, bot_api_token, cur_bot_config):
    # Если это сообщение не для вайбера, не будем его обрабатывать
    if __MESSENGER_TYPE__ != cur_bot_config['type']:
        return None

    # Текстовое сообщение
    try:
        json_object['message']['text']
        return "text"
    except Exception as exc:
        pass

    # Событие
    try:
        json_object['event']
        return "event"
    except Exception as exc:
        pass

    # По умолчанию - событие
    return "event"

# Возвращает параметр конфигурации бота
def getModuleParam(json_object, bot_api_token, cur_bot_config, module_param_name):
    try:
        return int(str(cur_bot_config['module_config'][module_param_name]))
    except Exception:
        return __DEFAULT_TEXT_MESSAGE_LENGTH__
