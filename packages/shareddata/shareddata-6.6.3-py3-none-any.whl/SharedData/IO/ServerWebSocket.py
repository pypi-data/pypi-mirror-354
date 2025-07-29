
import time
import sys
import time
import asyncio
import websockets
import json
import os
from cryptography.fernet import Fernet

from SharedData.IO.SyncTable import SyncTable

# TODO: DONT SERVE DATA IF TABLE IS NOT IN MEMORY
class ServerWebSocket():

    """
    ServerWebSocket is an asynchronous WebSocket server class that manages client connections, authentication, and data synchronization.
    
    Attributes:
        BUFF_SIZE (int): Buffer size for data transfer, set to 128 KB.
        clients (dict): A dictionary tracking all connected client sockets and their metadata.
        lock (asyncio.Lock): An asynchronous lock to ensure thread-safe access to the clients dictionary.
        server: The WebSocket server instance.
        accept_clients: Placeholder for client acceptance control (not implemented).
    
    Methods:
        runserver(shdata, host, port):
            Starts the WebSocket server on the specified host and port, and listens for incoming client connections.
    
        handle_client_thread(conn, path):
            Handles a new client connection, adds the client to the clients dictionary, and manages client lifecycle including disconnection.
    
        handle_client_websocket(client):
            Manages the WebSocket communication with an authenticated client, including receiving login data, authenticating using a token,
            and handling client actions such as subscribing or publishing to a synchronized table.
    
    The server authenticates clients using a token encrypted with Fernet symmetric encryption. Upon successful authentication,
    clients can subscribe to or publish data to shared tables, with synchronization handled by the SyncTable class.
    """
    BUFF_SIZE = int(128*1024)
    
    # Dict to keep track of all connected client sockets
    clients = {}
    # Create a lock to protect access to the clients Dict
    lock = asyncio.Lock()
    server = None
    accept_clients = None

    @staticmethod
    async def runserver(shdata, host, port):

        """
        Starts an asynchronous WebSocket server that listens on the specified host and port.
        
        This static method initializes the server with shared data, logs the listening address,
        and begins handling incoming client connections using the `handle_client_thread` coroutine.
        The server runs until it is explicitly closed.
        
        Parameters:
            shdata (Any): Shared data to be used by the server and client handlers.
            host (str): The hostname or IP address on which the server will listen.
            port (int): The port number on which the server will listen.
        
        Returns:
            None
        """
        Logger.log.info(f'Listening on {host}:{port}')

        ServerWebSocket.shdata = shdata

        ServerWebSocket.server = await websockets.serve(ServerWebSocket.handle_client_thread, host, port)

        await ServerWebSocket.server.wait_closed()

    @staticmethod
    async def handle_client_thread(conn, path):
        """
        Asynchronously handles a new client connection by registering the client, managing its lifecycle, and processing communication.
        
        This static method performs the following steps:
        - Logs the new client connection.
        - Adds the client connection to the shared clients dictionary with initial metadata.
        - Calls the main client websocket handler to process client messages.
        - Handles any exceptions during client communication by logging errors.
        - Ensures the client is removed from the clients dictionary and the connection is closed upon disconnection.
        
        Args:
            conn: The client connection object representing the websocket connection.
            path: The request path associated with the websocket connection.
        """
        addr = conn.remote_address
        Logger.log.info(f"New client connected: {addr}")
        # conn.settimeout(60.0)

        # Add the client socket to the list of connected clients
        async with ServerWebSocket.lock:
            ServerWebSocket.clients[conn] = {
                'watchdog': time.time_ns(),
                'transfer_rate': 0.0,
            }

        client = ServerWebSocket.clients[conn]
        client['conn'] = conn
        client['addr'] = addr

        try:
            await ServerWebSocket.handle_client_websocket(client)
        except Exception as e:
            Logger.log.error(f"Client {addr} disconnected with error: {e}")
        finally:
            async with ServerWebSocket.lock:
                ServerWebSocket.clients.pop(conn)
            Logger.log.info(f"Client {addr} disconnected.")
            conn.close()

    @staticmethod
    async def handle_client_websocket(client):

        """
        Asynchronously handles a WebSocket client connection by authenticating the client using a token, updating client state, and managing subscription or publication actions on a synchronized table.
        
        Parameters:
            client (dict): A dictionary containing client information, including the WebSocket connection under 'conn' and client address under 'addr'.
        
        Behavior:
            - Receives and decodes a login message from the client.
            - Decrypts and verifies the authentication token against an environment variable.
            - Logs authentication success or failure.
            - Updates the client dictionary with login message data.
            - Initializes the client for synchronization.
            - Depending on the client's requested action ('subscribe' or 'publish') and container type ('table'), enters the appropriate asynchronous loop to handle data publishing or subscription.
        
        Raises:
            Exception: If client authentication fails.
        """
        client['authenticated'] = False
        conn = client['conn']

        # Receive data from the client
        data = await conn.recv()
        if data:
            # clear watchdog
            client['watchdog'] = time.time_ns()
            data = data.decode()
            login_msg = json.loads(data)
            # authenticate
            key = os.environ['SHAREDDATA_SECRET_KEY'].encode()
            token = os.environ['SHAREDDATA_TOKEN']
            cipher_suite = Fernet(key)
            received_token = cipher_suite.decrypt(login_msg['token'].encode())
            if received_token.decode() != token:
                errmsg = 'Client %s authentication failed!' % (
                    client['addr'][0])
                Logger.log.error(errmsg)
                raise Exception(errmsg)
            else:
                client['authenticated'] = True
                Logger.log.info('Client %s authenticated' %
                                (client['addr'][0]))

                client.update(login_msg) # load client message
                client = SyncTable.init_client(client)
                if client['action'] == 'subscribe':
                    if client['container'] == 'table':
                        await SyncTable.websocket_publish_loop(client)
                elif client['action'] == 'publish':
                    if client['container'] == 'table':
                        # reply with mtime and count
                        responsemsg = {
                            'mtime': float(client['records'].mtime),
                            'count': int(client['records'].count),
                        }
                        await conn.send(json.dumps(responsemsg))
                        await SyncTable.websocket_subscription_loop(client)

