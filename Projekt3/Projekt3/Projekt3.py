import gzip
import json
import requests
import sys
from bs4 import BeautifulSoup
from os.path import join

url='https://www.jeja.pl/'

def main():
    if len(sys.argv) < 2:
        sys.exit('Nie podano nazwy pliku JSON do zapisu danych.')
    file=''
    if sys.argv[1][-5:] != '.json':
        file=sys.argv[1]+'.json'
    else: file=sys.argv[1]
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    
    divs_posts = soup.find_all('div', class_='ob-left-box ob-left-box-images')
    h2s_titles=[post.find('h2').find('a').text for post in divs_posts]
    votes_up = [post.find('div', class_='star-box') for post in divs_posts]
    votes_down = [votes.find('a', class_='votedown').find('span').text for votes in votes_up]
    votes_up = [votes.find('a', class_='voteup').find('span').text for votes in votes_up]
    
    x={h2s_titles[i]: (votes_up[i],votes_down[i]) for i in range(len(h2s_titles))}
    
    with open(file,'w', encoding='utf-8') as f:
        json.dump(x,f)

    print(x)
    with open(file, 'r', encoding='utf-8') as f:
        print(json.load(f))



if __name__ == "__main__":
    main()