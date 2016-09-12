from bs4 import BeautifulSoup
import requests

def file_list(url, ext=''):
    li=[]

    page = requests.get(url).text

    # debug
    #print page

    soup = BeautifulSoup(page, 'html.parser')

    for node in soup.find_all('a'):
        if node.get('href').endswith(ext):
            li.append(url + '/' + node.get('href'))

    return li

url = 'http://clarkstars.grtv.im/transmission'
ext = 'mkv'

for f in file_list(url, ext):
    print f
