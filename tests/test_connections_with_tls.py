import asyncio

from sayd import SaydServer, SaydClient


pytest_plugins = ("pytest_asyncio",)


server: SaydServer = SaydServer(cert="cert.crt", cert_key="cert.key", port=7050)

server_messages: str = 0
clients_messages: str = 0

clients: list = []


@server.callback("message")
async def server_message(address: tuple, instance: str, data: dict) -> None:
    global server_messages

    await server.call(name="message", address=address)

    server_messages += 1


async def client_message(instance: str, data: dict) -> None:
    global clients_messages

    clients_messages += 1


async def test() -> None:
    global server_messages
    global clients_messages


    await server.start()


    for _ in range(128):
        client: SaydClient = SaydClient(cert="cert.crt", port=7050)
        client.add_callback("message", client_message)
        clients.append(client)

        await client.start()

    
    for _ in clients:
        await _.call("message")


    await asyncio.sleep(6)

    assert client.connected
    assert server_messages == 128
    assert clients_messages == 128
    clients_messages = 0


    await server.call("message")


    await asyncio.sleep(3)


    assert clients_messages == 128


    for _ in clients:
        await _.stop()


    await server.stop()


    await asyncio.sleep(1)
