from asyncio import sleep

from sayd import SaydServer, SaydClient


pytest_plugins = ("pytest_asyncio",)

server: SaydServer = SaydServer()


server_messages: int = 0
clients_messages: int = 0


@server.callback("message")
async def server_message(address: tuple, instance: str, data: dict) -> dict:
    global server_messages
    server_messages += 1

async def client_message(instance: str, data: dict) -> dict:
    global clients_messages
    clients_messages += 1


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


    for _ in clients:
        response = await _.call("message", wait=False)

        if isinstance(response, dict):
            clients_responses.append(response)
    
    server_responses = await server.call("message", wait=False)

    
    await sleep(3)
        
    assert _.connected
    
    assert len(clients_responses) == 0
    assert server_responses is True

    assert server_messages == 128
    assert clients_messages == 128

    
    for _ in clients:
        await _.stop()

    await server.stop()
