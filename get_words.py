import requests
import lxml
import io
import os
import operator
import csv
from bs4 import BeautifulSoup

# get scraping links
def read_poem_links_from_file(path):
    poem_links = []
    if os.path.exists(path):
        poem_links = [line.strip() for line in open(path)]
    return poem_links

# get words from poem page
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
    return word_list

#get poem text
def get_poem_text(link):
    text = ""
    page = requests.get(link)
    encoding = page.headers['content-type'].split('charset=')[1]
    soup = BeautifulSoup(page.text, from_encoding="cp1252")
    bolded = soup.find_all('b')
    title = bolded[5].getText()
    text += title
    for p in soup.find_all('p'):
        links = p.find_all('a')
        font_tags = p.find_all('font')
        if len(links) > 0 or len(font_tags) > 0:
            continue
        else:
            text += " " + p.getText()
    return text

# clean up words from punctuation          
def clean_up_word(word):
    accepted_characters = "абвгдежзийклмнопрстуфхцчшщъьюяѝ"
    for c in list(word):
        if c not in list(accepted_characters):
            word = word.replace(c, "")
    return word

# create dictionary from word list
def create_dictionary(word_list):
    word_count = {}
    for word in word_list:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    with open("datasets/poems_set.csv", "w", newline="", encoding= "utf-8") as csvfile:
        fieldnames = ["word", "frequency"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key, value in sorted(word_count.items(), key=operator.itemgetter(1), reverse=True):
            writer.writerow({
                "word" : key,
                "frequency" : value
            })
        csvfile.close()

# amass a wordlist from all poems
def get_all_poems_words(path):
    word_list = []
    links = read_poem_links_from_file(path)
    for link in links:
        word_list.extend(get_poem_vocabulary(link))
    return word_list

def get_all_text(path):
    links = read_poem_links_from_file(path)
    with io.open("datasets/poems_text.txt", 'w', encoding='utf8') as f:
        for link in links:
            f.write(get_poem_text(link))
    f.close()
    
# create final frequency dictionary
def get_complete_dictionary(path):
    word_list = get_all_poems_words(path)
    print(word_list)
    create_dictionary(word_list)


# get_complete_dictionary("links/poetry_links.txt")
# print(get_poem_text("https://liternet.bg/publish11/k_kadiiski/ezdach/gong.htm"))
get_all_text("links/poetry_links.txt")
