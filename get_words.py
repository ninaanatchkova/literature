import requests
import lxml
import operator
from bs4 import BeautifulSoup

def get_poem_vocabulary(link):
    word_list = []
    page = requests.get(link)
    encoding = page.headers['content-type'].split('charset=')[1]
    soup = BeautifulSoup(page.text, from_encoding="cp1252")
    bolded = soup.find_all('b')
    title = bolded[5].getText().lower().split()
    for word in title:
        word = clean_up_word(word)
        if len(word) > 0:
            word_list.append(word)
    for p in soup.find_all('p'):
        links = p.find_all('a')
        font_tags = p.find_all('font')
        if len(links) > 0 or len(font_tags) > 0:
            continue
        else:
            words = p.getText().lower().split()
            for word in words:
                word = clean_up_word(word)
                if len(word) > 0:
                    word_list.append(word)
    return(word_list)

            
def clean_up_word(word):
    accepted_characters = "абвгдежзийклмнопрстуфхцчшщъьюяѝ"
    for c in list(word):
        if c not in list(accepted_characters):
            word = word.replace(c, "")
    return(word)

def create_dictionary(list):
    word_count = {}
    for word in list:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    for key, value in sorted(word_count.items(), key=operator.itemgetter(1), reverse=True):
        print(key, value)

word_list = get_poem_vocabulary("https://liternet.bg/publish11/k_kadiiski/ezdach/treva1.htm")
create_dictionary(word_list)