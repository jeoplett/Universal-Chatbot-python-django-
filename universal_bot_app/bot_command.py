# coding: utf8

from . import models


# Возвращает все имена существующих профилей знаний
def getAllBotKnowledgeProfileNames():
    return models.getAllBotKnowledgeProfileNames()

# Возвращает конкретный профиль знаний по его имени
def getBotKnowledgeProfile(bot_knowledge_profile_name):
    return models.getBotKnowledgeProfile(bot_knowledge_profile_name)

def getBotStartCommand(unified_message):
    bot_knowledge_profile = models.getBotKnowledgeProfile(unified_message['bot_config']['knowledge_profile'])
    return bot_knowledge_profile['command_start']

def getBotHelpCommand(unified_message):
    bot_knowledge_profile = models.getBotKnowledgeProfile(unified_message['bot_config']['knowledge_profile'])
    return bot_knowledge_profile['command_help']

def getBotUnknownCommand(unified_message):
    bot_knowledge_profile = models.getBotKnowledgeProfile(unified_message['bot_config']['knowledge_profile'])
    return bot_knowledge_profile['command_unknown']

def getBotSimilarityCommand(unified_message):
    bot_knowledge_profile = models.getBotKnowledgeProfile(unified_message['bot_config']['knowledge_profile'])
    return bot_knowledge_profile['command_similarity']

def getBotTriggerByBotCommand(unified_message, bot_command):
    bot_knowledge_profile = models.getBotKnowledgeProfile(unified_message['bot_config']['knowledge_profile'])
    return bot_knowledge_profile['syntax'].get(bot_command)

def getBotEventCommand(unified_message):
    bot_knowledge_profile = models.getBotKnowledgeProfile(unified_message['bot_config']['knowledge_profile'])
    return bot_knowledge_profile['command_event']

def getBotSemantics(unified_message):
    bot_knowledge_profile = models.getBotKnowledgeProfile(unified_message['bot_config']['knowledge_profile'])
    return bot_knowledge_profile['semantics']
    