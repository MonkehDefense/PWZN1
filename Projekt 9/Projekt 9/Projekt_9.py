import asyncio
import aiohttp
import aiofiles
import async_timeout
from bs4 import BeautifulSoup
import multiprocessing as mp
import requests
import cv2
from concurrent.futures import ProcessPoolExecutor
from os import listdir
from os.path import join

def initiate(url):
	req = requests.get(url)
	soup = BeautifulSoup(req.text, 'html.parser')
	del req

	a_posts = soup.find_all('a')
	a_posts = [post['href'] for post in a_posts if post.text[-4:]=='.png']
	return a_posts

async def dload(url, file):
	"""
	download + grayscale
	"""
	#print(file)
	async with aiohttp.ClientSession() as session:
		async with session.get(url + file) as resp:
			f = await aiofiles.open(join('.','obrazy',file), mode = 'wb')
			await f.write(await resp.read())
			await f.close()
	#grayscale
#	img = cv2.imread(path)
#	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#	cv2.imwrite(path,img)

async def main():
	url = 'http://if.pw.edu.pl/~mrow/dyd/wdprir/'
	images = initiate(url)
	await asyncio.gather(*[dload(url,img) for img in images])

	for filename in listdir(join('.','obrazy')):
		if not filename.endswith('.png'):
			continue
		img = cv2.imread(join('.','obrazy',filename))
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		cv2.imwrite(join('.','obrazy',filename),img)

asyncio.run(main())


