import json
import DataBase as DB
import os

GroupIndex = 0
if os.path.isfile('GroupData.json'):
    f = open('GroupData.json', 'r')
    GroupTable = json.load(f)
    f.close()
else:
    GroupTable = {}
#{
# 'ID': '0',
# 'Name': 'My Chat Room',
# 'Member': ['fulton74717','futen84717']
#}
def NewBag():
    a = dict({'id':'', 'owner':'', 'name':'', 'member':[]})
    return a
def CreateGroup(dataIn):
    global GroupIndex
    tmp = NewBag()
    try:
        tmp['id'] = str(GroupIndex)
        GroupIndex += 1
        tmp['name'] = dataIn['name']
        tmp['owner'] = dataIn['account']
        tmp['member'].append(dataIn['account'])
        GroupTable[tmp['id']] = tmp
        return True
    except IndexError:
        return False
def AddMemberToGroup(dataIn):
    if dataIn['id'] in GroupTable:
        person = dataIn['who']
        if not person in GroupTable[dataIn['id']]['member'] and person in DB.UserData:
            GroupTable[dataIn['id']]['member'].append(person)
            return True
    return False
def RemoveMemberFromGroup(dataIn):
    if dataIn['id'] in GroupTable:
        person = dataIn['account']
        if person in GroupTable[dataIn['id']]['member'] and person in DB.UserData:
            GroupTable[dataIn['id']]['member'].remove(person)
            return True
    return False
def CreateMessage(dataIn):
    data = dict({'command':dataIn['command'], 'account':dataIn['to'], 'from':dataIn['account'],
                'message':dataIn['message']})
    return json.dumps(data)
def SoundRequest(dataIn):
    data = dict({'command':dataIn['command'], 'from':dataIn['account']})
    return json.dumps(data)
def CreateSoundMessage(dataIn):
    data = dict({'command':dataIn['command'], 'from':dataIn['account'], 'voice':dataIn['voice']})
    return json.dumps(data)
def CreateGroupMessageDict(dataIn):
    name = DB.UserData[dataIn['account']]['nickname'] + '(' + dataIn['account']  + ')'
    data = dict({'command':dataIn['command'], 'id':dataIn['id'], 'from':name,
        'message':dataIn['message'], 'member':GroupTable[dataIn['id']]['member']})
    return data 
def AskingUpdate(dataIn):
    data = DB.AskingUpdate(dataIn)
    who = data['account']
    out = []
    for key in GroupTable:
        tmp = GroupTable[key]
        if who in tmp['member']:
            member_lst = []
            for one in tmp['member']:
                if not one == who:
                    member_lst.append(one)
            out.append(key)
            out.append(tmp['name'])
            out.append(member_lst)
    data['group'] = out
    return json.dumps(data)
def SaveGroupData():
    for ID in GroupTable:
        if len(GroupTable[ID]) == 0:
            GroupTable.pop(ID, None)
    f = open('GroupData.json','w')
    f.write(json.dumps(GroupTable, indent=4))
    f.close()
