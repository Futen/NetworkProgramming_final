from Tkinter import *
from threading import Thread
from PIL import ImageTk, Image
import socket
import json
import thread
import ttk
import time
import pyaudio
import Log
import subprocess


PIKA_SER = 'C:/Python27/python.exe Server.py'
PIKA_Cli = 'C:/Python27/python.exe pikaclient.py'

LOCALIP = '192.168.1.105'


""" for user to enter server's IP port """
class ServerIP_Port:

    def __init__(self, master):

        self.label_1 = Label(master, text="ServerIP")
        self.label_2 = Label(master, text="ServerPort")
        self.entry_1 = Entry(master)
        self.entry_2 = Entry(master)

        self.label_1.grid(row=0, sticky=E)      # East, West, North, South
        self.label_2.grid(row=1)
        self.entry_1.grid(row=0, column=1)
        self.entry_2.grid(row=1, column=1)

        self.button_1 = Button(master, text="OK", command=self.setIP)
        self.button_1.grid(row=2, column=2)
        self.button_2 = Button(master, text="Quit", command=exit)
        self.button_2.grid(row=2, column=3)

    def setIP(self):
        global Server
        Server['IP'] = self.entry_1.get()
        Server['port'] = int(self.entry_2.get())
        print "IP : " + Server['IP']
        print "Port : " + str(Server['port'])
        root.quit()


""" A function to pop up error message """
class errorMessage:
    
    def __init__(self, message):
        self.top = Toplevel()
        self.top.title("error message")

        self.msg = Message(self.top, text=message)
        self.msg.pack()

        self.button = Button(self.top, text="OK", command=self.top.destroy)
        self.button.pack()


""" Let user to do offline test """
class Test:

    def __init__(self):
        self.testTop = Toplevel()
        self.testTop.title("Testing Plateform")

        self.button_chatTest = Button(self.testTop, text="Chat Test", command=self.ChatTest)
        self.button_chatTest.pack()       
        self.button_chatTest2 = Button(self.testTop, text="Chat Test2", command=self.ChatTest2)
        self.button_chatTest2.pack()

        
        self.button_chatTest3 = Button(self.testTop, text="groupChat Test", command=self.groupChatTest)
        self.button_chatTest3.pack()
        self.button_chatTest4 = Button(self.testTop, text="groupChat Test2", command=self.groupChatTest2)
        self.button_chatTest4.pack()

        self.button_tree = Button(self.testTop, text="Update Tree", command=self.update)
        self.button_tree.pack()
        self.button_tree2 = Button(self.testTop, text="Update Tree2", command=self.update2)
        self.button_tree2.pack()

        self.button_friend = Button(self.testTop, text="Friend req", command=self.friend)
        self.button_friend.pack()
        self.button_friend2 = Button(self.testTop, text="Friend req2", command=self.friend2)
        self.button_friend2.pack()

    """ simulate a friend give you message """
    def ChatTest(self):
        global ChatFrom, newFriendMsg, loadFriendMsg
        ChatFrom = {'from':'a', 'message':"Hello\n\n"}
        if ChatFrom['from'] not in ChatingList:
            newFriendMsg = 1
        else:
            loadFriendMsg = 1

    def ChatTest2(self):
        global ChatFrom, newFriendMsg, loadFriendMsg
        ChatFrom = {'from':'b', 'message':"Hello\n\n"}
        if ChatFrom['from'] not in ChatingList:
            newFriendMsg = 1
        else:
            loadFriendMsg = 1

    """ simulate a user send messageto group """
    def groupChatTest(self):
        global ChatFromGroup, newGroupMsg, loadGroupMsg
        ChatFromGroup = ['group1', 'Andy', "Hello\n\n"]    # msg to  group 1 from Andy
        if ChatFrom[0] not in ChatingList:
            newGroupMsg = 1
        else:
            loadGroupMsg = 1

    def groupChatTest2(self):
        global ChatFromGroup, newGroupMsg, loadGroupMsg
        ChatFromGroup = ['group2', 'Bob', "Hello\n\n"]
        if ChatFrom[0] not in ChatingList:
            newGroupMsg = 1
        else:
            loadGroupMsg = 1
    
    """ simulate friend tree update """
    def update(self):
        global friendList, groupList, updateTree
        msg = {'friend':['a','apple','online', 'b','banana','offline', 'c','cucumber','busy'], 'group':['group1','NTHU','group2','NTU','group3','SSHU']}
        friendList = msg['friend']
        groupList = msg['group']
        updateTree = 1

    def update2(self):
        global friendList, groupList, updateTree
        msg = {'friend':['a','apple','online', 'b','banana','online', 'c','cucumber','offline', 'd','dpple','busy', 'e','ebanana','online', 'f','fcucumber','offline'
                            , 'g','gapple','online', 'h','hbanana','online', 'i','icucumber','offline', 'j','jdpple','busy', 'k','kebanana','online', 'l','lfcucumber','offline'], 
                'group':['group1','NTHU','group2','NTU', 'group3','NTHU1','group4','NTU1', 'group5','NTHU2','group6','NTU2'
                            , 'group7','NTHU4','group8','NTU6', 'group9','NTHU10','group10','NTU81', 'group11','NTHU25','group12','NTU21']}
        friendList = msg['friend']
        groupList = msg['group']
        updateTree = 1

    """ simulate friend request arrive """
    def friend(self):
        global recvFriendReq, reqAccount
        msg = {'account':'b'}
        reqAccount = msg['account']
        recvFriendReq = 1

    def friend2(self):
        global recvFriendReq, reqAccount
        msg = {'account':'c'}
        reqAccount = msg['account']
        recvFriendReq = 1
        
