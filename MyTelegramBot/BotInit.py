print('STARTING')
from MyTelegramBot.MyBot import MyBot
import MyTelegramBot.BotConfig as cnfg
from pprint import pprint, pformat
import re
import telepot
import traceback
import urllib3
import os
import urllib.request, json
import re
import MyTelegramBot.foodWord2emoji as wrd2em
import random
from MyTelegramBot.MessageBatchRequest import MessageBatchRequest as MsgBatchReq

#🍳 cozinhando
#🍲 comida ️🍴🍽🥄


bot = MyBot(cnfg.telegram_bot_token)
apiurl = 'http://127.0.0.1:5000/menu'

def make_name(name):
    return wrd2em.emojisAtBegin(name)

def extractRegisters(register, name):
    panicStickers = [
        'CAADAgADRwEAAksODwABHo4oVpiDstwC',
        'CAADAQADQgADIgjlA6G-CJlr2AGiAg',
        'CAADBAADaAMAAnMaRAV2eMJIkuqvAAEC',
        'CAADAQADfgADNKqECFOlBqo-pCJsAg',
        'CAADBAADjgQAAsY_ZAXYtRq7wVB7bgI',
        'CAADBAADyAQAAsY_ZAUTz1LJGDLbggI',

    ]

    tempFoods = ''
    batch = MsgBatchReq()

    tempFoods += '*{}*\n\n'.format(make_name(name.upper()))
    goodToGo = False

    for foodTouple in register:

        print(foodTouple)

        if foodTouple[0].lower() == 'Observações'.lower():
            tempFoods += '\n⚠_{}_ : _{}_\n'.format(foodTouple[0].upper(), foodTouple[1].lower().capitalize())

        elif foodTouple[0].lower() == '#no_food#'.lower():
            goodToGo = False
            batch.addSticker(random.choice(panicStickers))
            tempFoods += '\n❌ *{}* ❌'.format(foodTouple[1].upper())

        else:
            goodToGo = True
            foodTouple[0] = re.sub(r'food#\d*#[A-Za-zá-úÁ-Ú _]*', 'PRATO', foodTouple[0])
            tempFoods += '• *[{}]*\t{} {}\n'.format(foodTouple[0].upper(),
                                                   foodTouple[1].lower().capitalize(), ''.join(wrd2em.emojisFor(foodTouple[0] + ' ' + foodTouple[1])))

    if goodToGo:
        batch.shiftSticker('CAADBAADjgADQKtRAfOAKcb4Ej2zAg')

    batch.addText(tempFoods, 'markdown')
    return batch


