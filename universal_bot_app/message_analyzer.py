# coding: utf-8

import re
import copy
import app_statistic
import app_log
import chat_keeper
import random
import bot_command
import sys

def createUnifiedAnswerToText(unified_message):
    try:
        # Ответим по очереди на каждое сообщение
        for cur_text_message in unified_message['request_text']:
            unified_message['cur_text_message'] = cur_text_message.lower()
            
            # Получение крайней записи истории чата
            if unified_message['cur_text_message'] == bot_command.getBotStartCommand(unified_message):
                unified_message = chat_keeper.emptyLastChatRecord(unified_message)
            else:
                unified_message = chat_keeper.getLastChatRecord(unified_message)
        
            # Установка значений для начала чата
            if unified_message['last_chat_record']["last_chat_command"] == "":
                unified_message['last_chat_record']["last_chat_command"] = "/start"
                unified_message['last_chat_record']["last_chat_message"] = "/start"
        
            # Выясняем предыдущие тригер и функцию ответа
            # app_log.appendLog(str(unified_message['last_chat_record']))
            unified_message['last_chat_trigger'] = bot_command.getBotTriggerByBotCommand(unified_message, unified_message['last_chat_record']['last_chat_command'].lower())
            unified_message['last_answer_func'] = globals()[unified_message['last_chat_trigger']['answer_func']]
        
            # Формируем новую крайнюю запись истории чата - изначально она похожа на старую во всем, кроме сообщения из чата
            unified_message['new_chat_record'] = copy.deepcopy(unified_message['last_chat_record'])
            unified_message['new_chat_record']['last_chat_message'] = unified_message['cur_text_message']
            unified_message['new_chat_trigger'] = copy.deepcopy(unified_message['last_chat_trigger'])

            # Проводим анализ нового сообщения из чата только в случае, если это диалог, а не заполнение ответа
            if unified_message['last_chat_trigger']['type'] == "info":
                # Определение новой команды по сообщению из чата
                unified_message['new_chat_trigger'] = bot_command.getBotTriggerByBotCommand(unified_message, unified_message['cur_text_message'])
                if unified_message['new_chat_trigger']:
                    # Если команда НАЙДЕНА, то получаем функцию, отправляющую ответ
                    unified_message['new_answer_func'] = globals()[unified_message['new_chat_trigger']['answer_func']]
                else:
                    # Если команда НЕ найдена, то анализируем текст сообщения и получаем функцию, отправляющую ответ
                    unified_message = analyzeRequestMessage(unified_message)

                # Устанавливаем новую команду в записи чата
                unified_message['new_chat_record']['last_chat_command'] = unified_message['new_chat_trigger']['command']
                
            # Сохраняем неизвестное нам сообщение для последующего анализа
            if unified_message['new_chat_trigger']['command'].lower() in [bot_command.getBotSimilarityCommand(unified_message).lower(), bot_command.getBotUnknownCommand(unified_message).lower()]:
                app_statistic.pushUnknownResponse(unified_message)
            elif unified_message['last_chat_trigger']['type'] == "info":
                app_statistic.pushInfo(unified_message)
        
            # В случае заполнения формы необходимо сохранить информацию
            if unified_message['last_chat_trigger']['type'] == "push":
                app_statistic.pushForm(unified_message)

            # Создаем ответ на сообщение
            unified_message = createResponseMesssage(unified_message)

            # Создаем контекст ответа, вызываем функцию ответа и отвечаем: чаще всего просто повторяем предыдущий ответ для диалога, 
            # при заполнении формы контекст не создается (предыдущий ответ не повторяется)
            if (unified_message['new_chat_trigger']['repeat_last_command_text'] == "true" or unified_message['new_chat_trigger']['repeat_last_command_next_commands'] == "true") and (unified_message['last_chat_trigger']['repeatable_text'] == "true" or unified_message['last_chat_trigger']['repeatable_next_commands'] == "true"):
                unified_message = createResponseMesssageContext(unified_message)

            # Сохранение крайнего сообщения и состояния чата
            if unified_message['new_chat_trigger']['command'].lower() not in [bot_command.getBotUnknownCommand(unified_message).lower(), bot_command.getBotHelpCommand(unified_message).lower()]:
                chat_keeper.editLastChatRecord(unified_message)
    except Exception as exc:
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog("*** Exception caught during unified message analysis: " + str(exc) + ', line ' + str(tb.tb_lineno))
    # Возвращаем кумулятивный ответ на все текстовые сообщения
    return unified_message