""" A class for user login or register """
class RegisterLogin:

    def __init__(self, master):
      
        self.backframe = Frame(master, bg = "purple3", width=50, height=150)
        self.backframe.pack(side=TOP, fill=BOTH, expand=1)

        self.nameframe = Frame(self.backframe, bg = "purple4", width=50, height=100)
        self.nameframe.pack(side=BOTTOM)
        
        self.label_1 = Label(self.nameframe, text="Account", bg="purple4", fg="white", borderwidth=3, width=10)
        self.label_2 = Label(self.nameframe, text="Password", bg="purple4", fg="white", borderwidth=3, width=10)
        self.entry_1 = Entry(self.nameframe, width=25)
        self.entry_2 = Entry(self.nameframe, width=25, show="*")

        self.label_1.grid(row=0, sticky=W)
        self.entry_1.grid(row=0, column=1)      
        self.label_2.grid(row=1, sticky=W)
        self.entry_2.grid(row=1, column=1)

        self.button_1 = Button(self.nameframe, text="Login", bg="Gold", padx=8, pady=8, command=self.Login)
        self.button_1.grid(row=0, column=2, rowspan=2, sticky=W+E+N+S, padx=8, pady=8)

        self.button_2 = Button(self.nameframe, text="Register",bg="azure", command=self.Register)
        self.button_2.grid(row=2, column=2)

    """ send login message to server and wait for reply """
    def Login(self):
        global User, sock, recvUdp
        User['account'] = self.entry_1.get()
        User['passwd'] = self.entry_2.get()
        print("Logging")
        print "Name : " + User['account']
        print "Passwd : " + User['passwd']
        msg = {'command': 'Login', 'account':User['account'], 'password':User['passwd'], 'port':recvUdp.getsockname()[1], 'localip':LOCALIP}                  # need to discuss the msg format
        data_string = json.dumps(msg) #data serialized
        sock.send(data_string + '\n')

        self.ReactLogin()   # wait for reply

    """ send register message to server and wait for reply """
    def Register(self):
        global User, sock
        User['account'] = self.entry_1.get()
        User['passwd'] = self.entry_2.get()
        print("Registering")
        print "Name : " + User['account']
        print "Passwd : " + User['passwd']
        msg = {'command': 'Register', 'account':User['account'], 'password':User['passwd']}               # need to discuss the msg format
        data_string = json.dumps(msg) #data serialized
        sock.send(data_string + '\n')
        self.entry_1.delete(0, 'end')
        self.entry_2.delete(0, 'end')

        self.ReactRegister()    # wait for reply


    """ Waiting server send back the result
        success or fail and pop up message box"""
    def ReactRegister(self):
        global reactRegister, msg, RegisLogin

        if reactRegister == 1:               
            if msg['data'] == 'ok':
                top = Toplevel()
                top.title("message")

                msg = Message(top, text="Register success")
                msg.pack()

                button = Button(top, text="OK", command=top.destroy)
                button.pack()
                reactRegister = 0
                return
            else:
                errorMessage("The account is already exit")
                reactRegister = 0
                return
        RegisLogin.after(500, self.ReactRegister)
        return

    
    """ Waiting server send back the result
        success or fail and pop up message box"""
    def ReactLogin(self):
        global reactLogin, msg, RegisLogin
        
        if reactLogin == 1:
            if msg['data'] == 'ok':
                reactLogin = 0  
                RegisLogin.quit()
                return
            else:
                errorMessage("The password or account is wrong")
                reactLogin = 0
                return         
        RegisLogin.after(500, self.ReactLogin)
        return


""" A class for main interface """
class PikaChat:

    def __init__(self, master):
        global sock, User
        global loadFriendMsg, loadGroupMsg, ChatFrom, ChatFromGroup, ChatingList

        self.topframe = Frame(master, bg = "white", width=400, height=100)
        self.topframe.place(x=0, y=0, width=400, height=100)
        Profile(self.topframe)

        self.medianframe = Frame(master, bg = "white", width=400, height=560)
        self.medianframe.place(x=0, y=100, width=400, height=560)
        FriendTree(self.medianframe)

        self.bottomframe = Frame(master, bg = "gray", width=400, height=40)
        self.bottomframe.place(x=0, y=660, width=400, height=40)
        Search(self.bottomframe)

        #Test()
        self.showRequest()
        self.RecvVoice()
        self.popPika()

        self.popRoom()
        self.popRequest()
    

    """ When other invite you to play with him/her
        pop up the message box, let user 
        reply other's pika request """
    def popPika(self):
        global poppika, PikaMsg

        if poppika == 1:
            self.top = Toplevel()
            self.top.title("Pika Request")
            self.top.geometry('300x100')

            self.msg = Message(self.top, text=PikaMsg['from'] + " want to play with You", width=200, font=14)
            self.msg.place(x=30, y=25)

            self.buttonYes = Button(self.top, text="Accept", bg='green', command=self.PikaAccept)
            self.buttonYes.place(x=80, y=70)
            self.buttonNo = Button(self.top, text="Reject", bg='red', command=self.PikaReject)
            self.buttonNo.place(x=170, y=70)
            poppika = 0
            
        root.after(500, self.popPika)
        

    """ When you click on the accept button
        send back the accept message and start playing"""
    def PikaAccept(self):
        global PikaMsg, User

        msg = {'command': 'PikaAccept', 'account':User['account'], 'to':PikaMsg['from']}
        data_string = json.dumps(msg) #data serialized
        sock.send(data_string + '\n')

        self.top.destroy()

        thread.start_new_thread(self.pikaServer, ())


    """ When you click on reject button
        send back the accept message """
    def PikaReject(self):
        global PikaMsg, User

        msg = {'command': 'PikaReject', 'account':User['account'], 'to':PikaMsg['from']}
        data_string = json.dumps(msg) #data serialized
        sock.send(data_string + '\n')

        self.top.destroy()


    """ Call terminal to turn on the game """
    def pikaServer(self):
        global PIKA_SER
        print "start pika"
        subprocess.call(PIKA_SER, shell=True)
        

    """ When login, aks server if there anyone
        send friend request to you """
    def showRequest(self):
        global User
        msg = {'command': 'ShowRequest', 'account':User['account']}
        data_string = json.dumps(msg) #data serialized
        sock.send(data_string + '\n')


    """ If friend send you a message to you, but the chating window
        between you guys not yet existed, pop it up. Or someone send
        the message to one of your group, pop it up """
    def popRoom(self):
        global newFriendMsg, newGroupMsg, ChatFrom, ChatFromGroup, ChatingList

        if newFriendMsg == 1:
            Chatroom(ChatFrom['from']).PrintFriendMsg()
            ChatingList.append(ChatFrom['from'])
            print ChatingList
            newFriendMsg = 0
        elif newGroupMsg == 1:
            GroupChatroom(ChatFromGroup['id']).PrintGroupMsg()
            ChatingList.append(ChatFromGroup['id'])
            newGroupMsg = 0  
        root.after(500, self.popRoom)

    """ If someone send request to you, pop up the windows
        let user decide accept or not. P.s. recvFriendReq
        is the signal when running the program, someone 
        send request to you. While recvFriendReqS is the signal
        when first login, you call showRequest, the server 
        send back the result to you"""
    def popRequest(self):
        global recvFriendReq, reqAccount, recvFriendReqS, friend_request

        if recvFriendReq == 1:
            AcceptFriend(reqAccount)
            recvFriendReq = 0
        elif recvFriendReqS == 1:
            for req in friend_request:
                AcceptFriend(req)
            recvFriendReqS = 0
        root.after(500, self.popRequest)


    """ Use python's module to recv the sound """
    def RecvVoice(self):
        FORMAT = pyaudio.paInt16
        CHUNK = 256
        CHANNELS = 2
        RATE = 44100

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels = CHANNELS,
                        rate = RATE,
                        output = True,
                        frames_per_buffer = CHUNK,
                        )

        thread.start_new_thread(self.udpRecv, (CHUNK, CHANNELS,))
        thread.start_new_thread(self.play, (stream, CHUNK,))

    """ Once the user login, open a udp socket to 
        ready to listen from other users' voice """
    def udpRecv(self, CHUNK, CHANNELS):
        global recvUdp, recvframes
        while True:
            print "recving data"
            try:
                soundData, addr = recvUdp.recvfrom(CHUNK * CHANNELS * 2)
                recvframes.append(soundData)
            except:
                pass

    """ Play out the sound you received """
    def play(self, stream, CHUNK):
        global recvUdp, recvframes
        BUFFER = 10
        while True:
            if len(recvframes) == BUFFER:
                while True:
                    try:
                        stream.write(recvframes.pop(0), CHUNK)
                    except:
                        pass

