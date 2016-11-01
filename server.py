import socket

#create a socket to listen for new connections
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#let socket be immidately reused
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#bind socket to looopback
s.bind(("", 50007))

#set socket to non blocking; this is weird on BSDs(osx)
#s.setblocking(False)

#listen!
s.listen(1)


conn, addr = s.accept()
print "connected", addr

while 1:
    #take only latin strings, cuz italy
    data = conn.recv(1024).decode("latin1")
    if not data: break
    #we need to strip to remove whatever magic comes from telnet
    textin = str(data).strip()
    print "received ", textin, "from client"
    if textin == "hello":
        print "fuuuuuuuuck"
        conn.sendall("got it!")
conn.close()

#data structure for rooms
rooms = {
    "Cave": {
        "description": "The cave is damp and cold. There's an exit in the distance",
        "exits": { "outside": "Outside" },
    },
    "Outside": {
        "description": "You're outside the cave in a field. You're warm.",
        "exits": { "inside": "Cave" },
    }
}
