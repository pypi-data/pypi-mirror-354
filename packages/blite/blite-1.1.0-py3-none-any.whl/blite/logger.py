import time

class LogLevel:
    NO_LOG = 0
    CONCISE = 1
    VERBOSE = 2

class Logger:
    def __init__(self):
        pass

    @staticmethod
    def reportSuccess(text):
        now = time.localtime()
        print(f'[*] {now.tm_year}-{now.tm_mon}-{now.tm_mday} {now.tm_hour}:{now.tm_min}:{now.tm_sec} {text}')

    @staticmethod
    def reportFailure(text):
        now = time.localtime()
        print(f'[X] {now.tm_year}-{now.tm_mon}-{now.tm_mday} {now.tm_hour}:{now.tm_min}:{now.tm_sec} {text}')

    @staticmethod
    def report(text):
        now = time.localtime()
        print(f'[-] {now.tm_year}-{now.tm_mon}-{now.tm_mday} {now.tm_hour}:{now.tm_min}:{now.tm_sec} {text}')