""" A class for deal with user profile """
class Profile():

    def __init__(self, master):
        self.getProfile()
        self.master = master
        self.userState()

        self.profile = Button(self.master, fg="white", bg = "purple3", padx=1, pady=1, text="Edit Profile", command=self.editProfile)
        self.profile.place(x=300, y=5, width=100)
        self.editaccount = Button(self.master, fg="white", bg = "purple3", padx=1, pady=1, text="Edit Password", command=self.editPasswd)
        self.editaccount.place(x=300, y=35, width=100)
        self.editaccount = Button(self.master, fg="white", bg = "purple3", padx=1, pady=1, text="Delete Account", command=self.deleteAccountCheck)
        self.editaccount.place(x=300, y=65, width=100)

        time.sleep(0.1)
        self.printProfile()

    """ Can let user change their state """
    def userState(self):
        self.state = StringVar(self.master)
        self.state.set("online")                # default value
        STATE = ['online', 'busy', 'offline']

        option = OptionMenu(self.master, self.state, *STATE, command=self.updateState)
        option.config(bg='white', width=75)
        option.place(x=5, y=5, width=75)

    """ If state changed, let server know """
    def updateState(self, value):
        global sock
        print(value)
        
        msg = {'command': 'updateState', 'account':User['account'], 'state':value}
        data_string = json.dumps(msg) #data serialized
        sock.send(data_string + '\n')
        
    """ Print your profile on GUI """
    def printProfile(self):

        self.message_name = Message(self.master, anchor=W, bg = "white", text='Name: ' + User['name'], width=240)
        self.message_birth = Message(self.master, anchor=W, bg = "white", text='Birthday: ' + User['birthday'], width=240)       
        self.message_motto = Message(self.master, anchor=W, bg = "white", text='Motto: ' + User['motto'], width=240)
        self.message_name.place(x=80, y=5, width=220)
        self.message_birth.place(x=80, y=35, width=220)
        self.message_motto.place(x=80, y=65, width=220)       

    """ Edit your profile's window"""
    def editProfile(self):

        self.top = Toplevel()
        self.top.title("Setting Profile")

        self.label_name = Label(self.top, text="Name")
        self.label_birth = Label(self.top, text="Birthday")
        self.label_motto = Label(self.top, text="Motto")
        self.entry_name = Entry(self.top)
        self.entry_birth = Entry(self.top)
        self.entry_motto = Entry(self.top)

        self.label_name.grid(row=0, sticky=E)      # East, West, North, South
        self.label_birth.grid(row=1)
        self.label_motto.grid(row=2)
        self.entry_name.grid(row=0, column=1)
        self.entry_birth.grid(row=1, column=1)
        self.entry_motto.grid(row=2, column=1)

        self.button_1 = Button(self.top, text="OK", command=self.setProfile)
        self.button_1.grid(row=3, column=2)
        self.button_2 = Button(self.top, text="Back", command=self.top.destroy)
        self.button_2.grid(row=3, column=3)

    """ Set the profile and update it on your screen"""
    def setProfile(self):
        global User
        User['name'] = self.entry_name.get()
        User['birthday'] = self.entry_birth.get()
        User['motto'] = self.entry_motto.get()
        self.sendProfile()

        self.message_name.grid_remove()
        self.message_birth.grid_remove()
        self.message_motto.grid_remove()
        self.printProfile()

    """ send the update data to server """
    def sendProfile(self):
        global sock, User       
        msg = {'command': 'Profile', 'account':User['account'], 'nickname':User['name'], 'birthday':User['birthday'], 'motto':User['motto']}
        data_string = json.dumps(msg) #data serialized
        sock.send(data_string + '\n')
          
        print "Name : " + User['name']
        print "Birthday : " + User['birthday']
        print "Motto : " + User['motto']
        self.top.destroy()

    """ When login, ask your own profile """
    def getProfile(self):
        global sock, User
        
        msg = {'command': 'getProfile', 'account': User['account']}
        data_string = json.dumps(msg) #data serialized
        sock.send(data_string + '\n')

    """ Can edit your password """
    def editPasswd(self):

        self.edit = Toplevel()
        self.edit.title("Setting Passwd")

        self.label_newpasswd = Label(self.edit, text="New Password")
        self.entry_newpasswd = Entry(self.edit)
        self.label_newpasswd.grid(row=0, sticky=E)      # East, West, North, South
        self.entry_newpasswd.grid(row=0, column=1)      

        self.button_1 = Button(self.edit, text="OK", command=self.sendNewPasswd)
        self.button_1.grid(row=1, column=2)
        self.button_2 = Button(self.edit, text="Back", command=self.edit.destroy)
        self.button_2.grid(row=1, column=3)

    """ Send new password to server """
    def sendNewPasswd(self):
        global sock, User

        User['passwd'] = self.entry_newpasswd.get()
        
        msg = {'command': 'Profile', 'account':User['account'], 'password':User['passwd']}
        data_string = json.dumps(msg) #data serialized
        sock.send(data_string + '\n')
        
        print "NewPasswd : " + User['passwd']
        self.edit.destroy()

    """ Can delete your account, need to confirm """
    def deleteAccountCheck(self):
        self.delete = Toplevel()
        self.delete.title("deleting account")
        self.label_passwd = Label(self.delete, text="Your Password")
        self.entry_passwd = Entry(self.delete)
        self.label_passwd.grid(row=0, sticky=E)      # East, West, North, South
        self.entry_passwd.grid(row=0, column=1)      

        self.button_1 = Button(self.delete, text="OK", command=self.deleteAccount)
        self.button_1.grid(row=1, column=2)
        self.button_2 = Button(self.delete, text="Back", command=self.delete.destroy)
        self.button_2.grid(row=1, column=3)

    """ Confirm if OK. If delete, let server know """
    def deleteAccount(self):
        global sock, User
        
        if self.entry_passwd.get() == User['passwd']:
            
            msg = {'command': 'Delete', 'account':User['account']}
            data_string = json.dumps(msg) #data serialized
            sock.send(data_string + '\n')
            
            print "Delete account success"
            root.quit()
        else:
            errorMessage("Deleting account password error")
            self.entry_passwd.delete(0, 'end')

