# coding: utf8 

from __future__ import unicode_literals
from django.db import models
from . import app_config
from . import app_log
import sys

# Конфигурации чат-ботов
BOT_CONFIGS = {
   # "279802369:AAG11qQrJlySYTmozSq4Jno0ekNP7RbBdlc": {
   #     "name" : "bot_tlgrm_adopt_uat",
   #     "type" : "telegram",
   #     "start" : "no",
   #     "api_token" : "279802369:AAG11qQrJlySYTmozSq4Jno0ekNP7RbBdlc",
   #     "web_hook_url" : "https://pure-coast-15562-heroku-18.herokuapp.com:443/universal_bot_dispatcher/279802369:AAG11qQrJlySYTmozSq4Jno0ekNP7RbBdlc/",
   #     "web_hook_ssl_sert" : "",
   #     "web_hook_ssl_priv" : "",
   #     "knowledge_profile" : "adopt",
   #     "module": "bot_telegram",
   #     "module_config" : {
   #         "text_message_length" : 300
   #     },
   #     "accept_text_messages" : 'yes',
   #     "accept_event_messages" : 'yes',
   #     "accept_picture_messages" : 'no',
   #     "accept_sound_messages" : 'no',
   #     "accept_video_messages" : 'no',
   #     "state" : "running"
   # },
    "48c64f31e6a7d79d-e0f1d73fd500afe4-2e7bc35ea8b893f": {
        "name" : u"hrcetelem",
        "type" : "viber",
        "start" : "yes",
        "api_token" : "48c64f31e6a7d79d-e0f1d73fd500afe4-2e7bc35ea8b893f",
        "web_hook_url" : "https://pure-coast-15562-heroku-18.herokuapp.com:443/universal_bot_dispatcher/48c64f31e6a7d79d-e0f1d73fd500afe4-2e7bc35ea8b893f/",
        "web_hook_ssl_sert" : "",
        "web_hook_ssl_priv" : "",
        "knowledge_profile" : "adopt",
        "module": "bot_viber",
        "module_config" : {
            "text_message_length" : '300'
        },
        "accept_text_messages" : 'yes',
        "accept_event_messages" : 'yes',
        "accept_picture_messages" : 'no',
        "accept_sound_messages" : 'no',
        "accept_video_messages" : 'no',
        "state" : "running"
    },
    "49e8d10c7d27d26a-3e72f70e63166065-4d73250fa4de5153": {
        "name" : u"hrcetelemrkz",
        "type" : "viber",
        "start" : "yes",
        "api_token" : "49e8d10c7d27d26a-3e72f70e63166065-4d73250fa4de5153",
        "web_hook_url" : "https://pure-coast-15562-heroku-18.herokuapp.com:443/universal_bot_dispatcher/49e8d10c7d27d26a-3e72f70e63166065-4d73250fa4de5153/",
        "web_hook_ssl_sert" : "",
        "web_hook_ssl_priv" : "",
        "knowledge_profile" : "adoptrkz",
        "module": "bot_viber",
        "module_config" : {
            "text_message_length" : '300'
        },
        "accept_text_messages" : 'yes',
        "accept_event_messages" : 'yes',
        "accept_picture_messages" : 'no',
        "accept_sound_messages" : 'no',
        "accept_video_messages" : 'no',
        "state" : "running"
    }
}

