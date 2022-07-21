
import re
import ssl
import certifi
import asyncio
import aiohttp
from bs4 import BeautifulSoup


jookes_list = []


async def get_page_info(session, page: int, start_page: int):
    global jookes_list

    if page == start_page:
        url = 'https://anekdotov.net/'
    else:
        url =f'https://anekdotov.net/arc/{page}.html'

        async with session.get(url=url) as response:
            try:
                response_text = response.text()
                html_sourse = response_text

                page_info = BeautifulSoup(html_sourse, 'html.parser')

                jookes = page_info.find_all('div', class_='anekdot')
                for jooke in jookes:
                    jookes_list.append(jooke.text)

            except Exception as ex:
                print(f' Error:  {repr(ex)}')


async def load_site_info():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)

    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.get(url='https://anekdotov.net/') as response:
            try:
                response_text = await response.text()
                html_sourse = response_text


                page_info = BeautifulSoup(html_sourse, 'html.parser')

                page = page_info.find_all('a', string='Д А Л Е Е!', href=True)
                for href in page:
                    count_of_page = int(re.sub('[\\D]', '', href['href']))
            except Exception as ex:
                print(f' Error:  {repr(ex)}')
    tasks = []
    for page in range(count_of_page - 10, count_of_page):
        task_1 = asyncio.create_task(get_page_info(session=session, page=page, start_page=count_of_page))
        tasks.append(task_1)

    await asyncio.gather(*tasks)


async def run_tasks():
    global jookes_list

    await load_site_info()
    for joke in jookes_list:
        print(joke, '\n\n')
    # print(len(jookes_list))


if __name__ == '__main__':
    result = asyncio.get_event_loop().run_until_complete(run_tasks())
