from enum import Enum


class MessageTypes(Enum):
    TEXT = 'text'
    AUDIO = 'audio'
    IMAGE = 'image'
    STICKER = 'sticker'
    TEXTS = 'texts'


class MessageBatchRequest:
    def __init__(self, generalParseMode = None):
        self.messages = []
        self.parseMode = generalParseMode

    def add(self, messageType = MessageTypes.TEXT, content = None):
        if content not in [None, {None: True}]:
            self.messages.append(
                {
                    'message#{}'.format(len(self.messages)): {'type':messageType, 'content':content}
                }
            )
        else:
            print('CONTENT IS NONE')

    def shift(self, messageType = MessageTypes.TEXT, content = None):
        if content not in [None, {None: True}]:
            self.messages = \
                [{'message#{}'.format(len(self.messages)): {'type':messageType, 'content':content}}] \
                + self.messages


    def addText(self, message, parseMode = None):
        if self.parseMode is not None and parseMode is None:
            parseMode = self.parseMode

        elif parseMode is None:
            parseMode = 'HTML'

        self.add(MessageTypes.TEXT, {'message': message, 'parsemode': parseMode})

    def addTexts(self, messages, parseMode='HTML'):
        if self.parseMode is not None and parseMode is None:
            parseMode = self.parseMode

        elif parseMode is None:
            parseMode = 'HTML'

        self.add(MessageTypes.TEXTS, {'messages': messages, 'parsemode': parseMode})

    def addImage(self, path, caption):
        self.add(MessageTypes.IMAGE, {'path': path, 'caption': caption})

    def addAudio(self, audio, caption=None, duration=None, performer=None, title=None,
                  disable_notification=None):
        self.add(MessageTypes.AUDIO, {'audio': audio, 'caption': caption, 'duration': duration, 'performer': performer,
                                      'title': title, 'disable_notification': disable_notification})

    def addSticker(self, stickerid):
        self.add(MessageTypes.STICKER, {'stickerid': stickerid})

    def shiftText(self, message, parseMode = None):
        if self.parseMode is not None and parseMode is None:
            parseMode = self.parseMode

        elif parseMode is None:
            parseMode = 'HTML'
        self.shift(MessageTypes.TEXT, {'message': message, 'parsemode': parseMode})

    def shiftTexts(self, messages, parseMode=None):
        if self.parseMode is not None and parseMode is None:
            parseMode = self.parseMode

        elif parseMode is None:
            parseMode = 'HTML'
        self.shift(MessageTypes.TEXTS, {'messages': messages, 'parsemode': parseMode})

    def shiftImage(self, path, caption):
        self.shift(MessageTypes.IMAGE, {'path': path, 'caption': caption})

    def shiftAudio(self, audio, caption=None, duration=None, performer=None, title=None,
                  disable_notification=None):
        self.shift(MessageTypes.AUDIO, {'audio': audio, 'caption': caption, 'duration': duration, 'performer': performer,
                                      'title': title, 'disable_notification': disable_notification})
    def shiftSticker(self, stickerid):
        self.add(MessageTypes.STICKER, {'stickerid': stickerid})

    def __add__(self, other):
        print('SELF: {}'.format(self.messages))
        print('OTHER: {}'.format(other.messages))

        if isinstance(other, MessageBatchRequest):
            print('is instance!')
            batch = self.messages + other.messages
        else:
            batch = self.messages

        print('BATCH: {}'.format(batch))

        mrb = MessageBatchRequest()
        mrb.messages = batch
        return mrb