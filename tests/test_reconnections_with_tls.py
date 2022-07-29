import asyncio
import pytest

from sayd import SaydServer, SaydClient


pytest_plugins = ("pytest_asyncio",)


server: SaydServer = SaydServer(cert="cert.crt", cert_key="cert.key")

clients_messages: str = 0

clients: list = []


async def client_message(instance: str, data: dict) -> None:
    global clients_messages

    clients_messages += 1


async def test() -> None:
    global clients_messages


    await server.start()


    for _ in range(128):
        client: SaydClient = SaydClient(cert="cert.crt")
        client.add_callback("message", client_message)
        clients.append(client)

        await client.start()

    
    await asyncio.sleep(2)

    await server.stop()

    
    while client.connected:
        await asyncio.sleep(1)


    await server.start()

    await asyncio.sleep(8)


    await server.call("message")
    await server.call(name="message", address=server.clients.pop())

    await asyncio.sleep(2)

    assert clients_messages == 129


    for _ in clients:
        await _.stop()


    await server.stop()


    await asyncio.sleep(1)
