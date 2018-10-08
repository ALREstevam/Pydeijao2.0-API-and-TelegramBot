import json

configFilePath = 'config.json'
file = open(configFilePath)
data = json.load(file)
telegram_bot_token = data['telegramBotToken']
file.close()

