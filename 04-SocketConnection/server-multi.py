#!/usr/bin/env python3
import socket
import selectors
import types

HOST = ''     # Server IP or Hostname
#HOST = 'piBorg_Mother'     # Server IP or Hostname
#HOST = '127.0.0.1'     # Server IP or Hostname
PORT = 12345           # Pick an open Port (1000+ recommended), must match the client sport
ENCODE = 'utf-8'       # Data transfer encoding standard

def accept_wrapper(sock):
    
    conn, addr = sock.accept()  # Should be ready to read
    
    print('SERVER: Accepted connection from: ', (conn, addr))
    
    conn.setblocking(False)
    
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    
    local_events = selectors.EVENT_READ | selectors.EVENT_WRITE
    
    sel.register(conn, local_events, data=data)
    
def service_connection(pKey, pMask):
    
    sock = pKey.fileobj
    data = pKey.data
    
    if pMask & selectors.EVENT_READ:
        
        recv_data = sock.recv(1024)  # Should be ready to read
        
        if recv_data:
            data.outb += recv_data
            
        else:
            print('SERVER: Closing connection to: ', data.addr)
            sel.unregister(sock)
            sock.close()
            
    if pMask & selectors.EVENT_WRITE:
        
        if data.outb:
            print('SERVER: Echoing: ', repr(data.outb), ': to :', data.addr)
            
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]
            
#### START OF MAIN PROGRAM ####
            
sel = selectors.DefaultSelector()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    print('SERVER: Socket created')

    # Managing error exception
    try:
        
        s.bind((HOST, PORT))

        print('SERVER: Listening on: ', (HOST, PORT))
        s.listen()
        
        s.setblocking(False)
        sel.register(s, selectors.EVENT_READ, data=None)
        
        # Awaiting for message
        while True:
            
            # print('SERVER: Waiting for something to happen...')
            
            events = sel.select(timeout=None)
            
            for key, mask in events:
                
                # print('SERVER: Looking for data. events: ' + events)
                
                if key.data is None:
                    
#                    print('SERVER: key.data is None...')
                    accept_wrapper(key.fileobj)
                
                else:
                    
#                    print('SERVER: key.data is Not None...')
                    service_connection(key, mask)
                
    except socket.error:
        
        print('SERVER: Bind failed ')
    