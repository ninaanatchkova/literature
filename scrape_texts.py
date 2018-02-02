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

liternet_links = read_poem_links_from_file("links/kadiiski_liternet_links.txt")

# create corpus
def create_corpus():
    for link in liternet_links:
        save_poem_text(link, "kadiiski.txt")


#scrape and save poem text - LITERNET
def save_poem_text(link, filename):
    tokens = []
    page = requests.get(link)
    encoding = page.headers['content-type'].split('charset=')[1]
    soup = BeautifulSoup(page.text, from_encoding="cp1252")

    # find poem title
    bolded = soup.find_all('b')
    title = bolded[5].getText().split()
    for word in title:
        tokens.append(word)

    # poem verses
    for p in soup.find_all('p'):
        links = p.find_all('a')
        font_tags = p.find_all('font')
        # get rid of meta text
        if len(links) > 0 or len(font_tags) > 0:
            continue
        else:
            words = p.getText().split()
            for word in words:
                word = word.replace("<br", "")
                tokens.append(word)

    create_project_dir("texts")
    path = "texts/" + filename
    if not os.path.exists(path):
        f = open(path, 'w', encoding='utf8')
        for token in tokens:
            f.write(token + " ")
        f.close()
    else:
        f = open(path, 'a', encoding='utf8')
        for token in tokens:
            f.write(token + " ")
        f.close()

# word list from corpus
def create_word_list(path):
    word_list = []
    with open (path, "r", encoding= "utf-8") as f:
        text = f.read()
        words = text.split()
        for word in words:
            word = clean_up_word(word)
            if len(word) > 0:
                word_list.append(word)
    return word_list

# clean up words from punctuation          
def clean_up_word(word):
    word = word.lower()
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
    with open("datasets/kadiiski_dict.csv", "w", newline="", encoding= "utf-8") as csvfile:
        fieldnames = ["word", "frequency"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key, value in sorted(word_count.items(), key=operator.itemgetter(1), reverse=True):
            writer.writerow({
                "word" : key,
                "frequency" : value
            })
        csvfile.close()

# Create dir
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating folder ' + directory)
        os.makedirs(directory)


############################## Execute functions ####################
# create_corpus()

word_list = create_word_list("texts/kadiiski.txt")
create_dictionary(word_list)