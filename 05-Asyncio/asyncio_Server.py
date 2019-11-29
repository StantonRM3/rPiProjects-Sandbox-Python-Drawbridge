#!/usr/bin/env python3
# asyncio_echo_server_protocol.py
# https://pymotw.com/3/asyncio/io_protocol.html
# 
import asyncio
import logging
import sys

SERVER_ADDRESS = ('localhost', 66666)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)

log = logging.getLogger('main')

event_loop = asyncio.get_event_loop()

# It then defines a subclass of asyncio.Protocol to handle client
# communication. The protocol object’s methods are invoked based on
# events associated with the server socket.

class EchoServer(asyncio.Protocol):

    # Each new client connection triggers a call to connection_made().
    # The transport argument is an instance of asyncio.Transport,
    # which provides an abstraction for doing asynchronous I/O using
    # the socket. Different types of communication provide different
    # transport implementations, all with the same API. For example,
    # there are separate transport classes for working with sockets
    # and for working with pipes to subprocesses. The address of the
    # incoming client is available from the transport through
    # get_extra_info(), an implementation-specific method.

    def connection_made(self, transport):
        
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.log = logging.getLogger(
            'EchoServer_{}_{}'.format(*self.address)
        )
        self.log.debug('connection accepted')

    # After a connection is established, when data is sent from the
    # client to the server the data_received() method of the protocol
    # is invoked to pass the data in for processing. Data is passed as
    # a byte string, and it is up to the application to decode it in
    # an appropriate way. Here the results are logged, and then a
    # response is sent back to the client immediately by calling
    # transport.write().

    def data_received(self, data):
        
        self.log.debug('received {!r}'.format(data))
        self.transport.write(data)
        self.log.debug('sent {!r}'.format(data))

    # Some transports support a special end-of-file indicator (“EOF”).
    # When an EOF is encountered, the eof_received() method is called.
    # In this implementation, the EOF is sent back to the client to
    # indicate that it was received. Because not all transports support
    # an explicit EOF, this protocol asks the transport first whether
    # it is safe to send EOF.

    def eof_received(self):
        
        self.log.debug('received EOF')
        
        if self.transport.can_write_eof():
            self.transport.write_eof()
            
    # When a connection is closed, either normally or as the result of
    # an error, the protocol’s connection_lost() method is called. If
    # there was an error, the argument contains an appropriate exception
    # object. Otherwise it is None.

    def connection_lost(self, error):
        
        if error:
            
            self.log.error('ERROR: {}'.format(error))
            
        else:
            
            self.log.debug('closing')
            
        super().connection_lost(error)
        
    # There are two steps to starting the server. First the application
    # tells the event loop to create a new server object using the
    # protocol class and the hostname and socket on which to listen.
    # The create_server() method is a coroutine, so the results must
    # be processed by the event loop in order to actually start the
    # server. Completing the coroutine produces a asyncio.Server
    # instance tied to the event loop.

# Create the server and let the loop finish the coroutine before
# starting the real event loop.

factory = event_loop.create_server(EchoServer, *SERVER_ADDRESS)
server = event_loop.run_until_complete(factory)

log.debug('starting up on {} port {}'.format(*SERVER_ADDRESS))

# Then the event loop needs to be run in order to process events and
# handle client requests. For a long-running service, the run_forever()
# method is the simplest way to do this. When the event loop is stopped,
# either by the application code or by signaling the process, the server
# can be closed to clean up the socket properly, and then the event loop
# can be closed to finish handling any other coroutines before the
# program exits.

# Enter the event loop permanently to handle all connections.
try:
    
    event_loop.run_forever()

finally:
    
    log.debug('closing server')
    
    server.close()
    
    event_loop.run_until_complete(server.wait_closed())
    log.debug('closing event loop')
    
    event_loop.close()
    