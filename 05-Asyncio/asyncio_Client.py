#!/usr/bin/env python3
# asyncio_echo_client_protocol.py
# https://pymotw.com/3/asyncio/io_protocol.html
#
import asyncio
import functools
import logging
import sys

MESSAGES = [
    b'This is the message. ',
    b'It will be sent ',
    b'in parts.',
]
SERVER_ADDRESS = ('localhost', 66666)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)

log = logging.getLogger('main')

event_loop = asyncio.get_event_loop()

# The client protocol class defines the same methods as the server, with different implementations. The class constructor accepts two arguments, a list of the messages to send and a Future instance to use to signal that the client has completed a cycle of work by receiving a response from the server.

class EchoClient(asyncio.Protocol):

    def __init__(self, messages, future):
        
        super().__init__()
        
        self.messages = messages
        self.log = logging.getLogger('EchoClient')
        self.f = future

    # When the client successfully connects to the server, it starts communicating immediately. The sequence of messages is sent one at a time, although the underlying networking code may combine multiple messages into one transmission. When all of the messages are exhausted, an EOF is sent.

    # Although it appears that the data is all being sent immediately, in fact the transport object buffers the outgoing data and sets up a callback to actually transmit when the socket’s buffer is ready to receive data. This is all handled transparently, so the application code can be written as though the I/O operation is happening right away.

    def connection_made(self, transport):

        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.log.debug('connecting to {} port {}'.format(*self.address))
        
        # This could be transport.writelines() except that
        # would make it harder to show each part of the message
        # being sent.
        for msg in self.messages:
            
            transport.write(msg)
            self.log.debug('sending {!r}'.format(msg))
            
        if transport.can_write_eof():
            
            transport.write_eof()
            
    # When the response from the server is received, it is logged.

    def data_received(self, data):
        
        self.log.debug('received {!r}'.format(data))

    # And when either an end-of-file marker is received or the connection is closed from the server’s side, the local transport object is closed and the future object is marked as done by setting a result.

    def eof_received(self):
        
        self.log.debug('received EOF')
        self.transport.close()
        
        if not self.f.done():
            self.f.set_result(True)

    def connection_lost(self, exc):
        
        self.log.debug('server closed connection')
        self.transport.close()
        
        if not self.f.done():
        
            self.f.set_result(True)
        
        super().connection_lost(exc)

# Normally the protocol class is passed to the event loop to create the connection. In this case, because the event loop has no facility for passing extra arguments to the protocol constructor, it is necessary to create a partial to wrap the client class and pass the list of messages to send and the Future instance. That new callable is then used in place of the class when calling create_connection() to establish the client connection.

client_completed = asyncio.Future()

client_factory = functools.partial(
    EchoClient,
    messages=MESSAGES,
    future=client_completed,
)

factory_coroutine = event_loop.create_connection(
    client_factory,
    *SERVER_ADDRESS,
)

# To trigger the client to run, the event loop is called once with the coroutine for creating the client and then again with the Future instance given to the client to communicate when it is finished. Using two calls like this avoids having an infinite loop in the client program, which likely wants to exit after it has finished communicating with the server. If only the first call was used to wait for the coroutine to create the client, it might not process all of the response data and clean up the connection to the server properly.

log.debug('waiting for client to complete')

try:
    
    event_loop.run_until_complete(factory_coroutine)
    event_loop.run_until_complete(client_completed)

finally:

    log.debug('closing event loop')
    event_loop.close()
    