def createUnifiedAnswerToPicture(unified_message):
    return unified_message


def createUnifiedAnswerToSound(unified_message):
    return unified_message


def createUnifiedAnswerToVideo(unified_message):
    return unified_message


def createUnifiedAnswer(unified_message):
    # Вызываем свой обработчик для каждого типа контента, содержащегося во входящем сообщении
    try:
        if len(unified_message['request_text']) >= 1:
            unified_message = createUnifiedAnswerToText(unified_message)
        if len(unified_message['request_picture']) >= 1:
            unified_message = createUnifiedAnswerToPicture(unified_message)
        if len(unified_message['request_sound']) >= 1:
            unified_message = createUnifiedAnswerToSound(unified_message)
        if len(unified_message['request_video']) >= 1:
            unified_message = createUnifiedAnswerToVideo(unified_message)
    except Exception as exc:
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog("*** Exception caught during unified answer creation: " + str(exc) + ', line ' + str(tb.tb_lineno))
    # Возвращаем кумулятивный ответ на все содержащиеся во входящем сообщении типы контента сразу
    return unified_message 


def analyzeRequestMessage(unified_message):
    try:
        # Поищем совпадения в BOT_SEMANTICS
        count = 0
        bot_semantics = bot_command.getBotSemantics(unified_message)
        for re_xp in bot_semantics:
            if re.search(re_xp, unified_message['new_chat_record']['last_chat_message'], re.UNICODE) != None:
                commands = bot_semantics[re_xp]
                for command in commands:
                    count = count + 1
        if count == 1:
            # Если находим ТОЛЬКО ОДНО совпадение в семантике, то возвращаем тригер, соответствующий этому единственному совпадению
            new_chat_trigger = bot_command.getBotTriggerByBotCommand(unified_message, command.lower())
        elif count > 1:
            # Если находим БОЛЬШЕ ОДНОГО совпадения в семантике, то возвращаем тригер похожести
            new_chat_trigger = bot_command.getBotTriggerByBotCommand(unified_message, bot_command.getBotSimilarityCommand(unified_message))
        else:
            # Если в семантике ни одного совпадения нет, то возвращаем тригер неизвестности
            new_chat_trigger = bot_command.getBotTriggerByBotCommand(unified_message, bot_command.getBotUnknownCommand(unified_message))
        unified_message['new_chat_trigger'] = new_chat_trigger
        unified_message['new_chat_record']['last_chat_command'] = unified_message['new_chat_trigger']['command']
        unified_message['new_answer_func'] = globals()[unified_message['new_chat_trigger']['answer_func']]
    except Exception as exc:
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog("*** Exception caught during message analysis: " + str(exc) + ", line " + str(tb.tb_lineno))
    return unified_message