async def send_heartbeat():
    """
    Asynchronously sends periodic heartbeat logs containing the number of connected clients and their aggregate upload and download speeds.
    
    This coroutine continuously monitors all connected clients in the ServerWebSocket.clients dictionary, calculates the total upload and download bytes transferred since the last heartbeat, computes the transfer rates in MB/s, and logs this information every 15 seconds.
    
    The logged message includes the host, port, number of clients, download speed, and upload speed.
    
    Requires:
    - ServerWebSocket.clients: a dictionary mapping client identifiers to dictionaries containing 'upload' and 'download' byte counts.
    - Logger.log.debug: a logging method for debug messages.
    - `host` and `port` variables to be defined in the surrounding scope.
    - asyncio and time modules for asynchronous sleeping and time measurement.
    """
    lasttotalupload = 0
    lasttotaldownload = 0
    lasttime = time.time()
    while True:
        # Create a list of keys before entering the loop
        client_keys = list(ServerWebSocket.clients.keys())
        nclients = 0
        totalupload = 0
        totaldownload = 0
        for client_key in client_keys:
            nclients = nclients+1
            c = ServerWebSocket.clients.get(client_key)
            if c is not None:
                if 'upload' in c:
                    totalupload += c['upload']
                
                if 'download' in c:
                    totaldownload += c['download']
                
        te = time.time()-lasttime
        lasttime = time.time()
        download = (totaldownload-lasttotaldownload)/te
        upload = (totalupload-lasttotalupload)/te
        lasttotaldownload = totaldownload
        lasttotalupload = totalupload        

        Logger.log.debug('#heartbeat#host:%s,port:%i,clients:%i,download:%.2fMB/s,upload:%.2fMB/s' \
                         % (host, port, nclients, download/1024, upload/1024))        
        await asyncio.sleep(15)

async def main():
    """
    Asynchronously runs the main application by concurrently starting the WebSocket server and sending heartbeat signals.
    
    This function uses asyncio.gather to run the ServerWebSocket server with the provided shared data, host, and port,
    while simultaneously running the send_heartbeat coroutine to maintain connection health.
    
    Requires:
    - ServerWebSocket.runserver(shdata, host, port): Coroutine to start the WebSocket server.
    - send_heartbeat(): Coroutine to send periodic heartbeat messages.
    """
    await asyncio.gather(
        ServerWebSocket.runserver(shdata, host, port),
        send_heartbeat()
    )

if __name__ == '__main__':

    from SharedData.Logger import Logger
    from SharedData.SharedData import SharedData
    shdata = SharedData('SharedData.IO.ServerWebSocket', user='master')
    SyncTable.shdata = shdata
    
    if len(sys.argv) >= 2:
        _argv = sys.argv[1:]
    else:
        msg = 'Please specify IP and port to bind!'
        Logger.log.error(msg)
        raise Exception(msg)
    
    args = _argv[0].split(',')
    host = args[0]
    port = int(args[1])    
    
    Logger.log.info('ROUTINE STARTED!')
    
    asyncio.run(main())
