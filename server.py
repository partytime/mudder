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
    data = conn.recv(1024)
    if not data: break
    textin = str(data)
    print type(textin)
    print "received ", textin, "from client"
    print "data is ", data
    if textin == "hello":
        print "fuuuuuuuuck"
    if textin == "kill":
        print "hit kill", textin
        conn.close()
conn.close()
