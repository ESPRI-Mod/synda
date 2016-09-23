import bs4
import requests
import argparse

def file_list(url, ext=''):
    li=[]

    page = requests.get(url).text

    # debug
    #print page

    soup = bs4.BeautifulSoup(page, 'html.parser')

    for node in soup.find_all('a'):
        if node.get('href').endswith(ext):
            li.append(url + '/' + node.get('href'))

    return li

url = 'http://hydrology.princeton.edu/data/efwood/SWICCA/CMIP5/rcp45/2057-2099/bc_pr'
ext = 'nc'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    for f in file_list(url, ext):
        print f
