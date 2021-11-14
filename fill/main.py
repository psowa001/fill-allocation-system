import asyncio
import random
from aiohttp import ClientSession, ClientConnectionError


async def process():
    stock = ["AXA", "ABC", "BCD", "CDE", "DEF", "EFG", "FGH", "GHI", "HIJ", "IJK"]
    while True:
        tick = dict(
            stock = random.choice(stock),
            price = random.randint(1, 100),
            quantity = random.randint(1, 100)
        )

        await asyncio.sleep(random.randint(1, 30))

        async with ClientSession() as session:
            try:
                async with session.post("http://controller:8080/fill/", json=tick, ssl=False) as response:
                    response = await response.read()
            except ClientConnectionError as e:
                    print('Connection Error', str(e))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process())
    loop.run_forever()