""" A class for presenting the tree view"""
class FriendTree():

    def __init__(self, master):
        CreateGroup(master)
        self.tree = ttk.Treeview(master)
        self.tree.insert("", 1, "dir1", text="Friends", tags=("Dir"))      #insert(parent,index,item identifier,text) 
        self.tree.insert("", 2, "dir2", text="Groups", tags=("Dir"))
        self.tree.tag_configure('Dir', background='yellow', font=16)
        self.tree.place(x=6, y=50, width=370, height=510)

        self.tree.bind("<Double-1>",self.AskToChat)

        self.scrollbar = Scrollbar(master, command=self.tree.yview)
        self.scrollbar.bind("<MouseWheel>", self.tree.yview)
        self.tree['yscrollcommand'] = self.scrollbar.set
        self.scrollbar.place(x=380, y=50, height=500)

        self.online = ImageTk.PhotoImage(Image.open("online.jpg"))
        self.offline = ImageTk.PhotoImage(Image.open("offline.jpg"))
        self.busy = ImageTk.PhotoImage(Image.open("busy.jpg"))
        
        #creating function to send request asking friend_list&Group_list
        thread.start_new_thread(self.AskUpdating,())
        thread.start_new_thread(self.treeUpdate,())

    """ Update the tree every 6 seconds """
    def AskUpdating(self):
        global User, sock
        while True:           
            
            msg = {'command': 'AskingUpdate', 'account':User['account']}
            data_string = json.dumps(msg) #data serialized
            sock.send(data_string + '\n')
            
            print "Asking data"
            time.sleep(6)           #every 6 seconds ask for list                                   

    """ Update it"""
    def treeUpdate(self):
        global updateTree, friendList, groupList, lock
        while 1:
            if updateTree == 1:
                print "Updating"
                lock.acquire()
                self.reCreateTree()
                self.friendUpdate(friendList)
                self.groupUpdate(groupList)
                updateTree = 0
                lock.release()
                print "Update Fin"
                self.tree.place(x=6, y=50, width=370, height=500)

    """ destroy the tree first """
    def reCreateTree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.tree.insert("", 1, "dir1", text="Friends", tags=("Dir"))
        self.tree.insert("", 2, "dir2", text="Groups", tags=("Dir"))
        self.tree.tag_configure('Dir', background='yellow', font=16)

    """ construct friend tree first """
    def friendUpdate(self, data):
        global friendMap
        for i in range(0, len(data), 3):
            if data[i+2] == 'online':
                self.tree.insert("dir1","end",text = data[i+1] + ' (' + data[i] + ')' , image=self.online, values=(data[i]))
            elif data[i+2] == 'offline':
                self.tree.insert("dir1","end",text = data[i+1] + ' (' + data[i] + ')' , image=self.offline, values=(data[i]))
            else:
                self.tree.insert("dir1","end",text = data[i+1] + ' (' + data[i] + ')' , image=self.busy, values=(data[i]))
            friendMap[data[i]] = data[i+1]

        print friendMap
        self.tree.item("dir1", open=True)

    """ Then consruct the group tree """
    def groupUpdate(self, data):
        global groupMap, groupList

        for i in range(0, len(data), 3):
            member = ''
            for name in groupList[i+2]:
                member = member + ', ' + name
            member = member[2:]

            self.tree.insert("dir2","end",text = data[i+1] + ' (' + member + ')', values=(data[i]))
            groupMap[data[i]] = data[i+1]

        print groupMap
        self.tree.item("dir2", open=True)


    """ When double click the entry, pop up the 
        chatroom or group's room (need to check if 
        the window already existed)"""
    def AskToChat(self, event):
        global ChatingList
        item = self.tree.selection()[0]
        if self.tree.item(item,"text") != 'Friends' and self.tree.item(item,"text") != 'Groups':
            print "send request to " + self.tree.item(item,"text") + ' (' + self.tree.item(item,"values")[0] + ') '+ self.tree.parent(item)
            if self.tree.parent(item) == 'dir1':
                if self.tree.item(item,"values")[0] in ChatingList:
                    print "Already Open"
                else:
                    print "Chatroom"
                    ChatingList.append(self.tree.item(item,"values")[0])
                    print ChatingList
                    Chatroom(self.tree.item(item,"values")[0])
            elif self.tree.parent(item) == 'dir2':
                if self.tree.item(item,"values")[0] in ChatingList:
                    print "Already Open"
                else:
                    print "GroupChatroom"
                    ChatingList.append(self.tree.item(item,"values")[0])
                    print ChatingList
                    GroupChatroom(self.tree.item(item,"values")[0])

