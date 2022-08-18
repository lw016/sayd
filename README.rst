Sayd
====
*A performant asynchronous communication protocol in pure Python.*

This library was developed with simplicity and performance in mind, with modern practices of Python development, currently in a test state.

`Documentation Reference <https://sayd.readthedocs.io>`_


Install
-------
Works on Python 3.7.4+, is highly recommended to have installed `ujson <https://github.com/ultrajson/ultrajson>`_ and `uvloop <https://github.com/MagicStack/uvloop>`_ for a performance boost.

.. code-block:: bash

    pip install sayd


Optional
^^^^^^^^^^
.. code-block:: bash

    pip install ujson uvloop


Development
-----------
You need to have installed `poetry <https://github.com/python-poetry/poetry>`_ for dependencies management (`how to <https://python-poetry.org/docs/#installation>`_).

.. code-block:: bash

    git clone https://github.com/lw016/sayd
    cd sayd
    poetry install


Run the tests
^^^^^^^^^^^^^^
To run all the tests is required to have installed the Python versions 3.7, 3.8, 3.9 and 3.10.

.. code-block:: bash

    poetry run tox -e tests-py[37/38/39/310]

Build the docs
^^^^^^^^^^^^^^^
.. code-block:: bash

    poetry run tox -e docs


Features
--------
- Client and server implementations
- Reliable TCP persistent connection
- Auto reconnection
- Multiple asynchronous connections *(server)*
- Blacklist of clients *(server)*
- TLS encryption
- Data transmitted as dictionaries *(json)*
- Broadcast *(server)*
- Remote function callbacks
- Built-in CLI utility to generate self-signed certificates


Roadmap
-------
- Add support to Unix socket
- Implement TLS certificate authentication


CLI
---
The built-in CLI utility (*sayd*) can be used to generate self-signed certificates to encrypt the connection. Optionally you can install `rich <https://github.com/Textualize/rich>`_ to have a pretty CLI output.

.. code-block:: bash

    sayd --help


Usage example
-------------
Server
^^^^^^
.. code-block:: python

    import logging
    import asyncio

    from sayd import SaydServer


    logging.basicConfig(
            format="[%(name)s][%(levelname)s] %(asctime)s - %(message)s",
            datefmt="%Y/%m/%d %H:%M:%S"
            )

    logger = logging.getLogger("SERVER")
    logger.setLevel(logging.INFO)


    server = SaydServer(logger=logger)


    @server.callback("message")
    async def msg(address: tuple, instance: str, data: dict) -> dict:
        return {"greetings": "Hello there!"}


    async def main() -> None:
        await server.start()
        
        
        while True:
            result = await server.call("message", {"greetings": "Hi!"}) # Broadcast call.
            print(result)

            await asyncio.sleep(1)
        
        
        await server.stop()


    if __name__ == "__main__":
        asyncio.run(main())

Client
^^^^^^
.. code-block:: python

    import logging
    import asyncio

    from sayd import SaydClient


    logging.basicConfig(
            format="[%(name)s][%(levelname)s] %(asctime)s - %(message)s",
            datefmt="%Y/%m/%d %H:%M:%S"
            )

    logger = logging.getLogger("CLIENT")
    logger.setLevel(logging.INFO)


    client = SaydClient(logger=logger)


    @client.callback("message")
    async def msg(instance: str, data: dict) -> dict:
        return {"greetings": "Hello there!"}


    async def main() -> None:
        await client.start()


        while True:
            result = await client.call("message", {"greetings": "Hi!"})
            print(result)

            await asyncio.sleep(1)

        
        await client.stop()


    if __name__ == "__main__":
        asyncio.run(main())
