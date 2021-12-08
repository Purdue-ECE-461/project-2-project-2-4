""" import requests

total_elapsed = 0
response_times_ms = []

for i in range(10):
    result = requests.get("https://ece-461-project-2-team-4.uc.r.appspot.com/package/package6")
    response_times_ms.append(result.elapsed.total_seconds() *1000)

print(response_times_ms) """

""" import asyncio
import aiohttp
from aiohttp import ClientSession

async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    return await resp.text()

async def make_requests(url: str, **kwargs) -> None:
    async with ClientSession() as session:
        tasks = []
        for i in range(1,10):
            tasks.append(
                fetch_html(url=url, session=session, **kwargs)
            )
        results = await asyncio.gather(*tasks)
        # do something with results

if __name__ == "__main__":
    asyncio.run(make_requests(url='https://ece-461-project-2-team-4.uc.r.appspot.com/package/package6')) """



import asyncio
import aiohttp


@asyncio.coroutine
def get_status(url):
    code = '000'
    try:
        res = yield from asyncio.wait_for(aiohttp.request('GET', url), 4)
        code = res.status
        res.close()
    except Exception as e:
        print(e)
    print(code)


if __name__ == "__main__":
    urls = ['https://google.com/'] * 5
    coros = [asyncio.Task(get_status(url)) for url in urls]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(coros))
    loop.close()