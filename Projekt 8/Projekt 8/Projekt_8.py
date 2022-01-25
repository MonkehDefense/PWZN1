import multiprocessing as mp
import requests
import shutil
import cv2
from concurrent.futures import ProcessPoolExecutor
from os.path import join
from bs4 import BeautifulSoup

#initial setup - scraping png links
url = 'http://if.pw.edu.pl/~mrow/dyd/wdprir/'
def initiate():
	req = requests.get(url)
	soup = BeautifulSoup(req.text, 'html.parser')
	del req

	a_posts = soup.find_all('a')
	a_posts = [post['href'] for post in a_posts if post.text[-4:]=='.png']
	return a_posts

#process
def dld_gsc(file):
	"""
	download + grayscale
	"""
	print(file)
	r = requests.get(url + file,stream = True).content
	path=join('.','obrazy',file)
	with open(path,'wb') as f:
		f.write(r)
	del r
	#grayscale
	img = cv2.imread(path)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	cv2.imwrite(path,img)
	

if __name__ == '__main__':
	images = initiate()
	pool = ProcessPoolExecutor(len(images))
	for img in images:
		print(img)
		pool.submit(dld_gsc,img)