""" A class for user to create a new group """
class CreateGroup():

    def __init__(self, master):
        self.button_group = Button(master, text="Create Group", width=50, bg='purple3', fg='white', command=self.Create)
        self.button_group.place(x=300, y=10, width=100)

    """ Can enter the group's name """
    def Create(self):
        self.top = Toplevel()
        self.top.title("Create Group")
        self.top.geometry('300x100')

        self.entry_create = Entry(self.top, width=200)
        self.button_create = Button(self.top, text="Create", width=100, command=self.SendCreate)
        self.entry_create.place(x=0, y=40, width=200, height=25)
        self.button_create.place(x=200, y=40, width=100)

    """ Tell server """
    def SendCreate(self):
        global sock
        self.createName = self.entry_create.get()
        self.entry_create.delete(0, 'end')
        if self.createName != '':
            print (self.createName)
            
            msg = {'command': 'CreateGroup', 'account':User['account'], 'name':self.createName}
            data_string = json.dumps(msg) #data serialized
            sock.send(data_string + '\n')

            self.top.destroy()
          
        else:
            errorMessage("No data, Please enter again ~")

""" A class to show the friend request """
class AcceptFriend():

    def __init__(self, account):
        self.top = Toplevel()
        self.top.title("Friend Request")
        self.top.geometry('300x100')

        self.account = account
        self.msg = Message(self.top, text=self.account + " want to friend You", width=200, font=14)
        self.msg.place(x=30, y=25)

        self.buttonYes = Button(self.top, text="Accept", bg='green', command=self.Accept)
        self.buttonYes.place(x=80, y=70)
        self.buttonNo = Button(self.top, text="Reject", bg='red', command=self.Reject)
        self.buttonNo.place(x=170, y=70)

    def Accept(self):
        global sock
        print "accept"
        
        msg = {'command': 'AcceptInvite', 'account':User['account'], 'from':self.account}
        data_string = json.dumps(msg) #data serialized
        sock.send(data_string + '\n')
        
        self.top.destroy()
    def Reject(self):
        global sock
        print "reject"

        msg = {'command': 'RejectInvite', 'account':User['account'], 'from':self.account}
        data_string = json.dumps(msg) #data serialized
        sock.send(data_string + '\n')
        
        self.top.destroy()

""" A class can let user search for other user """
class Search():
    
    def __init__(self, master):
        self.entry_search = Entry(master, width=300)
        self.button_search = Button(master, text="Search", width=100, command=self.search)
        self.entry_search.place(x=5, y=10, width=300, height=25)
        self.button_search.place(x=325, y=10, width=70)

    """ Send the name to server """
    def search(self):
        global sock
        self.searchName = self.entry_search.get()
        self.entry_search.delete(0, 'end')
        if self.searchName != '':
            print (self.searchName)
            
            msg = {'command': 'Search', 'account':User['account'], 'who':self.searchName}
            data_string = json.dumps(msg) #data serialized
            sock.send(data_string + '\n')
            self.ReactSearch()  
        else:
            errorMessage("No data, Please enter again ~")

    """ React to the message sended back """
    def ReactSearch(self):
        global reactSearch, searchMsg
        while 1:
            if reactSearch == 1:
                if searchMsg['data'] == 'ok':
                    self.top = Toplevel()
                    self.top.title("Asking")
                    self.top.geometry('300x100')

                    self.msg = Message(self.top, text="Do you want to friend " + self.searchName + " ?", width=200, font=14)
                    self.msg.place(x=30, y=25)

                    self.buttonYes = Button(self.top, text="Yes", bg='green', command=self.SendFriendRequest)
                    self.buttonYes.place(x=80, y=70)
                    self.buttonNo = Button(self.top, text="No", bg='red', command=self.top.destroy)
                    self.buttonNo.place(x=170, y=70)

                else:
                    errorMessage("The account is not exit or You guys are already friend")
                reactSearch = 0
                break

    def SendFriendRequest(self):
        global sock
        msg = {'command': 'Invite', 'account':User['account'], 'to':self.searchName}
        data_string = json.dumps(msg) #data serialized
        sock.send(data_string + '\n')
        
        self.top.destroy()
        
