import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_address = ('127.0.0.1', 9000)
sock.bind(server_address)
print >>sys.stderr, 'starting up ROS server on %s port %s' % sock.getsockname()
sock.listen(1)

while True:
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        print >> sys.stderr, 'client connected:', client_address
        while True:
            BUFFER_SIZE = 1024
            data = connection.recv(BUFFER_SIZE)
            if data:
                print >>sys.stderr, 'received "%s"' % data
            elif data == '':
                print 'connection closed'
                connection.close()
                break

    finally:
        connection.close()
