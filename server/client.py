import socket
import asyncio
import threading
import aioconsole

from config import Config

sock = socket.socket()
sock.connect(('localhost', Config.PORT))
sock.setblocking(False)


async def listen_server(sock):
    loop = asyncio.get_event_loop()

    request = None
    while request != 'quit':
        response = (await loop.sock_recv(sock, 255)).decode('utf8')
        print('\n' + response + '\n')


async def write_server(sock):
    loop = asyncio.get_event_loop()

    while True:
        line = await aioconsole.ainput()
        await loop.sock_sendall(sock, line.encode())
        await asyncio.sleep(1)


async def main(sock):
    loop = asyncio.get_event_loop()

    lst = loop.create_task(listen_server(sock))
    wrt = loop.create_task(write_server(sock))

    await asyncio.gather(lst, wrt)

asyncio.run(main(sock))

sock.close()