""" A class for one to one chatroom """
class Chatroom():

    def __init__(self, account):
        global friendMap
        self.chatroom = Toplevel()
        self.chatroom.title("Chatroom  " + friendMap[account])
        self.chatroom.geometry('400x500')
        self.chatroom.resizable(width=False, height=False)

        self.who = account

        self.topframe = Frame(self.chatroom, bg = "white", width=150, height=50)
        self.topframe.pack(side=TOP, fill=X)
        
        self.getFriendProfile()
        time.sleep(0.1)
        self.printFriendProfile()

        self.ChatLog = Text(self.chatroom, bd=0, bg="white", height="8", width="50", font="Arial")
        self.ChatLog.config(state=DISABLED)

        #Bind a scrollbar to the Chat window
        self.scrollbar = Scrollbar(self.chatroom, command=self.ChatLog.yview, cursor="heart")
        self.scrollbar.bind("<MouseWheel>", self.ChatLog.yview)
        self.ChatLog['yscrollcommand'] = self.scrollbar.set

        #Create the Button to send message
        self.SendButton = Button(self.chatroom, font=30, text="Send", width="12", height=5,
                            bd=0, bg="#FFBF00", activebackground="#FACC2E",
                            command=self.PressButton)

        #Create the box to enter message
        self.EntryBox = Text(self.chatroom, bd=0, bg="white",width="29", height="5", font="Arial")
        self.EntryBox.bind("<KeyRelease-Return>", self.PressEnter)

        #Place all components on the screen
        self.scrollbar.place(x=376,y=50, height=350)
        self.ChatLog.place(x=6,y=50, height=350, width=370)
        self.EntryBox.place(x=6, y=401, height=90, width=265)
        self.SendButton.place(x=275, y=401, height=90)

        self.chatroom.protocol('WM_DELETE_WINDOW', self.CloseChatroom)

        self.photo_mic = ImageTk.PhotoImage(Image.open("mic.jpg"))
        self.photo_pika = ImageTk.PhotoImage(Image.open("pika.jpg"))
        self.button_unfriend = Button(self.topframe, text='Unfriend', command=self.Unfriend)
        self.button_unfriend.place(x=230, y=0, width=65, height=40)
        self.button_mic = Button(self.topframe, image=self.photo_mic, command=self.Mic)
        self.button_mic.place(x=300, y=0, width=40, height=40)
        self.button_pika = Button(self.topframe, image=self.photo_pika, command=self.Pika)
        self.button_pika.place(x=350, y=0, width=40, height=40)

        self.LoadMsg()

        thread.start_new_thread(self.recvFromFriend,())

    """ Can unfriend him/she """
    def Unfriend(self):
        global sock, User
        print "unfriend"

        msg = {'command': 'Unfriend', 'account':User['account'], 'who':self.who}
        data_string = json.dumps(msg) #data serialized
        sock.send(data_string + '\n')

        self.chatroom.destroy()

    """ Has a function let user chatting through mic """
    def Mic(self):
        global sock, User, IPOK

        msg = {'command': 'RequestIP', 'account':User['account'], 'who':self.who}
        data_string = json.dumps(msg) #data serialized
        sock.send(data_string + '\n')

        while IPOK == 0:
            pass
        IPOK = 0

        Audio(self.who)

    """ Has a game can let user play with friend """
    def Pika(self):
        global sock, User
        print "wait for friend"

        msg = {'command': 'RequestPika', 'account':User['account'], 'to':self.who}
        data_string = json.dumps(msg) #data serialized
        sock.send(data_string + '\n')

        self.waitForPika()

    """ Wait your friend's accept signal """
    def waitForPika(self):
        global pikaaccept, pikareject

        if pikaaccept == 1:
            print 'Accept'
            thread.start_new_thread(self.pikaClient, ())
            pikaaccept = 0
        elif pikareject == 1:
            print 'Reject'
            pikareject = 0

        root.after(500, self.waitForPika)

    """ If your friend accept, start the game """
    def pikaClient(self):
        print 'start pika'
        time.sleep(3)
        global PikaMsg
        IP = PikaMsg['ip']
        command = PIKA_Cli + ' ' + IP
        subprocess.call(command, shell=True)

    """ receive the message sended by friend """
    def recvFromFriend(self):
        global printFriendMsg, lock, ChatFrom

        while 1:
            if printFriendMsg == 1:
                lock.acquire()
                if self.who == ChatFrom['from']:
                    self.PrintFriendMsg()
                printFriendMsg = 0
                lock.release()
            else:
                pass
    """ When open the chatroom, request your friend's profile """
    def getFriendProfile(self):
        global User, sock
        msg = {'command': 'getFriendProfile', 'account':User['account'], 'who':self.who}
        data_string = json.dumps(msg) #data serialized
        sock.send(data_string + '\n')
        
    """ Show it on GUI """
    def printFriendProfile(self):
        global Friend

        self.message_name = Message(self.topframe, bg = "white", text='Name: ' + Friend['name'], width=200)
        self.message_birth = Message(self.topframe, bg = "white", text='Birthday: ' + Friend['birthday'], width=200)       
        self.message_motto = Message(self.topframe, bg = "white", text='Motto: ' + Friend['motto'], width=200)
        self.message_name.grid(row=0, column=1, sticky=W)
        self.message_birth.grid(row=0, column=2)
        self.message_motto.grid(row=1, column=1, sticky=W)

    """ When press enter, get the message """
    def PressEnter(self, event):
        self.EntryText = self.EntryBox.get("0.0",END)
        self.SendToServer()

    """ When press button, get the message + '\n' """
    def PressButton(self):
        self.EntryText = self.EntryBox.get("0.0",END) + '\n'
        self.SendToServer()

    """ Show the message on GUI, send to server """
    def SendToServer(self):
        global sock
        self.PrintMyMsg()

        msg = {'command': 'ChatToOne', 'account':User['account'], 'to':self.who, 'message':self.EntryText}
        data_string = json.dumps(msg) #data serialized
        sock.send(data_string + '\n')
        
        #Scroll to the bottom of chat windows
        self.ChatLog.yview(END)
        #Erace previous message in Entry Box
        self.EntryBox.delete("0.0",END)
    
    """ When open the chatroom, load the history message """
    def LoadMsg(self):
        global User
        data = Log.GetMessageData(User['account'], self.who)
        for item in data:
            if item['from'] == User['account']:
                self.LoadMyMsg(item)
            else:
                self.LoadFriendMsg(item)

    """ If the history message is mine """
    def LoadMyMsg(self, item):
        self.ChatLog.config(state=NORMAL)
        if self.ChatLog.index('end') != None:
            self.LineNumber = float(self.ChatLog.index('end'))-1.0
            self.ChatLog.insert(END, "You: " + item['message'])
            self.ChatLog.tag_add("You", self.LineNumber, self.LineNumber+0.4)
            self.ChatLog.tag_config("You", foreground="#FF8000", font=("Arial", 12, "bold"), justify=RIGHT)
            self.ChatLog.config(state=DISABLED)
            self.ChatLog.yview(END)

    """ If the history message is other's """
    def LoadFriendMsg(self, item):
        global friendMap
        self.ChatLog.config(state=NORMAL)
        
        self.LineNumber = float(self.ChatLog.index('end'))-1.0
        self.nameLen = len(friendMap[item['from']])*0.1
        print self.LineNumber
        print self.nameLen
        self.ChatLog.insert(END, friendMap[item['from']] + ': ' + item['message'])
        self.ChatLog.tag_add("Friend", self.LineNumber, self.LineNumber+self.nameLen)
        self.ChatLog.tag_config("Friend", foreground="#04B404", font=("Arial", 12, "bold"))
        self.ChatLog.config(state=DISABLED)
        self.ChatLog.yview(END)

    """ Print your message, store it in log """
    def PrintMyMsg(self):
        global User
        if self.EntryText != '':
            self.ChatLog.config(state=NORMAL)
            if self.ChatLog.index('end') != None:
                self.LineNumber = float(self.ChatLog.index('end'))-1.0
                self.ChatLog.insert(END, "You: " + self.EntryText)
                self.ChatLog.tag_add("You", self.LineNumber, self.LineNumber+0.4)
                self.ChatLog.tag_config("You", foreground="#FF8000", font=("Arial", 12, "bold"), justify=RIGHT)
                self.ChatLog.config(state=DISABLED)
                self.ChatLog.yview(END)
                Log.CreateMessage(User['account'], self.who, self.EntryText)

    """ Print friend's message, store it in log """
    def PrintFriendMsg(self):
        global ChatFrom, friendMap, User
        if ChatFrom['message'] != '':
            self.ChatLog.config(state=NORMAL)
        
            self.LineNumber = float(self.ChatLog.index('end'))-1.0
            self.nameLen = len(friendMap[ChatFrom['from']])*0.1
            print self.LineNumber
            print self.nameLen
            self.ChatLog.insert(END, friendMap[ChatFrom['from']] + ': ' + ChatFrom['message'])
            self.ChatLog.tag_add("Friend", self.LineNumber, self.LineNumber+self.nameLen)
            self.ChatLog.tag_config("Friend", foreground="#04B404", font=("Arial", 12, "bold"))
            self.ChatLog.config(state=DISABLED)
            self.ChatLog.yview(END)
            Log.CreateMessage(ChatFrom['from'], User['account'], ChatFrom['message'])

    """ When close the chatroom, remove from chatting list """
    def CloseChatroom(self):
        global ChatingList
        print "close chatroom"
        ChatingList.remove(self.who)
        self.chatroom.destroy()