def talkFunction(msg):
    chatId = msg['chat']['id']

    try:
        pprint(msg)
        msgType = telepot.glance(msg)[0]
        print(msgType)

        if msgType not in ['text', 'sticker']:
            bot.sendTip(chatId, 'Me envie apenas textos.')
            return
        data = bot.glanceMsg(msg)

        if data['txt'] == '/help':
            bot.sendMessages(chatId,
                             [
                                 '<b>Você pode usar os seguintes comandos:</b>\n'
                                 '/help - mostrar a lista de comandos\n'
                                 '/cardapio ou /card ou /menu para mostrar o cardápio completo do dia de hoje\n'
                                 '/alm ou /almoco - Mostra o cardápio do almoço de hoje\n'
                                 '/almoco_veg ou /almveg - Mostra o cardápio do almoço vegetariano de hoje\n'
                                 '/janta ou /jnt - Mostra o cardápio do jantar de hoje\n'
                                 '/janta_veg ou /jntveg - Mostra o cardápio do jantar vegetariano de hoje\n'
                                 '/alm_comp - Mostra o cardápio do almoço completo de hoje\n'
                                 '/jnt_comp - Mostra o cardápio do jantar completo de hoje\n'
                                 '/json - (debug) mostra as informações vindas da API em JSON\n'

                             ]
                             )

        elif data['txt'] == '/start':
            bot.sendMessages(chatId,
                             [
                                'Olá, este bot é capaz de lhe trazer o cardápio do restaurante universitário (vulgo bandeijão) da Faculdade de Tecnologia da Unicamp',
                                '*Você pode usar os seguintes comandos:*\n\n'
                                '/help - mostrar a lista de comandos\n'
                                '/cardapio ou /card ou /menu para mostrar o cardápio completo do dia de hoje\n'
                                '/alm ou /almoco - Mostra o cardápio do almoço de hoje\n'
                                '/almoco_veg ou /almveg - Mostra o cardápio do almoço vegetariano de hoje\n'
                                '/janta ou /jnt - Mostra o cardápio do jantar de hoje\n'
                                '/janta_veg ou /jntveg - Mostra o cardápio do jantar vegetariano de hoje\n'
                                '/alm_comp - Mostra o cardápio do almoço completo de hoje\n'
                                '/jnt_comp - Mostra o cardápio do jantar completo de hoje\n'
                                '/json - (debug) mostra as informações vindas da API em JSON\n']
                             )


        elif data['txt'] in ['/cardapio', '/menu', '/card', '/cardápio', '/bands', '/bandeco']:
            with urllib.request.urlopen(apiurl) as url:
                data = json.loads(url.read().decode())

                batch = MsgBatchReq(generalParseMode='markdown')
                batch.addText('*🍽{}🍽\n{} - {}*'.format(data['title'].upper(), data['date'], data['weekDay'].upper()))

                for name, register in data['foodRegister'].items():
                    batch = batch + extractRegisters(register, name)
                bot.runBatch(chatId, batch)
        elif data['txt'] in ['/alm', '/almoço', '/almoco']:
            with urllib.request.urlopen(apiurl) as url:
                data = json.loads(url.read().decode())

                batch = MsgBatchReq(generalParseMode='markdown')
                batch.addText('*🍽{}🍽\n{} - {}*'.format(data['title'].upper(), data['date'], data['weekDay'].upper()))

                print(batch.messages)

                batch = batch + extractRegisters(data['foodRegister']['Almoço'], 'ALMOÇO')

                print(batch.messages)

                bot.runBatch(chatId, batch)

        elif data['txt'] in ['/almoco_veg', '/almoço_veg', '/almveg']:
            with urllib.request.urlopen(apiurl) as url:
                data = json.loads(url.read().decode())

                batch = MsgBatchReq(generalParseMode='markdown')
                batch.addText('*🍽{}🍽\n{} - {}*'.format(data['title'].upper(), data['date'], data['weekDay'].upper()))

                batch = batch + extractRegisters(data['foodRegister']['Almoço Vegetariano'], 'Almoço Vegetariano')
                bot.runBatch(chatId, batch)


        elif data['txt'] in ['/janta', '/jnt']:
            with urllib.request.urlopen(apiurl) as url:
                data = json.loads(url.read().decode())

                batch = MsgBatchReq(generalParseMode='markdown')
                batch.addText('*🍽{}🍽\n{} - {}*'.format(data['title'].upper(), data['date'], data['weekDay'].upper()))

                batch = batch + extractRegisters(data['foodRegister']['Jantar'], 'Jantar')
                bot.runBatch(chatId, batch)

        elif data['txt'] in ['/janta_veg', '/jntveg']:
            with urllib.request.urlopen(apiurl) as url:
                data = json.loads(url.read().decode())

                batch = MsgBatchReq(generalParseMode='markdown')
                batch.addText('*🍽{}🍽\n{} - {}*'.format(data['title'].upper(), data['date'], data['weekDay'].upper()))

                batch = batch + extractRegisters(data['foodRegister']['Jantar Vegetariano'], 'Jantar Vegetariano')
                bot.runBatch(chatId, batch)


        elif data['txt'] in ['/alm_comp']:
            with urllib.request.urlopen(apiurl) as url:
                data = json.loads(url.read().decode())

                batch = MsgBatchReq(generalParseMode='markdown')
                batch.addText('*🍽{}🍽\n{} - {}*'.format(data['title'].upper(), data['date'], data['weekDay'].upper()))

                batch = batch + extractRegisters(data['foodRegister']['Almoço'], 'Almoço')
                batch = batch + extractRegisters(data['foodRegister']['Almoço Vegetariano'], 'Almoço Vegetariano')
                bot.runBatch(chatId, batch)

        elif data['txt'] in ['/jnt_comp']:
            with urllib.request.urlopen(apiurl) as url:
                data = json.loads(url.read().decode())

                batch = MsgBatchReq(generalParseMode='markdown')
                batch.addText('*🍽{}🍽\n{} - {}*'.format(data['title'].upper(), data['date'], data['weekDay'].upper()))

                batch = batch + extractRegisters(data['foodRegister']['Jantar'], 'Jantar')
                batch = batch + extractRegisters(data['foodRegister']['Jantar Vegetariano'], 'Jantar Vegetariano')
                bot.runBatch(chatId, batch)
        elif data['txt'] == '/json':
            with urllib.request.urlopen(apiurl) as url:
                data = json.loads(url.read().decode())
                bot.sendText(chatId, pformat(data))

        else:
            bot.sendSticker(chatId, 'CAADAQADcQADSZfpBsSwuIaA-d5aAg')
            bot.sendText(chatId, 'Não entendi a mensagem.')




    except urllib3.exceptions.ReadTimeoutError:
        bot.sendErrorMsg(chatId, 'Um erro ocorreu durante a obtenção dos dados.')
        traceback.print_exc()
        bot.sendSticker(chatId, 'CAADBAADGgMAAnMaRAVVEiMGXFjhEQI')

    except Exception as ex:
        bot.sendErrorMsg(chatId, 'Algo deu errado, tente novamente.')
        traceback.print_exc()
        bot.sendSticker(chatId, 'CAADBAAD0wEAAnMaRAVCtzF6SHO6dwI')


bot.setTalkHandleFunction(talkFunction)
print('ONLINE')


def run():
    while True:
        command = input('>> ')

        if command == 'exit':
            exit()

run()




