import requests
import lxml
from bs4 import BeautifulSoup

def get_poem_vocabulary(link):
    page = requests.get(link)
    encoding = page.headers['content-type'].split('charset=')[1]
    soup = BeautifulSoup(page.text, from_encoding="cp1252")
    bolded = soup.find_all('b')
    print(bolded[5].getText())
    for p in soup.find_all('p'):
        links = p.find_all('a')
        font_tags = p.find_all('font')
        if len(links) > 0 or len(font_tags) > 0:
            continue
        else:
            print(p.getText())

# get_poem_vocabulary("https://liternet.bg/publish11/k_kadiiski/ezdach/treva1.htm")