""" A class for sending voice """
class Audio():

    def __init__(self, who):
        self.startchat = Toplevel()
        self.startchat.title("Chating")
        self.startchat.geometry("300x100")
        self.close = 0

        self.message = Message(self.startchat, text = "Chat to " + who, width=200)
        self.message.place(x=100, y=30)

        self.button = Button(self.startchat, text="Close", bg='red', command=self.CloseMic)
        self.button.place(x=130, y=70)
        self.send = 1
        self.who = who
        
        self.SendVoice()

    """ close the mic """
    def CloseMic(self):
        self.close = 1
        self.startchat.destroy()

    """ Open the stream file """
    def SendVoice(self):
        CHUNK = 256
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100

        p = pyaudio.PyAudio()

        stream = p.open(format = FORMAT,
                        channels = CHANNELS,
                        rate = RATE,
                        input = True,
                        frames_per_buffer = CHUNK,
                        )
        thread.start_new_thread(self.udpStream, ())
        thread.start_new_thread(self.record, (stream, CHUNK,))

    """ Send it to friend """
    def udpStream(self):  
        global sendUdp, FriendIP, sendframes
        IP = FriendIP
        while self.close == 0:
            if len(sendframes) > 0:
                print "sending data"
                sendUdp.sendto(sendframes.pop(0), (IP[0], IP[1]))

        sendUdp.close()

    """ record the voice """
    def record(self, stream, CHUNK):    
        global sendframes
        while self.close == 0:
            sendframes.append(stream.read(CHUNK))
        
""" A class for group chating """
class GroupChatroom():

    def __init__(self, groupID):
        global groupMap
        self.chatroom = Toplevel()
        self.chatroom.title("GroupChatroom  " + groupMap[groupID])
        self.chatroom.geometry('400x500')
        self.chatroom.resizable(width=False, height=False)

        self.groupID = groupID

        self.ChatLog = Text(self.chatroom, bd=0, bg="white", height="8", width="50", font="Arial")
        self.ChatLog.config(state=DISABLED)

        self.button_addmembor = Button(self.chatroom, text="Add Member", command=self.AddMember, bg='purple3', fg='white')
        self.button_addmembor.place(x=294, y=15, width=100)
        self.button_leavegroup = Button(self.chatroom, text="Leave Group", command=self.LeaveGroup, bg='purple3', fg='white')
        self.button_leavegroup.place(x=6, y=15, width=100)
        self.entry_member = Entry(self.chatroom)
        self.entry_member.place(x=144, y=15, width=150, height=25)

        #Bind a scrollbar to the Chat window
        self.scrollbar = Scrollbar(self.chatroom, command=self.ChatLog.yview, cursor="heart")
        self.scrollbar.bind("<MouseWheel>", self.ChatLog.yview)
        self.ChatLog['yscrollcommand'] = self.scrollbar.set

        #Create the Button to send message
        self.SendButton = Button(self.chatroom, font=30, text="Send", width="12", height=5,
                            bd=0, bg="#FFBF00", activebackground="#FACC2E",
                            command=self.SendToServer)

        #Create the box to enter message
        self.EntryBox = Text(self.chatroom, bd=0, bg="white",width="29", height="5", font="Arial")
        self.EntryBox.bind("<KeyRelease-Return>", self.PressEnter)

        #Place all components on the screen
        self.scrollbar.place(x=376,y=50, height=350)
        self.ChatLog.place(x=6,y=50, height=350, width=370)
        self.EntryBox.place(x=6, y=401, height=90, width=265)
        self.SendButton.place(x=275, y=401, height=90)

        self.chatroom.protocol('WM_DELETE_WINDOW', self.CloseGroupChatroom)

        thread.start_new_thread(self.recvFromGroup,())
    
    """ Add member to the group """
    def AddMember(self):
        global sock
        self.member = self.entry_member.get()
        self.entry_member.delete(0, 'end')
        print "add member" + self.member

        msg = {'command': 'AddMember', 'account':User['account'], 'id':self.groupID, 'who':self.member}
        data_string = json.dumps(msg) #data serialized
        sock.send(data_string + '\n')

    """ User leave the group """
    def LeaveGroup(self):
        print 'leave group'
        global sock

        msg = {'command': 'LeaveGroup', 'account':User['account'], 'id':self.groupID}
        data_string = json.dumps(msg) #data serialized
        sock.send(data_string + '\n')

        self.chatroom.destroy()

    def recvFromGroup(self):
        global printGroupMsg, ChatFromGroup

        while 1:
            if printGroupMsg == 1:
                lock.acquire()
                if self.groupID == ChatFromGroup['id']:
                    self.PrintGroupMsg()
                printGroupMsg = 0
                lock.release()

    """ When press enter, get the message """
    def PressEnter(self, event):
        self.EntryText = self.EntryBox.get("0.0",END)
        self.SendToServer()

    """ When press button, get the message + '\n' """
    def PressButton(self):
        self.EntryText = self.EntryBox.get("0.0",END) + '\n'
        self.SendToServer()

    """ Send it to the server """
    def SendToServer(self):
        global User, sock
        self.PrintMyMsg()

        msg = {'command': 'ChatToGroup', 'id':self.groupID, 'account':User['account'], 'message':self.EntryText}
        data_string = json.dumps(msg) #data serialized
        sock.send(data_string + '\n')
        #Scroll to the bottom of chat windows
        self.ChatLog.yview(END)
        #Erace previous message in Entry Box
        self.EntryBox.delete("0.0",END)
            
    """ Print my own message on GUI """
    def PrintMyMsg(self):
        if self.EntryText != '':
            self.ChatLog.config(state=NORMAL)
            if self.ChatLog.index('end') != None:
                self.LineNumber = float(self.ChatLog.index('end'))-1.0
                self.ChatLog.insert(END, "You: " + self.EntryText)
                self.ChatLog.tag_add("You", self.LineNumber, self.LineNumber+0.4)
                self.ChatLog.tag_config("You", foreground="#FF8000", font=("Arial", 12, "bold"), justify=RIGHT)
                self.ChatLog.config(state=DISABLED)
                self.ChatLog.yview(END)

    """ Print others' message on GUI """
    def PrintGroupMsg(self):
        global ChatFromGroup
        if ChatFromGroup['message'] != '':
            self.ChatLog.config(state=NORMAL)
        
            self.LineNumber = float(self.ChatLog.index('end'))-1.0
            self.nameLen = len(ChatFromGroup['from'])*0.1
            print self.LineNumber
            print self.nameLen
            self.ChatLog.insert(END, ChatFromGroup['from'] + ': ' + ChatFromGroup['message'])
            self.ChatLog.tag_add("Friend", self.LineNumber, self.LineNumber+self.nameLen)
            self.ChatLog.tag_config("Friend", foreground="#04B404", font=("Arial", 12, "bold"))
            self.ChatLog.config(state=DISABLED)
            self.ChatLog.yview(END)

    """ Close the group chatroom """
    def CloseGroupChatroom(self):
        global ChatingList
        print "close group chatroom"
        ChatingList.remove(self.groupID)
        self.chatroom.destroy()

