import logging
import asyncio, socket

from config import Config

CLIENTS = []


async def handle_client(client):
    loop = asyncio.get_event_loop()

    request = None
    while request != 'quit':
        request = (await loop.sock_recv(client, 255)).decode('utf8')

        try:
            message = f'{client.getpeername()[0]} : ' + request
            logging.warning(message)
        except Exception:
            client.close()
            CLIENTS.remove(client)

        for other_client in CLIENTS:
            await loop.sock_sendall(other_client, message.encode('utf8'))


async def run_server():
    server = socket.socket()
    server.bind((Config.HOST, Config.PORT))
    server.listen(100)
    server.setblocking(False)

    loop = asyncio.get_event_loop()

    while True:
        client, _ = await loop.sock_accept(server)
        CLIENTS.append(client)
        loop.create_task(handle_client(client))


def main():
    asyncio.run(run_server())


if __name__ == '__main__':
    main()
