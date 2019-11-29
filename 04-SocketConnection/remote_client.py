#!/usr/bin/env python3
import socket

HOST = 'piBorg_Mother'    # Enter IP or Hostname of your server
PORT = 12345          # Pick an open Port (1000+ recommended), must match the server port
ENCODE = 'utf-8'      # Data transfer encoding standard

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

try:
    
    # Lets loop awaiting for your input
    while True:
        
        command = input('Enter your command: ')
        
        print('Command: ' + command)
        
        s.send(bytes(command.encode(ENCODE)))
        
        reply = s.recv(1024)
        
        if reply == 'Terminate':
            break
        
        print(reply)

except BrokenPipeError:
    
    print('Server has died, signing off...')
    
except:
    
    print('Unknown exception, quitting...')
    

