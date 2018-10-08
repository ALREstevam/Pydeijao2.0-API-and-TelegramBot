from MyTelegramBot.GeneralTelegramBot import GeneralTelegramBotWrapper

class MyBot (GeneralTelegramBotWrapper):
    def __init__(self, botToken):
        super().__init__(botToken)
        self.emojis = {'search': '🔍🤔', 'happy': '🙂', 'sad': '☹', 'tip': '😉', 'error': '❌😭'}

    def sendSearchMsg(self, chatid, msg):
        return self.sendText(chatid, '{} {}'.format(self.emojis['search'], msg))

    def sendErrorMsg(self, chatid, msg):
        return self.sendText(chatid, '{} {} '.format(self.emojis['error'], msg))

    def sendLinkMsg(self, chatid, msg, url):
        return self.sendText(chatid, '{}\n🔗: {}'.format(msg, url))

    def sendSadMsg(self, chatid, msg):
        return self.sendText(chatid, '{} {}'.format(self.emojis['sad'], msg))

    def sendHappyMsg(self, chatid, msg):
        return self.sendText(chatid, '{} {}'.format(self.emojis['happy'], msg))

    def sendTip(self, chatid, msg):
        return self.sendText(chatid, '{} {}'.format(self.emojis['tip'], msg))



