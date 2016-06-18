import json
import time
import os
import Parameter as Pm

def ReadUserData():
    f = open('UserData.json', 'r')
    data = json.load(f)
    f.close()
    return data

LoginLst = []
OnlineLst = []
OfflineLst = []
BusyLst = []
if os.path.isfile('UserData.json'):
    UserData = ReadUserData()
else:
    UserData = {}

test_time = time.time()
test_account1 = dict({'account':'fulton84717', 'password':'pig6983152', 'nickname':'Futen',
    'last_login_time':test_time, 'register_time':test_time, 'friend_request':[], 'friend_lst':['Futen']})
test_account2 = dict({'account':'Futen', 'password':'pig6983152', 'nickname':'Fulton',
    'last_login_time':test_time, 'register_time':test_time, 'friend_request':[], 'friend_lst':['fulton84717']})
test_data = dict({
                'fulton84717': test_account1,
                'Futen': test_account2
                })
def NewBag():
    a = dict({'account':'', 'password':'', 'nickname':'', 'last_login_time':test_time, 
        'register_time':test_time, 'friend_request':[], 'birthday':'', 'frien_lst':[]
        })
    return a
def CreateAccount(data):
    if not data['account'] in UserData:
        now_time = time.time()
        UserData[data['account']] = NewBag()
        UserData[data['account']]['account'] = data['account']
        UserData[data['account']]['password'] = data['password']
        #UserData[data['account']]['nickname'] = data['nickname']
        UserData[data['account']]['last_login_time'] = now_time
        UserData[data['account']]['register_time'] = now_time
        return True
    else:
        return False
def ModifyAccount(dataIn):
    if not dataIn['account'] in UserData:
        return False
    else:
        account = dataIn['account']
        if 'password' in dataIn:
            UserData[account]['password'] = dataIn['password']
        if 'nickname' in dataIn:
            UserData[account]['nickname'] = dataIn['nickname']
        if 'birthday' in dataIn:
            UserData[account]['birthday'] = dataIn['birthday']
        return True
def DeleteAccount(dataIn):
    if dataIn['account'] in UserData:
        UserData.pop(dataIn['account'], None)
        return True
    else:
        return False
def FriendRequest(dataIn):
    if dataIn['account'] in UserData and dataIn['to'] in UserData:
        if dataIn['account'] in UserData[dataIn['to']]['friend_request'] or dataIn['account'] in UserData[dataIn['to']]['friend_lst']:
            return False
        UserData[dataIn['to']]['friend_request'].append(dataIn['account'])
        return True
    else:
        return False
def FriendRequestPacket(dataIn):
    data = {}
    data['command'] = Pm.FRIENDREQUESTSHOW
    data['account'] = dataIn['to']
    data['from'] = dataIn['account']
    return json.dumps(data)
def AcceptFriendRequest(dataIn):
    if dataIn['account'] in UserData and dataIn['to'] in UserData:
        if dataIn['to'] in UserData[dataIn['account']]['friend_request']:
            UserData[dataIn['account']]['friend_request'].remove(dataIn['to'])
            UserData[dataIn['account']]['friend_lst'].append(dataIn['to'])
            UserData[dataIn['to']]['friend_lst'].append(dataIn['account'])
            return True
        return False
    else:
        return False
def RejectFriendRequest(dataIn):
    if dataIn['account'] in UserData and dataIn['to'] in UserData:
        UserData[dataIn['account']]['friend_request'].remove(dataIn['to'])
        return True
    else:
        return False
def RemoveFriend(dataIn):
    if dataIn['account'] in UserData and dataIn['to'] in UserData:
        if dataIn['to'] in UserData[dataIn['account']]['friend_lst']:
            UserData[dataIn['account']]['friend_lst'].remove(dataIn['to'])
            UserData[dataIn['to']]['friend_lst'].remove(dataIn['account'])
            return True
    return False
def GetFriendRequest(dataIn):
    if dataIn['account'] in UserData:
        tmp = UserData[dataIn['account']]['friend_request']
        out = []
        for one in tmp:
            if one in UserData:
                out.append(one)
            else:
                tmp.remove(one)
        return out
    else:
        return None
def UserLogin(dataIn):
    now_time = time.time()
    #if not dataIn['account'] in LoginLst and dataIn['account'] in UserData:
    if dataIn['account'] in UserData:
        if UserData[dataIn['account']]['password'] == dataIn['password']:
            if not dataIn['account'] in LoginLst:
                LoginLst.append(dataIn['account'])
            if not dataIn['account'] in OnlineLst:
                OnlineLst.append(dataIn['account'])
            UserData[dataIn['account']]['last_login_time'] = now_time
            return True
    return False
def UserLogout(dataIn):
    if dataIn['account'] in LoginLst:
        if dataIn['account'] in OnlineLst:
            OnlineLst.remove(dataIn['account'])
        if dataIn['account'] in BusyLst:
            BusyLst.remove(dataIn['account'])
        if dataIn['account'] in OfflineLst:
            OfflineLst.remove(dataIn['account'])
        LoginLst.remove(dataIn['account'])
        return True
    else:
        return False
def SearchUser(dataIn):
    if dataIn['who'] in UserData:
        return True
    else:
        return False
def ChangeState(dataIn):
    if dataIn['account'] in OnlineLst:
        OnlineLst.remove(dataIn['account'])
    if dataIn['account'] in BusyLst:
        BusyLst.remove(dataIn['account'])
    if dataIn['account'] in OfflineLst:
        OfflineLst.remove(dataIn['account'])
    if dataIn['state'] == 'online':
        OnlineLst.append(dataIn['account'])
    elif dataIn['state'] == 'busy':
        BusyLst.append(dataIn['account'])
    elif dataIn['state'] == 'offline':
        OfflineLst.append(dataIn['account'])
    else:
        return False
    return True
def SaveUserData():
    f = open('UserData.json', 'w')
    f.write(json.dumps(UserData, indent = 4))
    f.close()


if __name__ == '__main__':
    a = dict({'a':[1,2,3,4], 'b':0})
    f = open('gg.txt','w')
    f.write(json.dumps(a, indent=4))
    f.close()











