# coding: utf8 

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import settings
import sys

from . import app_log
from . import message_dispatcher
from . import app_config
from . import app_statistic

import universal_bot_app.bot_config

@csrf_exempt
def restart(self):
    app_log.appendLog('Restarting bots..')
    bot_config.runBotsFromConfig()
    return JsonResponse({}, status=200)

@csrf_exempt
def index(self, bot_api_token):

    # Получение JSON запроса от мессенджера
    try:
        # Преобразование запроса в объект
        json_object = json.loads(self.body.decode('utf8'))
        # Лог входящего запроса
        app_log.appendLog('<- [stage 1] ' + str(json_object))
    except Exception as exc:
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog(u"*** Exception caught during query analysis: " + str(exc) + ", line " + str(tb.tb_lineno))
        # В случае некорректного запроса все равно отправляем статус его получения
        return JsonResponse({}, status=200)
    else:
        # Унификация сообщения, его анализ и сборка ответа
        try:
            # Унификация сообщения от мессенджера
            unified_message = message_dispatcher.createUnifiedMessageByRequest(json_object, bot_api_token)
            app_log.appendLog('<- [stage 2] ' + unified_message['bot_config']['name'] + ' (' + unified_message['bot_config']['api_token'] + '): ' + str(unified_message['request_text']))
            # Если удалось создать унифицированное сообщение, то анализируем сообщение, независимо от мессенджера 
            if unified_message != None:
                unified_message = message_dispatcher.createUnifiedAnswer(unified_message)
                app_log.appendLog('<- [stage 3] ' + unified_message['bot_config']['name'] + ' (' + unified_message['bot_config']['api_token'] + '): \r\nresponse_text: ' + str(unified_message['response_text']) + u'\r\nresponse_commands: ' + str(unified_message['response_commands']))
                # Если удалось провести анализ сообщения, то соберем ответ на него, персонифицированный для мессенджера
                if unified_message != None:
                    unified_message = message_dispatcher.dispatchUnifiedMessage(unified_message)
                    app_log.appendLog('<- [stage 4] ' + unified_message['bot_config']['name'] + ' (' + unified_message['bot_config']['api_token'] + '): DISPATCHED.')
        except Exception as exc:
            exc_type, exc_obj, tb = sys.exc_info()
            app_log.appendLog("*** Exception caught during unified message analysis: " + str(exc) + ', line ' + str(tb.tb_lineno))

    # Отправка ответа мессенджеру: в любом случае отвечаем, что все ок, чтобы не спамил
    return JsonResponse({}, status=200)