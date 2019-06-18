# coding: utf8

import universal_bot_app.bot_command
import universal_bot_app.app_log
import re
import copy
import universal_bot_app.app_config
from universal_bot_app.message_analyzer import getNewAnswerFunction
from universal_bot_app.message_analyzer import getLastAnswerFunction
import requests
import sys

# ФУНКЦИИ, СОЗДАЮЩИЕ КОНТЕНТ В ОТВЕТАХ ЧАТА

def answerEMPTY(unified_message):
    try:
        unified_message['response_text'] = unified_message['response_text']
    except Exception as exc:
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog(u"*** Exception caught on execution trigger function 'answerEMPTY': " + str(exc) + ", line " + str(tb.tb_lineno))
    return unified_message

    
def answerPUSH(unified_message):
    try:
        unified_message['response_text'] = unified_message['response_text']
    except Exception as exc:
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog(u"*** Exception caught on execution trigger function 'answerPUSH': " + str(exc) + ", line " + str(tb.tb_lineno))
    return unified_message


def answerUNKNOWN(unified_message):
    try:
        unified_message['response_text'] = unified_message['response_text']
    except Exception as exc:
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog(u"*** Exception caught on execution trigger function 'answerUNKNOWN': " + str(exc) + ", line " + str(tb.tb_lineno))
    return unified_message


def answerSIMILAR(unified_message):
    try:
        if unified_message['new_chat_trigger']['command'].lower() not in [bot_command.getBotUnknownCommand(unified_message).lower(), bot_command.getBotHelpCommand(unified_message).lower()]:
            template_message = unified_message['new_chat_record']['last_chat_message']
        else:
            template_message = unified_message['last_chat_record']['last_chat_message']
        # Поиск похожих команд
        bot_semantics = bot_command.getBotSemantics(unified_message)
        for re_xp in bot_semantics:
            if re.search(re_xp, template_message, re.UNICODE) != None:
                commands = bot_semantics[re_xp]
                for command in commands:
                    if command.lower() not in str(unified_message['response_commands']).lower():
                        unified_message['response_commands'] = unified_message['response_commands'] + [command]
        # Затем всегда добавляем команды начала и помощи
        if bot_command.getBotHelpCommand(unified_message).lower() not in str(unified_message['response_commands']).lower():
            unified_message['response_commands'] = unified_message['response_commands'] + [bot_command.getBotHelpCommand(unified_message)]
    except Exception as exc:
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog(u"*** Exception caught on execution trigger function 'answerSIMILAR': " + str(exc) + ", line " + str(tb.tb_lineno))
    return unified_message


def answerServiceList(unified_message):
    try:
        # Проверка авторизации: статус текущего процесса авторизации
        try:
            auth_data = unified_message['last_chat_record']['auth_data']
        except Exception as exc:
            auth_data = { 
                'stage' : '0', 
                'token' : '',
                'phone' : ''
            }
            unified_message['last_chat_record']['auth_data'] = auth_data
            unified_message['new_chat_record']['auth_data'] = auth_data

        # Проверка авторизации: статус авторизации на сервере
        try:
            request_data = {"request_type": "checkauth", "api_token": unified_message['bot_api_token'], "chat_id": unified_message['chat_id']}
            response = requests.get(app_config.getStatServiceURL(), params = request_data)
            app_log.appendLog(app_config.getStatServiceURL() + ' [AUTHCHECK] -> ' + response.text)
            response_text = (response.text + '#$#').split('#$#')[0]
            response_comment = (response.text + '#$#').split('#$#')[1]
            if response_text != "0" and len(response_text) == 1:
                auth_data.stage = response_text
            elif len(response_text) != 1:
                raise Exception("exception on server (" + response.text + ")")
        except Exception as exc:
            exc_type, exc_obj, tb = sys.exc_info()
            app_log.appendLog(u"*** Exception caught during authorization check: " + str(exc) + ", line " + str(tb.tb_lineno))

        # Отдельная проверка блокировки авторизации пользователя
        if auth_data['stage'] == '3':
            unified_message['response_text'] = [u"Ты пока не можешь пройти подтверждение, отправь нам запрос на apelsin@cetelem.ru."]
            unified_message['response_commands'] = [u"Начать заново"]
            return unified_message

        # Сообщение пользователю в зависиомсти от статуса авторизации
        if auth_data['stage'] == '0':
            unified_message['response_text'] = [u"Чтобы пользоваться функциями для сотрудников, сперва необходимо подтвердить номер твоего мобильного телефона. С этой целью используй меню ниже 'Подтвердить номер'."]
            unified_message['response_commands'] = [u"Подтвердить номер", u"Начать заново"]
        if auth_data['stage'] == '1':
            unified_message['response_text'] = [u"Чтобы пользоваться приложениями Банка, необходимо завершить процесс подтверждения номера твоего моибльного телефона. Ранее был выслан код подтверждения, если ты его получил, то перейди в меню 'Ввести код' и введи код подтверждения. Если код не был получен, то запроси новый код, используя меню 'Подтвердить номер'."]
            unified_message['response_commands'] = [u"Ввести код", u"Подтвердить номер", "Начать заново"]
        if auth_data['stage'] == '2':
            unified_message['response_text'] = [u"Чего желаешь, коллега? Выбери пункт ниже."]
            unified_message['response_commands'] = [u"Новые информационные письма", u"Начать заново"]
    except Exception as exc:
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog(u"*** Exception caught on execution trigger function 'answerServiceList': " + str(exc) + ", line " + str(tb.tb_lineno))

    return unified_message


