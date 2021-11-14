import asyncio
import numpy
from aiohttp import ClientSession, ClientConnectionError


async def process(delay = 30):
    accounts = dict()
    iter = 2

    while True:
        account_shares = numpy.random.dirichlet(numpy.ones(iter), size=1)[0]
        for i in range(iter):
            account_name = "account" + str(i+1)
            accounts[account_name] = round(account_shares[i] * 100)
        
            await asyncio.sleep(delay)

            async with ClientSession() as session:
                try:
                    async with session.post("http://controller:8080/aum/", json=accounts, ssl=False) as response:
                        response = await response.read()
                except ClientConnectionError as e:
                    print('Connection Error', str(e))

        iter += 1


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process())
    loop.run_forever()