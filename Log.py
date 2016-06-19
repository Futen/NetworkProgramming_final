import json
import os
import numpy as np

F_NAME = 'LogData.npy'
if os.path.isfile(F_NAME):
    LogData = list(np.load(F_NAME))
else:
    LogData = []

def NewLogBag():
    a = dict({'who_1':'', 'who_2':'', 'data':[]})
    return a
def NewMessageBag():
    a = dict({'from':'', 'to':'', 'message':''})
    return a
def CreateLog(account1, account2):
    if account1 == account2:
        print 'Create Fail'
        return None
    log = NewLogBag()
    log['who_1'] = account1
    log['who_2'] = account2
    LogData.append(log)
    return log
def FindLog(account1, account2):
    for log in LogData:
        if (log['who_1'] == account1 or log['who_2'] == account1) and \
           (log['who_1'] == account2 or log['who_2'] == account2) and account1 != account2:
            return log
    return None
def SaveLog():
    np.save(F_NAME, LogData)

def CreateMessage(From, To, Message):
    log = FindLog(From, To)
    if log is None:
        log = CreateLog(From, To)
    Msg = NewMessageBag()
    Msg['from'] = From
    Msg['to'] = To
    Msg['message'] = Message
    log['data'] = list(log['data'])
    log['data'].append(Msg)
    SaveLog()
    return True
def GetMessageData(account1, account2):
    log = FindLog(account1, account2)
    if log is None:
        return []
    else:
        return log['data']