def createResponseMesssageContext(unified_message):
    try:
        if unified_message['last_chat_trigger']['repeatable_next_commands'] == "true" or unified_message['last_chat_trigger']['repeatable_text'] == "true":
            # Для info команд выберем случайный допустимый ответ и загрузим все следующие команды
            if unified_message['new_chat_trigger']['type'] == "info" or unified_message['new_chat_trigger']['type'] == "transit":
                try:
                    if unified_message['new_chat_trigger']['repeat_last_command_text'] == "true" and unified_message['last_chat_trigger']['repeatable_text'] == "true":
                        # Если одно текстовое сообщение, то выберем его, если их несколько, то выберем случайное
                        if len(unified_message['last_chat_trigger']['answer_text']) > 1:
                            answer_text = unified_message['last_chat_trigger']['answer_text'][random.randint(1, len(unified_message['last_chat_trigger']['answer_text'])) - 1]
                        elif len(unified_message['last_chat_trigger']['answer_text']) == 1:
                            answer_text = unified_message['last_chat_trigger']['answer_text'][0]
                        else:
                            answer_text = ""
                        if answer_text != "" and answer_text.lower() not in str(unified_message['response_text']).lower():
                            unified_message['response_text'] = unified_message['response_text'] + [answer_text]
                except Exception as exc:
                    exc_type, exc_obj, tb = sys.exc_info()
                    app_log.appendLog("*** Exception caught during context creation: " + str(exc) + ', line ' + str(tb.tb_lineno))
                    answer_text = ""
                    
                # Добавим все доступные переходы (кнопки)
                if unified_message['new_chat_trigger']['repeat_last_command_next_commands'] == "true" and unified_message['last_chat_trigger']['repeatable_next_commands'] == "true":
                    for command in unified_message['last_chat_trigger']['next_commands']:
                        if command != "" and command.lower() not in str(unified_message['response_commands']).lower():
                            unified_message['response_commands'] = unified_message['response_commands'] + [command]
    
                # Подготовим разметку
                if len(unified_message['new_chat_trigger']['next_commands']) > 0:
                    unified_message['response_markup']['row_width'] = 1 
                    unified_message['response_markup']['one_time_keyboard'] = True
                else:
                    unified_message['response_markup']['row_width'] = 0 
                    unified_message['response_markup']['one_time_keyboard'] = False
        
                # Выполним функцию-обработчик для контекста (предыдущего сообщения)
                unified_message['last_answer_func'] = globals()[unified_message['last_chat_trigger']['answer_func']]
                unified_message = unified_message['last_answer_func'](unified_message)
    except Exception as exc:
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog("*** Exception caught during message context creation: " + str(exc) + ', line ' + str(tb.tb_lineno))

    return unified_message