""" A function to recv all socket from server """
def recvServer():
    
    global sock, Friend, lock, printFriendMsg, printGroupMsg, ChatFrom, ChatFromGroup, reactRegister, msg, reactLogin
    global reqAccount, msg, reactLogin, newFriendMsg, newGroupMsg, reactSearch, recvFriendReq, searchMsg, friend_request
    global recvFriendReqS, friendList, groupList, updateTree, User, FriendIP, IPOK, PikaMsg, poppika
    global pikaaccept, pikareject

    while 1:
        
        msgRecv = sock.recv(1300)
        try:
            msg = json.loads(msgRecv)
        except:
            continue
        print msg
        lock.acquire()
        if msg['command'] == 'Register':
            reactRegister = 1

        elif msg['command'] == 'Login':
            reactLogin = 1

        elif msg['command'] == 'Profile':
            print "success"

        elif msg['command'] == 'Search':
            searchMsg = msg
            reactSearch = 1

        elif msg['command'] == 'getFriendProfile':
            Friend['name'] = msg['nickname']
            Friend['birthday'] = msg['birthday']
            Friend['motto'] = msg['motto']

        elif msg['command'] == 'Unfriend':
            if msg['data'] == 'ok':
                print 'OK'
            else:
                print "GG"

        elif msg['command'] == 'ChatToOne':
            ChatFrom = msg
            if ChatFrom['from'] not in ChatingList:
                newFriendMsg = 1
            else:
                printFriendMsg = 1

        elif msg['command'] == 'ChatToGroup':
            ChatFromGroup = msg
            if ChatFromGroup['id'] not in ChatingList:
                newGroupMsg = 1
            else:
                printGroupMsg = 1

        elif msg['command'] == 'AskingUpdate':
            friendList = msg['friend']
            groupList = msg['group']
            updateTree = 1

        elif msg['command'] == 'ShowInvite':
            reqAccount = msg['from']
            recvFriendReq = 1

        elif msg['command'] == 'ShowRequest':
            friend_request = msg['friend_request']
            recvFriendReqS = 1

        elif msg['command'] == 'getProfile':
            User['name'] = msg['nickname']
            User['birthday'] = msg['birthday']
            User['motto'] = msg['motto']

        elif msg['command'] == 'AddMember':
            if msg['data'] == 'ok':
                print 'OK'
            else:
                print "GG"

        elif msg['command'] == 'LeaveGroup':
            if msg['data'] == 'ok':
                print 'OK'
            else:
                print "GG"

        elif msg['command'] == 'RequestIP':
            FriendIP = msg['ip']
            IPOK = 1

        elif msg['command'] == 'RequestPika':
            PikaMsg = msg
            poppika = 1

        elif msg['command'] == 'PikaAccept':
            PikaMsg = msg
            pikaaccept = 1

        elif msg['command'] == 'PikaReject':
            PikaMsg = msg
            pikareject = 1

        lock.release()
        
        
def Exit():
    thread.exit()
    exit(0)
        

def SendLogout():
    print "Logout"
    
    root.destroy()


Server = {'IP':'None', 'port':0}
"""
root = Tk()
root.title("ServerIP_Port")
a = ServerIP_Port(root)
root.protocol('WM_DELETE_WINDOW', Exit)  # root is your root window
root.mainloop()
root.destroy()
"""
Server['IP'] = '114.25.190.10'  
Server['port'] = 8000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((Server['IP'], Server['port']))
except sock.error:
    print "connect error"
    exit(0)

print "recvudp socket"
recvUdp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recvUdp.bind(('0.0.0.0', 0))
print recvUdp.getsockname()[1]

print "sendudp socket"
sendUdp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


lock = thread.allocate_lock()
printFriendMsg = 0
printGroupMsg = 0
reactRegister = 0
reactLogin = 0
reactSearch = 0
updateTree = 0
newGroupMsg = 0
newFriendMsg = 0
recvFriendReq = 0
recvFriendReqS = 0
recvAudio = 0
micBusy = 0
pikaBusy = 0

IPOK = 0
poppika = 0
pikareject = 0
pikaaccept = 0
recvframes = []
sendframes = []

msg = {}
PikaMsg = {}
searchMsg = {}
ChatFrom = {}
searchName = ""

User = {'account':'None', 'passwd':'None', 'name':'None', 'birthday':'None', 'motto':'None'}
Friend = {'name':'None', 'birthday':'None', 'motto':'None'}
ChatingList = []
friendMap = {}
groupMap = {}

thread.start_new_thread(recvServer,())


RegisLogin = Tk()
RegisLogin.title("RegisterLogin")
RegisLogin.geometry('400x500')
b = RegisterLogin(RegisLogin)
RegisLogin.resizable(width=False, height=False)
RegisLogin.protocol('WM_DELETE_WINDOW', Exit)  # root is your root window
RegisLogin.mainloop()
RegisLogin.destroy()



root = Tk()
root.title("Pika Chat")
root.geometry('400x700')
main = PikaChat(root)
root.resizable(width=False, height=False)
root.protocol('WM_DELETE_WINDOW', SendLogout)  # root is your root window
root.mainloop()
exit(0)


