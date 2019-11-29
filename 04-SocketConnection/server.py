#!/usr/bin/env python3
import socket
import selectors

HOST = '127.0.0.1'     # Server IP or Hostname
PORT = 12345           # Pick an open Port (1000+ recommended), must match the client sport
ENCODE = 'utf-8'       # Data transfer encoding standard

sel = selectors.DefaultSelector()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    print('SERVER: Socket created')

    # Managing error exception
    try:
        
        s.bind((HOST, PORT))

    except socket.error:
        
        print('SERVER: Bind failed ')

    print('SERVER: Listening on: ', (HOST, PORT))
    s.listen()
    
    s.setblocking(False)
    sel.register(s, selectors.EVENT_READ, data=None)

    conn, addr = s.accept()
    
    # Awaiting for message
    with conn:
        
        print('Connected by:', addr)
        
        while True:
            
            data = conn.recv(1024).decode(ENCODE)
            if not data:           
                break
            
            print('Server received: ' + data)
            reply = data
    
            # process your message
            if data == 'Quit':
               
                conn.send(bytes('Quit'.encode(ENCODE)))
                break
            
            else:
                
                reply = 'REPLYING: ' + reply

            # conn.send(bytes(reply,'utf-8')  # Sending reply
            print('Reply: ' + reply)
            conn.sendall(bytes(reply.encode(ENCODE)))

    conn.close()                    # Close connections