def createResponseMesssage(unified_message):
    try:
        # Для info команд выберем случайный допустимый ответ и загрузим все следующие команды
        if unified_message['last_chat_trigger']['type'] != "push":
            try:
                # Если одно текстовое сообщение, то выберем его, если их несколько, то выберем случайное
                if len(unified_message['new_chat_trigger']['answer_text']) > 1:
                    answer_text = unified_message['new_chat_trigger']['answer_text'][random.randint(1, len(unified_message['new_chat_trigger']['answer_text'])) - 1]
                elif len(unified_message['new_chat_trigger']['answer_text']) == 1:
                    answer_text = unified_message['new_chat_trigger']['answer_text'][0]
                else:
                    answer_text = ""
                if answer_text != "" and answer_text.lower() not in str(unified_message['response_text']).lower():
                    unified_message['response_text'] = unified_message['response_text'] + [answer_text]
            except Exception as exc:
                exc_type, exc_obj, tb = sys.exc_info()
                app_log.appendLog("*** Exception caught during message creation: " + str(exc) + ', line ' + str(tb.tb_lineno))
                answer_text = ""
                
            # Добавим все доступные переходы (кнопки)
            if str(unified_message['last_chat_trigger']).lower() != bot_command.getBotSimilarityCommand(unified_message).lower() and str(unified_message['new_chat_trigger']).lower() != bot_command.getBotUnknownCommand(unified_message).lower():
                for command in unified_message['new_chat_trigger']['next_commands']:
                    if command != "" and command.lower() not in str(unified_message['response_commands']).lower():
                        unified_message['response_commands'] = unified_message['response_commands'] + [command]
    
        # Для push команд выберем ответ, соответствующий действию пользователя
        if unified_message['last_chat_trigger']['type'] == "push":
            if unified_message['new_chat_record']['last_chat_message'].lower() in unified_message['last_chat_trigger']['push_cancel'].lower():
                text = unified_message['last_chat_trigger']['push_cancel_text']
            else:
                text = unified_message['last_chat_trigger']['after_push_text']
            if text != "" and text.lower() not in str(unified_message['response_text']).lower():
                unified_message['response_text'] = unified_message['response_text'] + [text]

            unified_message['new_chat_record']['last_chat_command'] = unified_message['last_chat_trigger']['after_push_command']
            unified_message['last_chat_record'] = copy.deepcopy(unified_message['new_chat_record'])
            unified_message['new_chat_trigger'] = bot_command.getBotTriggerByBotCommand(unified_message, unified_message['last_chat_trigger']['after_push_command'])
            unified_message['new_chat_trigger']['repeatable_text'] = "true"
            unified_message['new_chat_trigger']['repeatable_next_commands'] = "true"
            unified_message['new_chat_trigger']['repeat_last_command_text'] = "true"
            unified_message['new_chat_trigger']['repeat_last_command_next_commands'] = "true"
            unified_message['last_chat_trigger'] = copy.deepcopy(unified_message['new_chat_trigger'])
            unified_message['last_answer_func'] = globals()[unified_message['last_chat_trigger']['answer_func']]
            
        # Подготовим разметку
        if len(unified_message['new_chat_trigger']['next_commands']) > 0:
            unified_message['response_markup']['row_width'] = 1 
            unified_message['response_markup']['one_time_keyboard'] = True
        else:
            unified_message['response_markup']['row_width'] = 0 
            unified_message['response_markup']['one_time_keyboard'] = False

        # Выполним функцию-обработчик для текущего сообщения
        unified_message['new_answer_func'] = globals()[unified_message['new_chat_trigger']['answer_func']]
        unified_message = unified_message['new_answer_func'](unified_message)
    except Exception as exc:
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog("*** Exception caught during current message creation: " + str(exc) + ', line ' + str(tb.tb_lineno))

    return unified_message


# ФУНКЦИИ, СОЗДАЮЩИЕ КОНТЕНТ В ОТВЕТАХ ЧАТА

def answerEVENT(unified_message):
    try:
        if unified_message['event_id'] == u"conversation_started":
            unified_message['response_text'] = [u"Привет, рад тебя видеть! Спрашивай, расскажу все, что знаю о нашем Банке."]
	    unified_message['response_commands'] = [u"Задать вопрос", u"Сообщить о сложностях в работе"]
        else:
            unified_message['response_text'] = []
    except Exception as exc:
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog(u"*** Exception caught during trigger assemble by answerEVENT: " + str(exc) + ', line ' + str(tb.tb_lineno))
    return unified_message

def answerEMPTY(unified_message):
    try:
        unified_message['response_text'] = unified_message['response_text']
    except Exception as exc:
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog(u"*** Exception caught during trigger assemble by answerEMPTY: " + str(exc) + ', line ' + str(tb.tb_lineno))
    return unified_message

    
def answerPUSH(unified_message):
    try:
        unified_message['response_text'] = unified_message['response_text']
    except Exception as exc:
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog(u"*** Exception caught during trigger assemble by answerPUSH: " + str(exc) + ', line ' + str(tb.tb_lineno))
    return unified_message


def answerUNKNOWN(unified_message):
    try:
        unified_message['response_text'] = unified_message['response_text']
    except Exception as exc:
        exc_type, exc_obj, tb = sys.exc_info()
        app_log.appendLog(u"*** Exception caught during trigger assemble by answerUNKNOWN: " + str(exc) + ', line ' + str(tb.tb_lineno))
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
        app_log.appendLog(u"*** Exception caught during trigger assemble by answerSIMILAR: " + str(exc) + ', line ' + str(tb.tb_lineno))
    return unified_message

