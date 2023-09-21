import requests
import threading
import multiprocessing
import asyncio
import aiohttp

import sys
import time
from pathlib import Path
from os import path

urls = sys.argv[1:]

images_path = Path('./img/')


def download_thread(urls):
    start_time = time.time()
    threads = []
    for url in urls:
        t = threading.Thread(target=download_img, args=(url,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    download_time = time.time() - start_time
    print(f'Downloading by threading complited in {download_time:.2f}')
    
def download_processing(urls):
    start_time = time.time()
    processes = []
    for url in urls:
        p = multiprocessing.Process(target=download_img, args=(url,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    download_time = time.time() - start_time
    print(f'Downloading by multiprocessing complited in {download_time:.2f}')


def download_img(url):
    start_time = time.time()
    response = requests.get(url)
    filename = images_path.joinpath(path.basename(url))
    with open(filename, 'wb') as f:
        f.write(response.content)
    download_time = time.time() - start_time
    print(f'Image {filename} downloaded in {download_time:.2f}')
    
    
async def download_async(urls):
    start_time = time.time()
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(download_img_async(url))
        tasks.append(task)
    await asyncio.gather(*tasks)
    download_time = time.time() - start_time
    print(f'Downloading by asyncio complited in {download_time:.2f}')


async def download_img_async(url):
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            img = await response.read()
            filename = images_path.joinpath(path.basename(url))
            with open(filename, 'wb') as f:
                f.write(img)
            download_time = time.time() - start_time
            print(f'Image {filename} downloaded in {download_time:.2f}')    
    
if __name__ == '__main__':
    if urls:
        print('Start downloading by threading')
        download_thread(urls)
        print('Start downloading by multiprocessing')
        download_processing(urls)
        print('Start downloading by asyncio')
        loop = asyncio.get_event_loop()
        loop.run_until_complete(download_async(urls))
    else:
        print('No urls to download')