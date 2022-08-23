from asyncio import sleep

from sayd import SaydServer, SaydClient


pytest_plugins = ("pytest_asyncio",)

server: SaydServer = SaydServer()


@server.callback("message")
async def server_message(address: tuple, instance: str, data: dict) -> dict:
    return {}

async def client_message(instance: str, data: dict) -> dict:
    return {}


async def test() -> None:
    clients: list = []

    clients_responses: list = []
    server_responses: list = []

    response: Union[dict, None]

    
    await server.start()

    for _ in range(128):
        client: SaydClient = SaydClient(port="7050")

        client.add_callback("message", client_message)
        clients.append(client)

        await client.start()

    await sleep(3)
    
    
    for _ in clients:
        response = await _.call("message")

        if isinstance(response, dict):
            clients_responses.append(response)
    
    server_responses = await server.call("message")


    assert len(clients_responses) == 128
    assert len(server_responses) == 128


    server_responses.clear()

    for _ in server.clients:
        response = await server.call("message", address=_)

        if isinstance(response, dict):
            server_responses.append(response)

    
    assert len(server_responses) == 128

    
    for _ in clients:
        await _.stop()

    await server.stop()
