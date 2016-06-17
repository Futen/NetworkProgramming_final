import json
import time

LoginLst = []
UserData = {}
ttt = 0

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
    a = dict({'account':'', 'password':'', 'nickname':'', 'last_login_time':test_time, 'register_time':test_time, 'friend_request':[],
              'frien_lst':[]
        })
    return a
def CreateAccount(data):
    if not data['account'] in UserData:
        now_time = time.time()
        UserData[data['account']] = NewBag()
        UserData[data['account']]['account'] = data['account']
        UserData[data['account']]['password'] = data['password']
        UserData[data['account']]['nickname'] = data['nickname']
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
        UserData[account]['password'] = dataIn['password']
        UserData[account]['nickname'] = dataIn['nickname']
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
def AcceptFriendRequest(dataIn):
    if dataIn['account'] in UserData and dataIn['to'] in UserData:
        if dataIn['to'] in UserData[dataIn['account']]['friend_request']:
            UserData[dataIn['account']]['friend_request'].pop(dataIn['to'], None)
            UserData[dataIn['account']]['friend_lst'].append(dataIn['to'])
            UserData[dataIn['to']]['friend_lst'].append(dataIn['account'])
            return True
        return False
    else:
        return False
def RejectFriendRequest(dataIn):
    if dataIn['account'] in UserData and dataIn['to'] in UserData:
        UserData[dataIn['account']]['friend_request'].pop(dataIn['to'], None)
        return True
    else:
        return False
def GetFriendRequest(dataIn):
    if dataIn['account'] in UserData:
        tmp = UserData[dataIn['account']]['friend_request']
        out = []
        for one in tmp:
            if one in UserData:
                out.append(one)
            else:
                tmp.pop(one, None)
        return True
    else:
        return False
def UserLogin(dataIn):
    now_time = time.time()
    if not dataIn['account'] in LoginLst:
        LoginLst.append(dataIn['account'])
        UserData[dataIn['account']]['last_login_time'] = now_time
        return True
    else: 
        return False
def UserLogout(dataIn):
    if dataIn['account'] in LoginLst:
        LoginLst.remove(dataIn['account'])
        return True
    else:
        return False
def ReadUserData():
    f = open('UserData.json', 'r')
    UserData = json.load(f)
    f.close()
def SaveUserData():
    f = open('UserData.json', 'w')
    f.write(json.dumps(UserData, indent = 4))
    f.close()


if __name__ == '__main__':
    a = dict({'a':[1,2,3,4], 'b':0})
    f = open('gg.txt','w')
    f.write(json.dumps(a, indent=4))
    f.close()











