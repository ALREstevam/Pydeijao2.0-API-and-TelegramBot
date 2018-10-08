import telepot
from telepot.loop import MessageLoop
from MyTelegramBot.MessageBatchRequest import MessageBatchRequest,MessageTypes

class GeneralTelegramBotWrapper:
    def __init__(self, botToken):
        try:
            self.wrBot = telepot.Bot(botToken)
            self.wrBot.getMe()
            self.botName = self.wrBot.getMe()['first_name']
            self.botUserName = self.wrBot.getMe()['username']
        except:
            print('Bot não foi criado')
            exit(-1)

    def sendText(self, chatId, message, parseMode='HTML'):
        self.wrBot.sendChatAction(chatId, 'typing')
        self.wrBot.sendMessage(chatId, message, parse_mode=parseMode)

    def setTalkHandleFunction(self, handle):
        MessageLoop(self.wrBot, handle).run_as_thread()

    def sendSticker(self, chatid, stickerid):
        self.wrBot.sendChatAction(chatid, 'typing')
        self.wrBot.sendSticker(chatid, stickerid)
        pass

    def sendAudio(self, chatId, audio, caption=None, duration=None, performer=None, title=None,
                  disable_notification=None):
        self.wrBot.sendChatAction(chatId, 'upload_audio')
        self.wrBot.sendAudio(chatId, audio, caption, duration, performer, title, disable_notification)

    def sendPic(self, chatId, path, caption):
        self.wrBot.sendChatAction(chatId, 'upload_photo')
        self.wrBot.sendPhoto(chatId, path, caption)

    def sendStartMessage(self, chatId, message):
        self.sendText(chatId, message)

    def glanceMsg(self, msg):
        msgType = telepot.glance(msg)[0]

        txt = ''
        if msgType == 'sticker':
            txt = msg['sticker']['emoji']
        elif msgType == 'text':
            txt = msg['text']

        lname = ''
        if 'last_name' in msg['from']:
            lname = msg['from']['last_name']

        return {
            'fullname': msg['from']['first_name'] + ' ' + lname,
            'first_name': msg['from']['first_name'],
            'last_name': lname,
            'chat_id': msg['chat']['id'],
            'lang': msg['from']['language_code'],
            'txt': txt,
            'msgType': msgType
        }

    def sendMessages(self, chatid, messages, parseMode='HTML'):
        for msg in messages:
            self.sendText(chatid, msg, parseMode)

    def runBatch(self, chatId, batch):
        for message in batch.messages:
            for messageName, messageContent in message.items():
                print('Running message : {}'.format(messageName))

                try:
                    if messageContent['type'] == MessageTypes.TEXT:
                        self.sendText(chatId, messageContent['content']['message'], messageContent['content']['parsemode'])

                    elif messageContent['type'] == MessageTypes.TEXTS:
                        self.sendMessages(chatId, messageContent['content']['messages'], messageContent['content']['parsemode'])

                    elif messageContent['type'] == MessageTypes.AUDIO:
                        self.sendAudio(chatId, messageContent['content']['audio'], messageContent['content']['caption'],
                                     messageContent['content']['duration'], messageContent['content']['performer'],
                                     messageContent['content']['title'], messageContent['content']['disable_notification'])

                    elif messageContent['type'] == MessageTypes.STICKER:
                        self.sendSticker(chatId, messageContent['content']['stickerid'])

                    elif messageContent['type'] == MessageTypes.IMAGE:
                        self.sendPic(chatId, messageContent['content']['path'], messageContent['content']['caption'])
                except Exception as ex:
                    print('AN EXCEPTION OCCURRED')
                    print(ex)