import socket
import game as g
import users as u
import rooms as r
import threading
import Queue
import time

# create a socket to listen for new connections
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# let socket be immidately reused
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind socket to port
s.bind(("", 50007))
# set socket to non blocking; this is weird on BSDs(osx)
# s.setblocking(False)
# listen!
s.listen(1)

gq = Queue.Queue()
lock = threading.Lock()
clients = []
usersOnline = []

class run_server(threading.Thread):
    def __init__ (self, conn, gq):
        self.conn = conn
        self.socket = socket
        self.gq = gq
        threading.Thread.__init__(self)

    ##def clientConn(self):
    def run(self):
        print threading.currentThread().getName()
        print "global queue is", self.gq
        # lock and update the clients list
        lock.acquire()
        clients.append(self)
        lock.release()
        n = g.Navigation()
        p = g.Player()
        self.conn.send("Login: ")
        self.data = self.conn.recv(1024).decode("latin1")
        self.textin = str(self.data).strip()
        user = self.textin
        if not p.checkUserExists(user):
            self.conn.send("Your name doesn't seem to be on our list. Creating new user!\n")
            p.addUser(user, "A new user with no description")
        self.conn.send("***************************************\n")
        self.conn.send("WELCOME " + self.textin.upper() + "\n")
        if u.users[user]['wizard']:
            self.conn.send("It's a pleasure to see a managing wizard around.\n")
        self.conn.send("***************************************\n")
        self.conn.send("Enjoy the trip, my dear friend.\n")
        self.conn.send("(If you are lost, type 'help' for a command list)\n")
        self.conn.send("***************************************\n")
        lock.acquire()
        usersOnline.append(user)
        lock.release()

        while 1:
            # take only latin strings, cuz italy
            self.data = self.conn.recv(1024).decode("latin1")
            if not self.data: break
            #if not self.gq.empty():
            #    print "A message is in the queue"
            #    shoutMsg = self.gq.get()
            #    self.conn.send(str(shoutMsg))
            #    self.gq.task_done()
            # we need to strip to remove whatever magic comes from telnet
            self.textin = str(self.data).strip()
            print "received ", self.textin, "from client"

            # Navigation commands
            if self.textin == "east" or self.textin == "e" and n.getCurLoc(user)['exits']:
                if "east" in n.getCurLoc(user)['exits']:
                    n.moveLoc(user, 'east')
                else:
                    self.conn.send("You hit a wall there. Go somewhere else, and be careful.\n")

            if self.textin == "west" or self.textin == "w" and n.getCurLoc(user)['exits']:
                if "west" in n.getCurLoc(user)['exits']:
                    n.moveLoc(user, 'west')
                else:
                    self.conn.send("You hit a wall there. Go somewhere else, and be careful.\n")

            if self.textin == "north" or self.textin == "n" and n.getCurLoc(user)['exits']:
                if "north" in n.getCurLoc(user)['exits']:
                    n.moveLoc(user, 'north')
                else:
                    self.conn.send("You hit a wall there. Go somewhere else, and be careful.\n")

            if self.textin == "south" or self.textin == "s" and n.getCurLoc(user)['exits']:
                if "south" in n.getCurLoc(user)['exits']:
                    n.moveLoc(user, 'south')
                else:
                    self.conn.send("You hit a wall there. Go somewhere else, and be careful.\n")

            if self.textin == "up" or self.textin == "u" and n.getCurLoc(user)['exits']:
                if "up" in n.getCurLoc(user)['exits']:
                    n.moveLoc(user, 'up')
                else:
                    self.conn.send("You hit a wall there. Go somewhere else, and be careful.\n")

            if self.textin == "down" or self.textin == "d" and n.getCurLoc(user)['exits']:
                if "down" in n.getCurLoc(user)['exits']:
                    n.moveLoc(user, 'down')
                else:
                    self.conn.send("You hit a wall there. Go somewhere else, and be careful.\n")

            # Object commands
            if self.textin == "inventory" or self.textin == "i":
                self.conn.send(str(p.getInventory(user)) + "\n")

            if self.textin.startswith("get "):
                item = self.textin[4:]
                loc = n.getCurLoc(user)
                if item in loc['items']:
                    p.addItem(user, item)
                    loc['items'].remove(item)
                else:
                    self.conn.send("Sorry, that item seems to have dissapeared, try again.\n")

            if self.textin.startswith("drop "):
                item = self.textin[5:]
                loc = n.getCurLoc(user)
                p.dropItem(user, item)
                loc['items'].append(item)

            # Communication commands
            if self.textin.startswith("shout "):
                mes = self.textin[6:]
                #  send message to all users
                for c in clients:
                    c.conn.send(mes)
                #self.gq.put(str(mes))

            # Game control commands
            if self.textin == "look":
                loc = n.getCurLoc(user)
                self.conn.send("You are currently in room " + str(p.getCurLoc(user)))
                self.conn.send("("+ str(loc['description']) + ")\n")
                self.conn.send("This room contains:" + str(loc['items']) + "\n")
                self.conn.send("It contains exits " + str(loc['exits']) + "\n")

            if self.textin == "who":
                # TODO - print out all the active users logged in
                self.conn.send("==Users Online ==\n")
                for user in usersOnline:
                    self.conn.send(user + "\n")

            if self.textin == "help":
                self.conn.send("HELP - GAME OPTIONS \n")
                self.conn.send("* get <itemName> -- takes an item from room and places it in your inventory\n")
                self.conn.send("* drop <itemName> -- takes an item from your inventory and places it in room\n")
                self.conn.send("* i -- lists your inventory\n")
                self.conn.send("* n, e, s, w, u, d -- move between rooms\n")
                self.conn.send("* look -- shows room name, description, contents list and exit list\n")
                self.conn.send("* quit -- exits game\n")
                if u.users[user]['wizard']:
                    self.conn.send("* @tele <roomName> -- teleports your player to a new room\n")
                    self.conn.send("* @dig <roomName> -- create a room and moves you to it\n")
                    self.conn.send("* @open <direction> <roomToGo> -- create an exit in the given direction to the given room\n")
                    self.conn.send("* @desc <description> -- adds a description to the current room\n")
                    self.conn.send("* @create <itemName> -- creates an item in the current room\n")
            if self.textin == "quit":
                self.conn.send("Farewell to you, my friend. \n")
                self.conn.close()

            if self.textin.startswith("@tele ") and u.users[user]['wizard']:
                room = self.textin[6:]
                if room in r.rooms:
                    u.users[user]['location'] = room

            if self.textin.startswith("@dig ") and u.users[user]['wizard']:
                roomName = self.textin[5:]
                newRoom = {roomName: {
                            "description": "",
                            "exits": {},
                            "items": []
                        }}
                r.rooms.update(newRoom)
                u.users[user]['location'] = roomName

            if self.textin.startswith("@open ") and u.users[user]['wizard']:
                readIn = self.textin.split()
                direction = readIn[1]
                destination = readIn[2]
                loc = n.getCurLoc(user)
                loc['exits'].update({direction: destination})

            if self.textin.startswith("@desc ") and u.users[user]['wizard']:
                desc = self.textin[6:]
                loc = n.getCurLoc(user)
                loc['description'] = desc

            if self.textin.startswith("@create ") and u.users[user]['wizard']:
                item = self.textin[8:]
                loc = n.getCurLoc(user)
                loc['items'].append(item)

        lock.acquire()
        clients.remove(self)
        lock.release()
        self.conn.close()

threads = []
while 1:
    conn, addr = s.accept()
    print "connected", addr
    lq = Queue.Queue()
    world = run_server(conn, gq)
    world.start()
    threads.append(world)
    time.sleep(0.1)

s.close()