# Профиль знаний бота для адаптации новичков РКЦ
MESSAGE_MAP_ADOPT_RKZ = {
    "/start": {
        "command": "/start",
        "previous_commands": ["*"],
        "next_commands": [u"Задать вопрос", u"Сообщить о сложностях в работе"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Привет! Для начала давай познакомимся. Я - бот! Нестандартное решение для твоей адаптации)) С моей помощью ты можешь легко узнать любую информацию. Если я иногда не буду понимать тебя, то буду переспрашивать."],
        "re": ["hi", u"привет", u"здравствуйте", u"добрый день", u"добрый вечер", u"доброе утро", u"начать"],
        "type": "info"
    },
    u"начать заново": {
        "command": u"Начать заново",
        "previous_commands": ["*"],
        "next_commands": [u"Задать вопрос", u"Сообщить о сложностях в работе"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"О чем хочешь узнать?" + u"\U0001F609"],
        "re": [u"начать заново"],
        "type": "info"
    },
    u"задать вопрос": {
        "command": u"Задать вопрос",
        "previous_commands": ["/start"],
        "next_commands": [u"Важные контакты", u"О банке", u"Наши ценности", u"Рабочие моменты", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Что именно тебя интересует (выбор ниже)?"],
        "re": [u"задать вопрос", u"вопрос"],
        "type": "info"
    },
    u"важные контакты": {
        "command": u"Важные контакты",
        "previous_commands": ["задать вопрос"],
        "next_commands": [u"HR", u"Вопросы обучения", u"Отдел кадров", u"Другой контакт", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"О каких контактах ты хотел бы узнать?"],
        "re": [u"контакт", u"телефон", u"почта", u"емэйл", u"email"],
        "type": "info"
    },
    u"о банке": {
        "command": u"О банке",
        "previous_commands": ["задать вопрос"],
        "next_commands": [u"Общая информация", u"Отделы РКЦ", u"Цель и миссия", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"О чем ты хотел бы спросить?"],
        "re": [u"банк", u"сетелем", u"кредито", u"cetelem", u"bank"],
        "type": "info"
    },
    u"общая информация": {
        "command": u"О банке",
        "previous_commands": ["О банке"],
        "next_commands": [u"О банке", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u""" 
'Сетелем Банк' ООО - Крупнейший универсальный банк Российской Федерации и стран СНГ. Сбербанку принадлежит 79,2% акций и 20,8% акции принадлежит Банку BNP PARIBAS.
Наш Банк специализируется на АВТО-кредитовании, Кредитование подержанных автомобилей и Кредиту наличными.
        """],
        "re": [u"обшая", u"информация", u"специализация", u"банк", u"сетелем", u"cetelem"],
        "type": "info"
    },
    u"отделы ркц": {
        "command": u"Отделы РКЦ",
        "previous_commands": ["О банке"],
        "next_commands": [u"О банке", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u""" 
Отделы РКЦ:
    Руководитель центра.
    Отдел досудебного взыскания.
    Группа подачи заявлений в судебные органы.
    Группа контроля качества и поддержки процессов взыскания.
    Отдел клиентского обслуживания.
    Отдел претензионной и операционной работы.
    Группа аналитики и контроля качества операционных процессов.
    Отдел телемаркетинга.
    Отдел анализа кредитных заявок.
    Группа операционной поддержки и сопровождения кредитных операций.
    Группа информационных технологий.
    Группа по работе с персоналом.
    Служба защиты бизнеса.
    Административно – хозяйственная группа.
        """],
        "re": [u"центр", u"ркц", u"РКЦ", u"отдел", u"структура"],
        "type": "info"
    },
    u"цель и миссия": {
        "command": u"Цель и миссия",
        "previous_commands": ["О банке"],
        "next_commands": [u"О банке", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"""
Наша цель - cтать лидером на рынке потребительского кредитования и автокредитования. Быть лидером в сфере ответственного кредитования.
Наше видение - предоставлять финансовые решения, направленные на улучшение качества жизни наших потребителей.
        """],
        "re": [u"цель", u"миссия", u"РКЦ", u"банк", u"сетелем", u"cetelem"],
        "type": "info"
    },
    u"наши ценности": {
        "command": u"Наши ценности",
        "previous_commands": ["задать вопрос"],
        "next_commands": [u"Да (расскажи про ценности)", u"Нет (не надо про ценности)", u"О банке", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Хотел бы узнать о ценностях, принятых у нас в Банке?"],
        "re": [u"ценност", u"лидер", u"команда", u"клиент"],
        "type": "info"
    },
    u"нет (не надо про ценности)": {
        "command": u"Нет (не надо про ценности)",
        "previous_commands": ["о банке"],
        "next_commands": [u"О банке", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Хорошо, сейчас не будем про ценности, но когда у тебя будет время, ознакомься с ними внимательнее. Это поможет тебе понять, что от тебя ожидают на работе."],
        "re": [u"UYFE!!#&TEH"],
        "type": "info"
    },
    u"да (расскажи про ценности)": {
        "command": u"Да (расскажи про ценности)",
        "previous_commands": ["о банке"],
        "next_commands": [u"О банке", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"""
Я - ЛИДЕР
    Я принимаю ответственность за себя и за то, что происходит вокруг
    Я честен с собой, коллегами и Клиентами
    Я совершенствую себя, Банк и наше окружение, делая лучшее, на что способен
МЫ - КОМАНДА
    Мы с готовностью помогаем друг другу, работая на общий результат
    Мы помогаем расти и развиваться нашим коллегам
    Мы открыты, уважаем коллег и доверяем друг другу
ВСЕ - ДЛЯ КЛИЕНТА
    Я принимаю ответственность за себя и за то, что происходит вокруг
    Я честен с собой, коллегами и Клиентами
    Я совершенствую себя, Банк и наше окружение, делая лучшее, на что способен
        """],
        "re": [u"UYFE!!#&TEH"],
        "type": "info"
    },
    u"рабочие моменты": {
        "command": u"Рабочие моменты",
        "previous_commands": ["задать вопрос"],
        "next_commands": [u"Рабочий график", u"Мотивация денежная", u"Отпуск", u"Карьера", u"Плюшки и бонусы", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Да, в работе много тонконстей, о чем хотел бы узнать?"],
        "re": [u"банк", u"сетелем", u"кредито", u"cetelem", u"bank"],
        "type": "info"
    },
    u"сообщить о сложностях в работе": {
        "command": u"Сообщить о сложностях в работе",
        "previous_commands": ["начать заново"],
        "next_commands": ["Отмена"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "false",
        "after_push_command": u"начать заново",
        "after_push_text": u"Спасибо, что рассказал нам о своей ситуации. Мы обязательно рассмотрим ее и в случае необходимости примем меры.",
        "push_cancel": u"отмена",
        "push_cancel_text": u"Операция отменена.",
        "answer_func": "answerPUSH",
        "answer_text": [u"Подробно опиши свою ситуацию, я передам информацию нужным коллегам (или напиши слово 'отмена'):"],
        "re": [u"сложно", u"проблем", u"трудно"],
        "type": "push"
    },
    u"помощь": {
        "command": u"Помощь",
        "previous_commands": ["*"],
        "next_commands": [],
        "repeat_last_command_text": "true",
        "repeat_last_command_next_commands": "true",
        "repeatable_text": "false",
        "repeatable_next_commands": "false",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Чтобы получить интересующую информацию воспользуйся меню внизу экрана или напиши вопрос в строке сообщения. Если на какой-то вопрос я не смогу ответить, то попробуй задать его снова через день, возможно, я уже буду знать на него ответ. Чтобы попасть в меню нажми на /start."],
        "re": [u"помощь"],
        "type": "info"
    },
    "/unknown": {
        "command": "/unknown",
        "previous_commands": ["*"],
        "next_commands": [u"Помощь"],
        "repeat_last_command_text": "true",
        "repeat_last_command_next_commands": "true",
        "repeatable_text": "false",
        "repeatable_next_commands": "false",
        "answer_func": "answerUNKNOWN",
        "answer_text": [u"Видимо у меня есть ещё не вся информация о работе в Сетелем, но я обязательно узнаю то, что тебе нужно, и смогу ответить позже. Напиши мне завтра."],
        "re": [],
        "transit_to": "{GOBACK}",
        "type": "transit"
    },
    "/event": {
        "command": "/event",
        "previous_commands": ["*"],
        "next_commands": [],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "false",
        "answer_func": "answerEVENT",
        "answer_text": [""],
        "re": ['/event'],
        "transit_to": "",
        "type": "info"
    },
    "/similar": {
        "command": "/similar",
        "previous_commands": ["*"],
        "next_commands": [""],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_text": [u"Ой, я не совсем понял, что ты спросил. Пожалуйста, выбери нужный пункт из списка внизу."],
        "answer_func": "answerSIMILAR",
        "re": [],
        "type": "info"
    },
    "/picture": {
        "command": "/picture",
        "previous_commands": ["*"],
        "next_commands": [""],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_text": [u"Спасибо за картинку, обязательно посмотрю его позже."],
        "answer_func": "answerPICTURE",
        "re": [],
        "type": "picture"
    },
    "/sound": {
        "command": "/sound",
        "previous_commands": ["*"],
        "next_commands": [""],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_text": [u"Спасибо за звуковой файл, обязательно послушаю его позже."],
        "answer_func": "answerSOUND",
        "re": [],
        "type": "sound"
    },
    "/video": {
        "command": "/video",
        "previous_commands": ["*"],
        "next_commands": [""],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_text": [u"Видео? Мне? Спасибо, обязательно посмотрю его позже."],
        "answer_func": "answerMOVIE",
        "re": [],
        "type": "video"
    }
}

# Профиль знаний бота для адаптации КЭ
MESSAGE_MAP_ADOPT = {
    "/start": {
        "command": "/start",
        "previous_commands": ["*"],
        "next_commands": [u"Задать вопрос", u"Сообщить о сложностях в работе"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Привет, коллега! Меня зовут – HR bot – я твой электронный помощник " + u"\U0001F4F1" + u"\nЯ как и ты совсем недавно присоединился к команде Сетелем Банка, но уже многое узнал о работе здесь и готов поделиться с тобой своим опытом! Задавай мне вопросы, предлагай идеи, оставляй обратную связь. Я уверен, что мы подружимся " + u"\U0001F60A"],
        "re": ["hi", u"привет", u"здравствуйте", u"добрый день", u"добрый вечер", u"доброе утро", u"начать"],
        "type": "info"
    },
    u"начать заново": {
        "command": u"Начать заново",
        "previous_commands": ["*"],
        "next_commands": [u"Задать вопрос", u"Сообщить о сложностях в работе"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Чего изволишь?" + u"\U0001F609"],
        "re": [u"начать заново"],
        "type": "info"
    },
    u"задать вопрос": {
        "command": u"Задать вопрос",
        "previous_commands": ["/start"],
        "next_commands": [u"Форс-мажор", u"Моя мотивация"+u"\U0001F4B0", u"Моё развитие", u"Карьерный рост", u"Мой рабочий график", u"Отпуск", u"Льготы", u"Конфликты с руководством", u"Разное", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Что именно тебя интересует (выбор ниже)?"],
        "re": [u"задать вопрос", u"вопрос"],
        "type": "info"
    },
    u"форс-мажор": {
        "command": u"Форс-мажор",
        "previous_commands": [u"задать вопрос"],
        "next_commands": [u"Не знаю процедуру", u"Клиент поставил в тупик", u"Сложная ситуация в выходные", u"Через неделю клиенту исполняется 45 лет, можем ли мы его оформить?", u"Я заболел(а) и не могу выйти на работу", u"Здесь нет моего случая", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Бывает, что на работе случаются различные непредвиденные ситуации. А что случилось у тебя?"],
        "re": [u"форс", u"мажор"],
        "type": "info"
    },
    u"не знаю процедуру": {
        "command": u"Не знаю процедуру",
        "previous_commands": [u"форс-мажор"],
        "next_commands": [u"Форс-мажор", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Ты можешь написать письмо в службу поддержки КЭ на электронный адрес PHL. Кроме того, за тобой закреплен СКЭ и ВКЭ - можешь обратиться с вопросом к ним. Старшие коллеги с радостью помогут тебе в решении проблем."],
        "re": [u"знаю", u"процедур"],
        "type": "info"
    },
    #u"если вместо военного билета предоставили служебное удостоверение": {
    #    "command": u"Если вместо военного билета предоставили служебное удостоверение",
    #    "previous_commands": [u"форс-мажор"],
    #    "next_commands": [u"Форс-мажор", u"Начать заново"],
    #    "repeat_last_command_text": "false",
    #    "repeat_last_command_next_commands": "false",
    #    "repeatable_text": "false",
    #    "repeatable_next_commands": "true",
    #    "answer_func": "answerEMPTY",
    #    "answer_text": [u"Извиняюсь, пока не могу отвечать на этот вопрос здесь. Пиши сюда, они точно помогут - PHL@cetelem.ru"],
    #    "re": [u"военн", u"служебн", u"удостов"],
    #    "type": "info"
    #},
    u"клиент поставил в тупик": {
        "command": u"Клиент поставил в тупик",
        "previous_commands": [u"форс-мажор"],
        "next_commands": [u"Форс-мажор", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Без паники, у тебя есть несколько вариантов, как выйти из ситуации! 1. Позвони своему СКЭ, ВКЭ или РГКЭ. 2. Позвони по бесплатному телефону для КЭ 8 (800) 500-55-06. 3. Напиши письмо на PHL@cetelem.ru; формат темы письма: [твой вопрос], в теле письма кратко и понятно опиши сложившуюся ситуацию. Тебе обязательно помогут, и всё будет хорошо!"],
        "re": [u"клиент", u"тупик", u"сложно"],
        "type": "info"
    },
    u"сложная ситуация в выходные": {
        "command": u"Сложная ситуация в выходные",
        "previous_commands": [u"форс-мажор"],
        "next_commands": [u"Форс-мажор", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Если проблемы связаны с сетью Интернет, то необходимо обратиться к администратору диллерского центра. Если у тебя есть необходимость в авторизации кредитных договоров, то необходимо позвонить по телефону бесплатной горячей линии для КЭ: 8 (800) 500-55-06, а также уведомить своего непосредственного руководителя о данной проблеме"],
        "re": [u"сложно", u"выходн", u"ситуация"],
        "type": "info"
    },
    u"через неделю клиенту исполняется 45 лет, можем ли мы его оформить?": {
        "command": u"Через неделю клиенту исполняется 45 лет, можем ли мы его оформить?",
        "previous_commands": [u"форс-мажор"],
        "next_commands": [u"Форс-мажор", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Да, можем. На день приема клиенту 44 года и паспорт является действительным."],
        "re": [u"оформить", u"лет", u"исполняется"],
        "type": "info"
    },
    u"я заболел(а) и не могу выйти на работу": {
        "command": u"Я заболел(а) и не могу выйти на работу",
        "previous_commands": [u"форс-мажор"],
        "next_commands": [u"Форс-мажор", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"В первую очередь уведоми своего непосредственного руководителя. Он подскажет как быть в этой ситуации. Выздоравливай!"],
        "re": [u"заболел", u"выйти", u"работа", u"болит"],
        "type": "info"
    },
    u"здесь нет моего случая": {
        "command": u"здесь нет моего случая",
        "previous_commands": [u"форс-мажор"],
        "next_commands": [u"Оставить предложение/отзыв", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Ну бывает и такое…Задай вопрос своему непосредственному руководителю или Специалисту по персоналу твоего Представительства, а нам оставь отзыв - будем очень признательны!"],
        "re": [],
        "type": "info"
    },
    u"моего вопроса здесь нет": {
        "command": u"моего вопроса здесь нет",
        "previous_commands": [u"форс-мажор"],
        "next_commands": [u"Оставить предложение/отзыв", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Ну бывает и такое… Задай вопрос своему непосредственному руководителю, а нам оставь отзыв - будем очень признательны!"],
        "re": [],
        "type": "info"
    },
    #u"моя мотивация"+u"\U0001F4B0":{
    #    "command": u"Моя мотивация"+u"\U0001F4B0",
    #    "previous_commands": [u"задать вопрос"],
    #    "next_commands": [u"Мотивационная программа АВТО", u"Начать заново"],
    #    "repeat_last_command_text": "false",
    #    "repeat_last_command_next_commands": "false",
    #    "repeatable_text": "true",
    #    "repeatable_next_commands": "true",
    #    "answer_func": "answerEMPTY",
    #    "answer_text": [u"Выбери нужное, не стесняйся"],
    #    "re": [u"мотивация", u"премия"],
    #    "type": "info"
    #},
    #u"мотивационная программа пос":{
    #    "command": u"Мотивационная программа пос",
    #    "previous_commands": [u"моя мотивация"+u"\U0001F4B0"],
    #    "next_commands": [u"Как рассчитать премию ПОС",u"Где я могу посмотреть свою мотивационную программу ПОС",u"Где найти калькулятор для расчета премии",u"Моя мотивация"+u"\U0001F4B0",u"Начать заново"],
    #    "repeat_last_command_text": "false",
    #    "repeat_last_command_next_commands": "false",
    #    "repeatable_text": "true",
    #    "repeatable_next_commands": "true",
    #    "answer_func": "answerEMPTY",
    #    "answer_text": [u"Какой вопрос тебя интересует?"],
    #    "re": [u"програм", u"мотив", u"пос"],
    #    "type": "info"
    #},
    #u"как рассчитать премию пос": {
    #    "command": u"Как рассчитать премию пос",
    #   "previous_commands": [u"мотивационная программа пос"],
    #    "next_commands": [u"Мотивационная программа ПОС",u"Начать заново"],
    #    "repeat_last_command_text": "false",
    #    "repeat_last_command_next_commands": "false",
    #    "repeatable_text": "false",
    #    "repeatable_next_commands": "true",
    #    "answer_func": "answerEMPTY",
    #    "answer_text": [u"Чтобы рассчитать свою премию, нужно ознакомиться с мотивационной программой. Она размещена в твоём личном кабинете, в каталоге информационных писем на Учебном портале (sdo.cetelem.ru). На Учебном портале ты также можешь пройти курс «Мотивация ПОС» – в нём ты найдешь примеры расчета премии и тебе будет легко разобраться. Для того чтобы зайти в личный кабинет, введи свои логин и пароль от Учебного портала. Если у тебя будут вопросы, задай их своему руководителю – он обязательно поможет тебе!"],
    #    "re": [u"рассчет премии", u"преми", u"рассч", u"пос"],
    #    "type": "info"
    #},
    #u"где я могу посмотреть свою мотивационную программу пос": {
    #    "command": u"Где я могу посмотреть свою мотивационную программу пос",
    #    "previous_commands": [u"мотивационная программа пос"],
    #    "next_commands": [u"Мотивационная программа ПОС",u"Начать заново"],
    #    "repeat_last_command_text": "false",
    #    "repeat_last_command_next_commands": "false",
    #    "repeatable_text": "false",
    #    "repeatable_next_commands": "true",
    #    "answer_func": "answerEMPTY",
    #    "answer_text": [u"Мотивационная программа для Кредитных экспертов ПОС размещена в твоём личном кабинете, в каталоге информационных писем на Учебном портале (sdo.cetelem.ru). Для того чтобы зайти в личный кабинет, введи свои логин и пароль от Учебного портала. Если у тебя будут вопросы, задай их своему руководителю – он обязательно поможет тебе!"],
    #    "re": [u"мотив", u"програм", u"пос"],
    #    "type": "info"
    #},
    #u"где найти калькулятор для расчета премии": {
    #    "command": u"Где найти калькулятор для расчета премии",
    #    "previous_commands": [u"мотивационная программа пос"],
    #    "next_commands": [u"Мотивационная программа ПОС",u"Начать заново"],
    #    "repeat_last_command_text": "false",
    #    "repeat_last_command_next_commands": "false",
    #    "repeatable_text": "false",
    #    "repeatable_next_commands": "true",
    #    "answer_func": "answerEMPTY",
    #    "answer_text": [u"Калькулятор для расчета премии ты найдешь в Библиотеке Телематик. Зайди в Библиотеку Телематик и следуй маршруту:\nПапка в Библиотеке Телематик > Документация > POS > 01.07 Тарифы и калькуляторы:\n>Если у тебя Open Office: Калькулятор для КЭ ПОС для расчета премии (Open Office)_pattern.ods\n>Если у тебя MS Office:  Калькулятор для КЭ ПОС для расчета премии (MS Office)_pattern.xls\nЕсли у тебя будут вопросы, задай их своему руководителю – он обязательно поможет тебе!"],
    #    "re": [u"кальк", u"расчет", u"преми", u"пос"],
    #    "type": "info"
    #},
    u"моя мотивация"+u"\U0001F4B0":{
        "command": u"Моя мотивация"+u"\U0001F4B0",
        "previous_commands": [u"моя мотивация"+u"\U0001F4B0"],
        "next_commands": [u"Как рассчитать премию АВТО",u"Где я могу посмотреть свою мотивационную программу АВТО",u"Моего вопроса здесь нет",u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Какой вопрос тебя интересует?"],
        "re": [u"программа", u"мотив", u"авто"],
        "name": u"Мотивационная программа АВТО",
        "type": "info"
    },
    u"как рассчитать премию авто": {
        "command": u"Как рассчитать премию авто",
        "previous_commands": [u"мотивационная программа авто"],
        "next_commands": [u"Моя мотивация"+u"\U0001F4B0",u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Чтобы рассчитать свою премию, нужно ознакомиться с мотивационной программой. Она размещена в твоём личном кабинете, в каталоге информационных писем на Учебном портале (sdo.cetelem.ru). Для того чтобы зайти в личный кабинет, введи свои логин и пароль от Учебного портала. Если у тебя будут вопросы, задай их своему руководителю – он обязательно тебе поможет!"],
        "re": [u"расчет", u"авто", u"преми"],
        "type": "info"
    },
    u"где я могу посмотреть свою мотивационную программу авто": {
        "command": u"Где я могу посмотреть свою мотивационную программу авто",
        "previous_commands": [u"мотивационная программа авто"],
        "next_commands": [u"Моя мотивация"+u"\U0001F4B0",u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Мотивационная программа для Кредитных экспертов АВТО размещена в твоём личном кабинете, в каталоге информационных писем на Учебном портале (sdo.cetelem.ru). Для того чтобы зайти в личный кабинет, введи свои логин и пароль от Учебного портала. Если у тебя будут вопросы, задай их своему руководителю – он обязательно поможет тебе!"],
        "re": [u"мотив", u"програм", u"авто"],
        "type": "info"
    },
    u"моё развитие": {
        "command": u"Моё развитие",
        "previous_commands": [u"задать вопрос"],
        "next_commands": [u"Тренинги для новых сотрудников", u"Как записаться на тренинг?", u"Дистанционное обучение", u"Моего вопроса здесь нет", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Обучение и развитие - это основа профессионализма и успеха! Что конкретно тебя интересует?"],
        "re": [u"развитие", u"тренинг", u"обучение"],
        "type": "info"
    },
    u"тренинги для новых сотрудников": {
        "command": u"Тренинги для новых сотрудников",
        "previous_commands": [u"Моё развитие"],
        "next_commands": [u"Моё развитие", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Здорово! Мы любим целеустремленных и желающих развиваться! Информацию о тренингах для новых сотрудников ты можешь получить у своего непосредственного руководителя, а также у Бизнес-тренера своего Представительства."],
        "re": [u"тренинг", u"обучение", u"новичок", u"новый", u"сотрудник"],
        "type": "info"
    },
    u"как записаться на тренинг?": {
        "command": u"Как записаться на тренинг?",
        "previous_commands": [u"Моё развитие"],
        "next_commands": [u"Моё развитие", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Обратись с этим вопросом к своему непосредственному руководителю, или Бизнес-тренеру своего Представительства."],
        "re": [u"тренинг", u"запись", u"обучение", u"записаться"],
        "type": "info"
    },
    u"дистанционное обучение": {
        "command": u"Дистанционное обучение",
        "previous_commands": [u"Моё развитие"],
        "next_commands": [u"Моё развитие", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Дистанционное обучение ты можешь пройти здесь - sdo.cetelem.ru. Для того чтобы зайти в личный кабинет, введи свой логин и пароль от учебного портала. Если у тебя будут вопросы, задай их своему руководителю - он обязательно тебе поможет!"],
        "re": [u"дистанц", u"обучение", u"портал"],
        "type": "info"
    },
    u"карьерный рост": {
        "command": u"Карьерный рост",
        "previous_commands": [u"задать вопрос"],
        "next_commands": [u"Возможно ли повышение", u"Как перейти в офис", u"Открытые вакансии", u"Моего вопроса здесь нет", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Ага, подробности ниже " + u"\U0001F609"],
        "re": [u"карьерный рост", u"карьер", u"рост"],
        "type": "info"
    },
    u"возможно ли повышение": {
        "command": u"Возможно ли повышение",
        "previous_commands": [u"карьерный рост"],
        "next_commands": [u"Карьерный рост", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Да, в Сетелем мы всегда стараемся повышать своих сотрудников! Показывай высокие результаты, проходи все курсы, следи за рассылками вакансий (portal.jv.ru) и не упускай свой шанс продвинуться по карьерной лестнице."],
        "re": [u"повышен", u"повысят", u"должност"],
        "type": "info"
    },
    #u"через сколько возможно повышение": {
    #    "command": u"Через сколько возможно повышение",
    #    "previous_commands": [u"карьерный рост"],
    #    "next_commands": [u"Карьерный рост", u"Начать заново"],
    #    "repeat_last_command_text": "false",
    #    "repeat_last_command_next_commands": "false",
    #    "repeatable_text": "false",
    #    "repeatable_next_commands": "true",
    #    "answer_func": "answerEMPTY",
    #    "answer_text": [u"По правилам Банка сотрудник должен отработать 6 месяцев, чтобы претендовать на перевод или повышение"],
    #    "re": [u"повышен", u"повысят", u"должност"],
    #    "name": u"Через сколько возможно повышение",
    #    "type": "info"
    #},
    u"как перейти в офис": {
        "command": u"Как перейти в офис",
        "previous_commands": [u"карьерный рост"],
        "next_commands": [u"Карьерный рост", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Следи за актуальными вакансиями на (portal.jv.ru) или через коммуникации. Когда тебе понравится вакансия, отправь свое резюме по указанным контактам и поставь в копию своего руководителя. При переводе учитывается стаж работы в банке (желательно более 6 месяцев), результаты работы и собеседования."],
        "re": [u"офис", u"работа", u"повышен"],
        "type": "info"
    },
    u"открытые вакансии": {
        "command": u"Открытые вакансии",
        "previous_commands": [u"карьерный рост"],
        "next_commands": [u"Карьерный рост", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Информацию об открытых вакансиях ты найдешь здесь - (portal.jv.ru), а также из регулярных рассылок об открытых вакансиях."],
        "re": [u"вакансии", u"работа", u"повышен"],
        "type": "info"
    },
    #u"кто такие универсальные агенты": {
    #    "command": u"Кто такие универсальные агенты",
    #    "previous_commands": [u"карьерный рост"],
    #    "next_commands": [u"Карьерный рост",u"Начать заново"],
    #    "repeat_last_command_text": "false",
    #    "repeat_last_command_next_commands": "false",
    #    "repeatable_text": "false",
    #    "repeatable_next_commands": "true",
    #    "answer_func": "answerEMPTY",
    #    "answer_text": [u"Универсальный агент - новая возможность для работы в Банке. Универсальные агенты могут гибко управлять своим временем и получать неограниченный доход. Узнать все подробности о работе агентом ты можешь у своего руководителя или Специалиста по подбору персонала твоего Макрорегиона"],
    #    "re": [u"агент", u"универсал"],
    #    "type": "info"
    #},
    u"отпуск": {
        "command": u"Отпуск",
        "previous_commands": [u"Я помогу тебе найти ответы на вопросы про отпуск, выбери нужный."],
        "next_commands": [u"Первый отпуск", u"Как оформить заявление на отпуск?", u"Когда мне переведут отпускные", u"Здесь нет моего случая", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Хочешь в отпуск, но что-то не знаешь о нем? Я помогу " + u"\U00002B07"],
        "re": [u"отпуск", u"сессия"],
        "type": "info"
    },
    u"первый отпуск": {
        "command": u"Первый отпуск",
        "previous_commands": [u"отпуск"],
        "next_commands": [u"Отпуск", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"В первый отпуск можно пойти через 6 месяцев после начала работы. Но если тебе нужно раньше, обсуди этот вопрос с руководителем и Специалистом по персоналу твоего РП."],
        "re": [u"отпуск", u"первый"],
        "type": "info"
    },
    u"как оформить заявление на отпуск?": {
        "command": u"Как оформить заявление на отпуск?",
        "previous_commands": [u"отпуск"],
        "next_commands": [u"Отпуск", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Для того, чтобы пойти в ежегодный оплачиваемый отпуск, необходимо: 1) явиться в офис за 14 календарных дней до начала отпуска, 2) написать заявление на отпуск, 3) согласовать заявление с Руководителем, 4) передать его Специалисту по персоналу, 5) подписать приказ о предоставлении ежегодного отпуска. Если тебе нужно предоставить отпуск без сохранения заработной платы, то ты можешь подать заявление за один день до его начала, также согласовав его с Руководителем."],
        "re": [u"заявление", u"отпуск"],
        "type": "info"
    },
    u"когда мне переведут отпускные": {
        "command": u"Когда мне переведут отпускные",
        "previous_commands": [u"отпуск"],
        "next_commands": [u"Отпуск", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Отпускные выплачиваются сотруднику не позднее чем за три дня до начала отпуска."],
        "re": [u"отпускные", u"отпуск"],
        "type": "info"
    },
    #u"отпуск во время сессии": {
    #    "command": u"Отпуск во время сессии",
    #    "previous_commands": [u"отпуск"],
    #    "next_commands": [u"Отпуск", u"Начать заново"],
    #    "repeat_last_command_text": "false",
    #    "repeat_last_command_next_commands": "false",
    #    "repeatable_text": "false",
    #    "repeatable_next_commands": "true",
    #    "answer_func": "answerEMPTY",
    #    "answer_text": [u"Твой руководитель точно знает ответ на этот вопрос."],
    #    "re": [u"отпуск", u"сесси"],
    #    "type": "info"
    #},
    #u"оплачивается ли сессия": {
    #    "command": u"Оплачивается ли сессия",
    #    "previous_commands": [u"отпуск"],
    #    "next_commands": [u"Отпуск", u"Начать заново"],
    #    "repeat_last_command_text": "false",
    #    "repeat_last_command_next_commands": "false",
    #    "repeatable_text": "false",
    #    "repeatable_next_commands": "true",
    #    "answer_func": "answerEMPTY",
    #    "answer_text": [u"Твой руководитель точно знает ответ на этот вопрос."],
    #    "re": [u"отпуск", u"сесси", u"оплач", u"оплат"],
    #    "type": "info"
    #},
    u"льготы": {
        "command": u"Льготы",
        "previous_commands": [u"задать вопрос"],
        "next_commands": [u"Кредит Сбербанка", u"Льготный кредит", u"Ипотека по сниженной ставке", u"Моего вопроса здесь нет", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Льготы - это хорошо, я о них кое-что знаю."],
        "re": [u"льгот"],
        "type": "info"
    },
    u"кредит сбербанка": {
        "command": u"Кредит Сбербанка",
        "previous_commands": [u"льготы"],
        "next_commands": [u"Льготы", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Уже через 3 месяца после трудоустройства ты можешь подать заявку на кредит в Сбербанк. Узнай детали из презентации по льготному кредитованию от Сбербанка в библиотеке Телематик - папка '06.03 Компенсации и льготы'."],
        "re": [u"кредит"],
        "type": "info"
    },
    u"льготный кредит": {
        "command": u"Льготный кредит",
        "previous_commands": [u"льготы"],
        "next_commands": [u"Льготы", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"У тебя есть возможность взять потребительский и автокредит по сниженной процентной ставке как в нашем Банке, так и в Сбербанке. Узнай детали из презентации по льготному кредитованию от Сбербанка в библиотеке Телематик - папка '06.03 Компенсации и льготы'."],
        "re": [u"кредит", u"льгот"],
        "type": "info"
    },
    u"ипотека по сниженной ставке": {
        "command": u"Ипотека по сниженной ставке",
        "previous_commands": [u"льготы"],
        "next_commands": [u"Льготы", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"У тебя есть возможность взять ипотеку по сниженной процентной ставке в Сбербанке. Узнай детали из презентации по льготному кредитованию от Сбербанка в библиотеке Телематик - папка '06.03 Компенсации и льготы'."],
        "re": [u"ипотек", u"ставк", u"кредит"],
        "type": "info"
    },
    u"разное": {
        "command": u"Разное",
        "previous_commands": [u"задать вопрос"],
        "next_commands": [u"Необходима копия трудовой", u"Время работы PHL", u"Как платят в Сетелем?", u"Как работается в Сетелем?", u"Какая у меня зарплата?", u"Хотел бы узнать обязанности старшего кредитного эксперта", u"Режим работы отдела кадров", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Другое - тоже не менее важное! О чем хочешь узнать?"],
        "re": [u"другое"],
        "type": "info"
    },
    #u"телефон поддержки": {
    #    "command": u"Телефон поддержки",
    #    "previous_commands": [u"другое"],
    #    "next_commands": [u"Другое", u"Начать заново"],
    #    "repeat_last_command_text": "false",
    #    "repeat_last_command_next_commands": "false",
    #    "repeatable_text": "false",
    #    "repeatable_next_commands": "true",
    #    "answer_func": "answerEMPTY",
    #    "answer_text": [u"Бесплатный телефон поддержки для КЭ 8 (800) 500-55-06."],
    #    "re": [u"телеф", u"поддер"],
    #    "type": "info"
    #},
    #u"нужна 2ндфл": {
    #    "command": u"Нужна 2ндфл",
    #    "previous_commands": [u"другое"],
    #    "next_commands": [u"Другое", u"Начать заново"],
    #    "repeat_last_command_text": "false",
    #    "repeat_last_command_next_commands": "false",
    #    "repeatable_text": "false",
    #    "repeatable_next_commands": "true",
    #    "answer_func": "answerEMPTY",
    #    "answer_text": [u"Отправь СОПу своего РП письмо с информацией за какой период тебе нужна справка 2НДФЛ. СОП передаст запрос дальше. Лучше заказывать такие справки в понедельник, тогда запрос обработают на этой неделе. Справка будет доставлена из ЦО в РП в течение 2-3х недель, о чем ты узнаешь от СОПа. Забрать справку из РП ты можешь сам или через РГКЭ."],
    #    "re": [u"ндфл", u"справк"],
    #    "type": "info"
    #},
    u"необходима копия трудовой": {
        "command": u"Необходима копия трудовой",
        "previous_commands": [u"разное"],
        "next_commands": [u"Разное", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Отправь Специалисту по персоналу твоего РП письмо с просьбой подготовить копию твоей трудовой книжки."],
        "re": [u"копи", u"трудов", u"книг", u"книж"],
        "type": "info"
    },
    #u"сколько работать после заявления об увольнении": {
    #    "command": u"Сколько работать после заявления об увольнении",
    #    "previous_commands": [u"другое"],
    #    "next_commands": [u"Другое", u"Начать заново"],
    #    "repeat_last_command_text": "false",
    #    "repeat_last_command_next_commands": "false",
    #    "repeatable_text": "false",
    #    "repeatable_next_commands": "true",
    #    "answer_func": "answerEMPTY",
    #    "answer_text": [u"Всё будет зависеть от срока работы в Банке: если он менее трёх месяцев, то 3 дня, если больше 3-х месяцев, то максимум 2 неделе. Также ты можешь обсудить с РГКЭ альтернативные сроки."],
    #    "re": [u"уволь"],
    #    "type": "info"
    #},
    #u"выдача карты дтс": {
    #    "command": u"Выдача карты дтс",
    #    "previous_commands": [u"другое"],
    #    "next_commands": [u"Другое",u"Начать заново"],
    #    "repeat_last_command_text": "false",
    #    "repeat_last_command_next_commands": "false",
    #    "repeatable_text": "false",
    #    "repeatable_next_commands": "true",
    #    "answer_func": "answerEMPTY",
    #    "answer_text": [u"Этот ответ точно знает Служба поддери КЭ - PHL@cetelem.ru"],
    #    "re": [u"карта", u"дтс", u"статус", u"выдач", u"выдат"],
    #    "type": "info"
    #},
    u"время работы phl": {
        "command": u"Время работы phl",
        "previous_commands": [u"разное"],
        "next_commands": [u"Разное", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Служба поддержки КЭ работает c 07:00 до 22:00 по МСК. Запросы, направленные на PHL@cetelem.ru в нерабочие часы PHL, будут обработаны с 07:00 до 9:00 по МСК"],
        "re": [u"phl", u"пхл", u"время"],
        "type": "info"
    },
    u"как платят в сетелем?": {
        "command": u"Как платят в Сетелем?",
        "previous_commands": [u"разное"],
        "next_commands": [u"Разное", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Заработная плата выплачивается не реже чем каждые полмесяца в следующие дни: 15-го числа месяца, за исключением февраля, (в феврале выплачивается 14 февраля) – выплата первой части заработной платы; в последний день месяца – выплата окончательного расчета за месяц. В случае, если день выплаты заработной платы приходится на выходной или нерабочий праздничный день, заработная плата подлежит выплате в предшествующий рабочий день."],
        "re": [u"зп", u"зарплата", u"зряплата", u"платят"],
        "type": "info"
    },
    u"как работается в сетелем?": {
        "command": u"Как работается в Сетелем?",
        "previous_commands": [u"разное"],
        "next_commands": [u"Разное", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Приходите и узнаете))"],
        "re": [u"работа", u"сетелем"],
        "type": "info"
    },
    u"какая у меня зарплата?": {
        "command": u"Какая у меня зарплата?",
        "previous_commands": [u"разное"],
        "next_commands": [u"Разное", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Данные по  заработной плате есть в твоём Трудовом договоре. Так же ты всегда можешь уточнить информацию по интересующим тебя выплатам у Специалистов по персоналу твоего Представительства. Кроме этого твой расчётный листок ты можешь получить у своего руководителя. "],
        "re": [u"зп", u"зарплата", u"зряплата"],
        "type": "info"
    },
    u"хотел бы узнать обязанности старшего кредитного эксперта": {
        "command": u"Хотел бы узнать обязанности старшего кредитного эксперта",
        "previous_commands": [u"разное"],
        "next_commands": [u"Разное", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Задай вопрос своему непосредственному руководителю и он обязательно тебе поможет, а нам оставь отзыв - будем очень признательны!"],
        "re": [u"старший", u"обязанности", u"эксперт"],
        "type": "info"
    },
    u"режим работы отдела кадров": {
        "command": u"Режим работы отдела кадров",
        "previous_commands": [u"разное"],
        "next_commands": [u"Разное", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Специалисты по персоналу работают по следующему графику: с понедельника по четверг с 09:00 до 18:00 по местному времени. В пятницу с 09:00 до 16:45 по местному времени. Обед - 45 минут в промежутке с 12:00 до 15:00 часов. Суббота и воскресенье- выходные дни. Контакты специалистов по персоналу твоего региона доступны в разделе 'Информация' в Basis.WFM по ссылке https://basiswfm.cetelem.ru"],
        "re": [u"отдел", u"режим", u"кадр"],
        "type": "info"
    },
    u"сообщить о сложностях в работе": {
        "command": u"Сообщить о сложностях в работе",
        "previous_commands": ["/start"],
        "next_commands": [u"С кем поговорить?", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"У тебя есть предложение по работе или обратная связь? Выбери подходящий пункт внизу."],
        "re": [u"сообщить о сложностях в работе"],
        "type": "info"
    },
    u"оставить предложение/отзыв": {
        "command": u"оставить предложение/отзыв",
        "previous_commands": [u"сообщить о сложностях в работе"],
        "next_commands": [u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Обратись с этим вопросом к Бизнес-партнеру по работе с персоналом (его контакты можно найти в Справочнике банка на корпоративном портале или в разделе 'Информация' в системе Basis WFM). Если тебе не удалось решить свой вопрос через Бизнес-партнера по работе с персоналом, напиши на горячую линию HR_Hotline@cetelem.ru."],
        "re": [u"оставить предложение", u"предложение", u"отзыв"],
        "type": "info"
    },
    u"отзыв о точке": {
        "command": u"Отзыв о точке",
        "previous_commands": ["сообщить о сложностях в работе"],
        "next_commands": ["Отмена"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "false",
        "after_push_command": u"начать заново",
        "after_push_text": u"Твой отзыв принят, благодарю, отзывы о точках очень важны для нас, мы их внимательно рассматриваем и учитываем в работе!",
        "push_cancel": u"отмена",
        "push_cancel_text": u"Операция отменена.",
        "answer_func": "answerPUSH",
        "answer_text": [u"Напиши отзыв о точке в строке сообщения, я внимательно прочитаю и передам информацию нужным коллегам (или напиши слово 'отмена'):"],
        "re": [u"отзыв о точке", u"отзыв"],
        "type": "push"
    },
    u"отзыв о руководителе": {
        "command": u"Отзыв о руководителе",
        "previous_commands": ["сообщить о сложностях в работе"],
        "next_commands": ["Отмена"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "false",
        "after_push_command": u"начать заново",
        "after_push_text": u"Твой отзыв принят, спасибо, отзывы о руководителях особенно важны для нас, мы их внимательно рассматриваем и учитываем в работе!",
        "push_cancel": u"отмена",
        "push_cancel_text": u"Операция отменена.",
        "answer_func": "answerPUSH",
        "answer_text": [u"Напиши отзыв о своем руководителе в строке сообщения, я внимательно прочитаю и передам информацию нужным коллегам (или напиши слово 'отмена'):"],
        "re": [u"отзыв о руководителе", u"отзыв"],
        "type": "push"
    },
    u"мой рабочий график": {
        "command": u"Мой рабочий график",
        "previous_commands": [u"задать вопрос"],
        "next_commands": [u"Во сколько начинается и заканчивается рабочий день", u"Во сколько начинается обед", u"Сколько длится обед", u"Здесь нет моего случая", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Ммммм.... А я круглосуточный =("],
        "re": [u"рабоч", u"день", u"график"],
        "type": "info"
    },
    u"во сколько начинается и заканчивается рабочий день": {
        "command": u"Во сколько начинается и заканчивается рабочий день",
        "previous_commands": [u"мой рабочий график"],
        "next_commands": [u"Мой рабочий график",u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"По графику работы, который ты можешь посмотреть в системе Basis.WFM. Система доступна по ссылке https://basiswfm.cetelem.ru Временный пароль, если что, ты можешь узнать у своего руководителя или специалиста по персоналу."],
        "re": [u"рабочий день", u"заканчивает", u"начинает", u"день", u"рабоч"],
        "type": "info"
    },
    u"во сколько начинается обед": {
        "command": u"Во сколько начинается обед",
        "previous_commands": [u"мой рабочий график"],
        "next_commands": [u"Мой рабочий график",u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Уточни этот вопрос у своего руководителя. А в остальном - приятного аппетита " + u"\U00002668"],
        "re": [u"обед", u"переры"],
        "type": "info"
    },
    u"сколько длится обед": {
        "command": u"Сколько длится обед",
        "previous_commands": [u"мой рабочий график"],
        "next_commands": [u"Мой рабочий график",u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Если ты работаешь от 1 до 4-х часов в день, то 30 минут. Если работаешь больше 4-х часов, то 1 час " + u"\U0001F550"],
        "re": [u"обед", u"переры"],
        "type": "info"
    },
    u"конфликты с руководством": {
        "command": u"Конфликты с руководством",
        "previous_commands": [u"задать вопрос"],
        "next_commands": [u"С кем поговорить?", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Обижает руководство? Оставь отзыв, а мы посмотрим, что к чему " + u"\U0001F60A"],
        "re": [u"обиж", u"обид", u"руковод", u"проблем", u"дебил", u"дурак", u"мудак", u"редиска", u"орет", u"идиот", u"сволоч", u"кретин", u"сука"],
        "type": "info"
    },
    u"с кем поговорить?": {
        "command": u"С кем поговорить?",
        "previous_commands": [u"Конфликты с руководством"],
        "next_commands": [u"Конфликты с руководством", u"Начать заново"],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "true",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Обратись с этим вопросом к Бизнес-партнеру по работе с персоналом (его контакты можно найти в Справочнике банка на корпоративном портале или в разделе 'Информация' в системе Basis WFM). Если тебе не удалось решить свой вопрос через Бизнес-партнера по работе с персоналом, напиши на горячую линию HR_Hotline@cetelem.ru."],
        "re": [u"обиж", u"обид", u"руковод", u"проблем", u"дебил", u"дурак", u"мудак", u"редиска", u"орет", u"идиот", u"сволоч", u"кретин", u"сука"],
        "type": "info"
    },
    u"помощь": {
        "command": u"Помощь",
        "previous_commands": ["*"],
        "next_commands": [],
        "repeat_last_command_text": "true",
        "repeat_last_command_next_commands": "true",
        "repeatable_text": "false",
        "repeatable_next_commands": "false",
        "answer_func": "answerEMPTY",
        "answer_text": [u"Чтобы получить интересующую информацию воспользуйся меню внизу экрана или напиши вопрос в строке сообщения. Если на какой-то вопрос я не смогу ответить, то попробуй задать его снова через день, возможно, я уже буду знать на него ответ. Чтобы попасть в меню нажми на /start."],
        "re": [u"помощь"],
        "type": "info"
    },
    "/unknown": {
        "command": "/unknown",
        "previous_commands": ["*"],
        "next_commands": [u"Помощь"],
        "repeat_last_command_text": "true",
        "repeat_last_command_next_commands": "true",
        "repeatable_text": "false",
        "repeatable_next_commands": "false",
        "answer_func": "answerUNKNOWN",
        "answer_text": [u"Видимо у меня есть ещё не вся информация о работе в Сетелем, но я обязательно узнаю то, что тебе нужно, и смогу ответить позже. Напиши мне завтра."],
        "re": [],
        "transit_to": "{GOBACK}",
        "type": "transit"
    },
    "/event": {
        "command": "/event",
        "previous_commands": ["*"],
        "next_commands": [],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "false",
        "repeatable_next_commands": "false",
        "answer_func": "answerEVENT",
        "answer_text": [""],
        "re": ['/event'],
        "transit_to": "",
        "type": "info"
    },
    "/similar": {
        "command": "/similar",
        "previous_commands": ["*"],
        "next_commands": [""],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_text": [u"Ой, я не совсем понял, что ты спросил. Пожалуйста, выбери нужный пункт из списка внизу."],
        "answer_func": "answerSIMILAR",
        "re": [],
        "type": "info"
    },
    "/picture": {
        "command": "/picture",
        "previous_commands": ["*"],
        "next_commands": [""],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_text": [u"Спасибо за картинку, обязательно посмотрю его позже."],
        "answer_func": "answerPICTURE",
        "re": [],
        "type": "picture"
    },
    "/sound": {
        "command": "/sound",
        "previous_commands": ["*"],
        "next_commands": [""],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_text": [u"Спасибо за звуковой файл, обязательно послушаю его позже."],
        "answer_func": "answerSOUND",
        "re": [],
        "type": "sound"
    },
    "/video": {
        "command": "/video",
        "previous_commands": ["*"],
        "next_commands": [""],
        "repeat_last_command_text": "false",
        "repeat_last_command_next_commands": "false",
        "repeatable_text": "true",
        "repeatable_next_commands": "true",
        "answer_text": [u"Видео? Мне? Спасибо, обязательно посмотрю его позже."],
        "answer_func": "answerMOVIE",
        "re": [],
        "type": "video"
    }
}

# Профили знаний ботов
BOT_KNOWLEDGE_PROFILES = {
    "adopt" : {
        "syntax" : MESSAGE_MAP_ADOPT,
        "semantics" : {},
        "command_unknown" : u"/unknown",
        "command_similarity" : u"/similar",
        "command_picture" : u"/picture",
        "command_sound" : u"/sound",
        "command_video" : u"/video",
        "command_start" : u"/start",
        "command_event" : u"/event",
        "command_help" : u"Помощь"
    },
    "adoptrkz" : {
        "syntax" : MESSAGE_MAP_ADOPT_RKZ,
        "semantics" : {},
        "command_unknown" : u"/unknown",
        "command_similarity" : u"/similar",
        "command_picture" : u"/picture",
        "command_sound" : u"/sound",
        "command_video" : u"/video",
        "command_start" : u"/start",
        "command_event" : u"/event",
        "command_help" : u"Помощь"
    }
}

# Возвращает список всех доступных ботов
def getAllBotAPITokens():
    all_bot_api_tokens = []
    for bot_api_token in BOT_CONFIGS:
        all_bot_api_tokens = all_bot_api_tokens + [bot_api_token]
    return all_bot_api_tokens
    
# Возвращает конфиг конкретного бота
def getBotConfigByAPIToken(bot_api_token):
    return BOT_CONFIGS[bot_api_token]

# Возвращает все имена существующих профилей знаний
def getAllBotKnowledgeProfileNames():
    bot_knowledge_profile_names = []
    for bot_knowledge_profile_name in BOT_KNOWLEDGE_PROFILES:
        bot_knowledge_profile_names = bot_knowledge_profile_names + [bot_knowledge_profile_name]
    return bot_knowledge_profile_names

# Возвращает конкретный профиль знаний по его имени
def getBotKnowledgeProfile(bot_knowledge_profile_name):
    return BOT_KNOWLEDGE_PROFILES[bot_knowledge_profile_name]

# Подготовка семантики ботов    
def initKnowledgeProfilesSemantics():
    # Заполним BOT_SEMANTICS - семантику чат-бота
    for bot_knowledge_profile_name in BOT_KNOWLEDGE_PROFILES:
        try:
            for command in BOT_KNOWLEDGE_PROFILES[bot_knowledge_profile_name]['syntax']:
                for re_xp in (BOT_KNOWLEDGE_PROFILES[bot_knowledge_profile_name]['syntax'][command]['re'] + [BOT_KNOWLEDGE_PROFILES[bot_knowledge_profile_name]['syntax'][command]['command']]):
                    try:
                        BOT_KNOWLEDGE_PROFILES[bot_knowledge_profile_name]['semantics'][re_xp]
                    except Exception:
                        BOT_KNOWLEDGE_PROFILES[bot_knowledge_profile_name]['semantics'][re_xp] = []
                    if BOT_KNOWLEDGE_PROFILES[bot_knowledge_profile_name]['syntax'][command]['command'] not in BOT_KNOWLEDGE_PROFILES[bot_knowledge_profile_name]['semantics'][re_xp]:
                        BOT_KNOWLEDGE_PROFILES[bot_knowledge_profile_name]['semantics'][re_xp] = BOT_KNOWLEDGE_PROFILES[bot_knowledge_profile_name]['semantics'][re_xp] + [BOT_KNOWLEDGE_PROFILES[bot_knowledge_profile_name]['syntax'][command]['command']]
        except Exception as exc:
            exc_type, exc_obj, tb = sys.exc_info()
            app_log.appendLog(u"*** Exception caught during semantics creation: " + str(exc) + ", line " + str(tb.tb_lineno))

def initModel():
    # Создаем семантику чат ботов
    initKnowledgeProfilesSemantics()


# Инициализация модели
initModel()
