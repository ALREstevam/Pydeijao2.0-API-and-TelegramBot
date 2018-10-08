#import MyTelegramBot.BotInit as bot
import Api.BandecoApi as api

import multiprocessing
import time

def add():
    while True:
        print('1')
        time.sleep(3)


def sud():
    while True:
        print('0')
        time.sleep(3)


if __name__ == '__main__':
    p1 = multiprocessing.Process(name='p1', target=add)
    p2 = multiprocessing.Process(name='p2', target=sud)

    p1.start()
    p2.start()