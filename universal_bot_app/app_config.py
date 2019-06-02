# coding: utf8 

APP_CONFIG = {
    "name" : "universal_bot_app"
}

__STAT_SERVICE_URL__ = "http://sdo.cetelem.ru/cetelem/cgi-bin/bp0026_chat_bot_update.html"

__SYSTEM_API_TOKEN__ = "jdp9843hdoiew7roft8pdq[19j32dpq3jdxpq83hpodh43p9"

def getAppConfig():
    return APP_CONFIG
    
def getStatServiceURL():
    return __STAT_SERVICE_URL__

def getSystemAPIToken():
    return __SYSTEM_API_TOKEN__