def answerAuth(unified_message):
    try:
        # Проверка авторизации: статус текущего процесса авторизации
        try:
            auth_data = unified_message['last_chat_record']['auth_data']
        except Exception as exc:
            auth_data = { 
                'stage' : '0', 
                'token' : '',
                'phone' : ''
            }
            unified_message['last_chat_record']['auth_data'] = auth_data
            unified_message['new_chat_record']['auth_data'] = auth_data

        # Проверка авторизации: статус авторизации на сервере
        try:
            request_data = {"request_type": "checkauth", "api_token": unified_message['bot_api_token'], "chat_id": unified_message['chat_id']}
            response = requests.get(app_config.getStatServiceURL(), params = request_data)
            app_log.appendLog(app_config.getStatServiceURL() + ' [AUTHCHECK] -> ' + response.text)
            response_text = (response.text + '#$#').split('#$#')[0]
            response_comment = (response.text + '#$#').split('#$#')[1]
            if response_text != "0" and len(response_text) == 1:
                auth_data.stage = response_text
            elif len(response_text) != 1:
                raise Exception("exception on server (" + response.text + ")")
        except Exception as exc:
            exc_type, exc_obj, tb = sys.exc_info()
            app_log.appendLog(u"*** Exception caught during authorization check: " + str(exc) + ", line " + str(tb.tb_lineno))

        # Отдельная проверка блокировки авторизации пользователя
        if auth_data['stage'] == '3':
            unified_message['response_text'] = [u"Ты пока не можешь пройти подтверждение, отправь нам запрос на dist@cetelem.ru."]
            unified_message['response_commands'] = [u"Начать заново"]
            return unified_message

        # Поведение при других командах во время атворизации
        if unified_message['new_chat_record']['last_chat_message'].lower() in [u"для сотрудников", u"начать заново"]:
            unified_message['new_chat_record']['last_chat_command'] = unified_message['last_chat_record']['last_chat_message'].lower()
            unified_message['last_chat_record'] = copy.deepcopy(unified_message['new_chat_record'])
            unified_message['new_chat_trigger'] = bot_command.getBotTriggerByBotCommand(unified_message, unified_message['new_chat_record']['last_chat_command'])
            unified_message['new_chat_trigger']['repeatable_text'] = "true"
            unified_message['new_chat_trigger']['repeatable_next_commands'] = "true"
            unified_message['new_chat_trigger']['repeat_last_command_text'] = "false"
            unified_message['new_chat_trigger']['repeat_last_command_next_commands'] = "false"
            unified_message['last_chat_trigger'] = copy.deepcopy(unified_message['new_chat_trigger'])
            unified_message['response_text'] = unified_message['response_text'] + unified_message['new_chat_trigger']['answer_text']
            unified_message['response_commands'] = unified_message['new_chat_trigger']['next_commands']
            unified_message['last_answer_func'] = globals()['getNewAnswerFunction'](unified_message) 
            unified_message['new_answer_func'] = unified_message['last_answer_func']
            unified_message['new_answer_func'](unified_message)
            return unified_message

        # При подтверждении номера процесс был инициирован заново
        if auth_data['stage'] == '1' and unified_message['new_chat_record']['last_chat_message'].lower() == u"подтвердить номер":
            auth_data['stage'] = '0'

        # Авторизация была ранее пройдена
        if auth_data['stage'] == '2':
            unified_message['response_text'] = [u"Твой номер мобильного телефона уже подтвержден, тебе доступен раздел 'Для сотрудников' - ты можешь перейти в него, используя меню ниже."]
            unified_message['response_commands'] = [u"Для сотрудников", u"Начать заново"]
            return unified_message

        # ЭТАП 2: проверка кода, отправленного на номер мобильного телефона
        if auth_data['stage'] == '1' and unified_message['new_chat_record']['last_chat_message'].lower() != u"ввести код":
            # Проверка кода на сервере
            request_data = {"request_type": "auth", "auth_stage": auth_data['stage'], "pseries": "", "pnum": "", "api_token": unified_message['bot_api_token'], "chat_id": unified_message['chat_id'], "phone": auth_data['phone']}
            response = requests.get(app_config.getStatServiceURL(), params = request_data)
            app_log.appendLog(app_config.getStatServiceURL() + ' [AUTH:1] -> ' + response.text)
            response_text = (response.text + '#$#').split('#$#')[0]
            response_comment = (response.text + '#$#').split('#$#')[1]
            # Ответ пользователю по умолчанию
            unified_message['response_text'] = [u"Упс.. похоже что-то пошло не так. Попробуй повторить операцию позже."]
            unified_message['response_commands'] = [u"Начать заново"]
            # Анализируем ответ сервера
            if response_text == "2":
                unified_message['response_text'] = [u"Номер мобильного телефона подтвержден, поздравляем, теперь тебе доступен раздел 'Для сотрудников'."]
                unified_message['response_commands'] = [u"Для сотрудников", u"Начать заново"]
                auth_data['phone'] = unified_message['last_chat_record']['last_chat_message']
                auth_data['stage'] = '2'
            elif response_text == "-1":
                if 'wrong code' in response_comment:
                    unified_message['response_text'] = [u"Введенный код не соответствует отправленному. Проверь код, отправленный тебе в СМС, и введи его еще раз."]
                    unified_message['response_commands'] = [u"отмена"]
                if 'no operation compleated' in response_comment:
                    auth_data['stage'] = '0'
                    unified_message['response_text'] = [u"Упс.. похоже что-то пошло не так. Попробуй сбросить историю чата и повторить операцию."]
                    unified_message['response_commands'] = [u"Начать заново"]
                if 'request new code' in response_comment:
                    auth_data['stage'] = '0'
                    unified_message['response_text'] = [u"Ну вот.. код был введен неверно несколько раз. А так все хорошо начиналось. Придется снова проверить номер через меню 'Проверить номер'. "]
                    unified_message['response_commands'] = [u"Проверить номер", u"Отмена"]
                if 'user blocked' in response_comment:
                    auth_data['stage'] = '0'
                    unified_message['response_text'] = [u"Слушай, явно что-то не так. Напиши нам письмо на apelsin@cetelem.ru - мы будем разбираться, почему ты не можешь пройти проверку номера."]
                    unified_message['response_commands'] = [u"Начать заново"]

        # ЭТАП 1: запрос ранее отправленного кода (в случае, если ранее на этапе ввода кода было выбрано действие "Отмена")
        if auth_data['stage'] == '1' and unified_message['new_chat_record']['last_chat_message'].lower() == u"ввести код":
            unified_message['response_text'] = [u"Введи код подтверждения, полученный в СМС."]
            unified_message['response_commands'] = [u"Отмена"]

        # ЭТАП 1: отправка кода на введенный номер мобильного телефона и запрос кода
        if auth_data['stage'] == '0' and unified_message['new_chat_record']['last_chat_message'].lower() != u"подтвердить номер" and unified_message['new_chat_record']['last_chat_message'].lower() != '':
            # Проверка номера на сервере
            request_data = {"request_type": "auth", "auth_stage": auth_data['stage'], "pseries": "", "pnum": "", "api_token": unified_message['bot_api_token'], "chat_id": unified_message['chat_id'], "phone": unified_message['new_chat_record']['last_chat_message'].lower()}
            response = requests.get(app_config.getStatServiceURL(), params = request_data)
            app_log.appendLog(app_config.getStatServiceURL() + ' [AUTH:0] -> ' + response.text)
            response_text = (response.text + '#$#').split('#$#')[0]
            response_comment = (response.text + '#$#').split('#$#')[1]
            # Ответ пользователю по умолчанию
            unified_message['response_text'] = [u"Упс.. похоже что-то пошло не так. Попробуй повторить операцию позже."]
            unified_message['response_commands'] = [u"Начать заново"]
            # Анализируем ответ сервера
            if response_text == "1":
                auth_data['stage'] = response_text
                auth_data['phone'] = unified_message['new_chat_record']['last_chat_message'].lower()
                unified_message['response_text'] = [u"Ура! Я вижу, что ты у нас работаешь. На твой номер мобильного телефона был отправлен код подтверждения, дождись его получения и отправь ответом на это сообщение."]
                unified_message['response_commands'] = [u"Отмена"]
            elif response_text == "0":
                auth_data['stage'] = '0'
                unified_message['response_text'] = [u"Ой.. похоже, твой номер мобильного телефона не принадлежит ни одному сотруднику Банка. Если ты ошибся при вводе номера, то введи его еще раз. Если ты верно ввел номер и работаешь в Банке, то жми 'Отмена' и передай номер своего мобильного телефона кадровому администратору. После того, как телефон будет внесен в систему Банка, ты сможешь пройти проверку."]
                unified_message['response_commands'] = [u"Отмена"]
            elif response_text == "-1":
                if 'no operation compleated' in response_comment:
                    auth_data['stage'] = '0'
                    unified_message['response_text'] = [u"Упс.. похоже что-то пошло не так. Попробуй сбросить историю чата и повторить операцию."]
                    unified_message['response_commands'] = [u"Начать заново"]
                if 'request new code' in response_comment:
                    auth_data['stage'] = '0'
                    unified_message['response_text'] = [u"Ну вот.. код был введен неверно несколько раз. А так все хорошо начиналось. Придется снова проверить номер через меню 'Проверить номер'. "]
                    unified_message['response_commands'] = [u"Проверить номер", u"Отмена"]
                if 'user blocked' in response_comment:
                    auth_data['stage'] = '0'
                    unified_message['response_text'] = [u"Слушай, явно что-то не так. Напиши нам письмо на apelsin@cetelem.ru - мы будем разбираться, почему ты не можешь пройти проверку номера."]
                    unified_message['response_commands'] = [u"Начать заново"]

        # ЭТАП 0: ввод номера мобильного телефона
        if auth_data['stage'] == '0' and unified_message['new_chat_record']['last_chat_message'].lower() == u"подтвердить номер":
            #unified_message['response_text'] = [u"Введи серию-номер своего паспорта и через пробел номер мобильного телефона, который ты указывал при трудоустройстве (он должен совпадать с тем, которым ты пользуешься сейчас). Если ты сменил номер мобильного телефона, то сообщи об этом своему руководителю, чтобы он передал твой новый номер кадровому администратору. На следующий день после того, как кадровый администратор изменит твой номер в системе Банка, можно будет снова попробовать подтвердить его здесь."]
            unified_message['response_text'] = [u"Введи номер мобильного телефона, который ты указывал при трудоустройстве (он должен совпадать с тем, которым ты пользуешься сейчас). Если ты сменил номер мобильного телефона, то сообщи об этом своему руководителю, чтобы он передал твой новый номер кадровому администратору. На следующий день после того, как кадровый администратор изменит твой номер в системе Банка, можно будет снова попробовать подтвердить его здесь."]
            unified_message['response_commands'] = [u"Отмена"]

        unified_message['last_chat_record']['auth_data'] = auth_data
        unified_message['new_chat_record']['auth_data'] = auth_data
    except Exception as exc:
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog(u"*** Exception caught on execution trigger function 'answerAuth': " + str(exc) + ", line " + str(tb.tb_lineno))

    return unified_message

def answerService110(unified_message):
    try:
        auth_data = { 
            'stage' : '0', 
            'token' : '',
            'phone' : ''
        }
        unified_message['last_chat_record']['auth_data'] = auth_data
        unified_message['new_chat_record']['auth_data'] = auth_data
    except Exception as exc:
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog(u"*** Exception caught on execution trigger function 'answerService110': " + str(exc) + ", line " + str(tb.tb_lineno))

    return unified_message