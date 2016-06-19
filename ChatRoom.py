import json
import DataBase as DB

GroupIndex = 0
GroupTable = {} 
#{
# 'ID': '0',
# 'Name': 'My Chat Room',
# 'Member': ['fulton74717','futen84717']
#}
def NewBag():
    a = dict({'id':'', 'name':'', 'member':[]})
    return a
def CreateGroup(dataIn):
    tmp = NewBag()
    try:
        tmp['id'] = str(GroupIndex)
        GroupIndex += 1
        tmp['name'] = dataIn['name']
        GroupTable[tmp['id']] = tmp
        return True
    except IndexError:
        return False
def AddMemberToGroup(dataIn):
    if dataIn['id'] in GroupTable:
        for person in dataIn['who']:
            if not person in GroupTable[dataIn['id']]['member'] and person in DB.UserData:
                GroupTable[dataIn['id']]['member'].append(person)
        return True
    return False
def RemoveMemberFromGroup(dataIn):
    if dataIn['id'] in GroupTable:
        person = dataIn['who']
        if person in GroupTable[dataIn['id']]['member'] and person in DB.UserData:
            GroupTable[dataIn['id']]['member'].remove(person)
            return True
    return False
def CreateMessage(dataIn):
    data = dict({'command':dataIn['command'], 'account':dataIn['to'], 'from':dataIn['account'],
                'message':dataIn['message']})
    return json.dumps(data)
