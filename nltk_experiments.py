import nltk
from nltk.tokenize import word_tokenize
from nltk.text import Text
from nltk import FreqDist
import io
import csv
import itertools


# clean up words from punctuation          
def clean_up_word(word):
    accepted_characters = "абвгдежзийклмнопрстуфхцчшщъьюяѝ"
    word = word.lower()
    for c in list(word):
        if c not in list(accepted_characters):
            word = word.replace(c, "")
    return word


def tokenize_text(path):
    f = io.open(path, mode="r", encoding="utf-8")
    raw = f.read()
    tokens = nltk.word_tokenize(raw)
    words = []
    for token in tokens:
        word = clean_up_word(token)
        if len(word) > 0:
            words.append(word)
    text = nltk.Text(words)
    return text

def get_top_words_from_csv(path):
    reader = csv.reader(open(path, 'r', encoding= "utf-8"))
    freq_dictionary = {}
    next(reader)
    for row in itertools.islice(reader, 50):
        k, v = row
        freq_dictionary[k] = v
    word_list = []
    for key in freq_dictionary.keys():
        word_list.append(key)
    return word_list

def get_top_words_from_bg_freq_dict():
    reader = csv.reader(open('datasets/D-Fiction0001_byFreq.csv', 'r', encoding= "utf-8"))
    freq_dictionary = {}
    for row in itertools.islice(reader, 50):
        row_text = row
        k_v = row_text[0].split("\t")
        k = k_v[0]
        v = k_v[1]
        print(row_text)
        freq_dictionary[k] = v
    word_list = []
    for key in freq_dictionary.keys():
        word_list.append(key)
    return word_list

def plot_dispersions_for_text(text, path):
    top_text_words = get_top_words_from_csv(path)
    top_dict_words = get_top_words_from_bg_freq_dict()
    text.dispersion_plot(top_text_words)
    text.dispersion_plot(top_dict_words)
    

def plot_frequency_distribution(text):
    freq_dist = FreqDist(text)
    print(freq_dist.most_common(50))
    freq_dist.plot(50, cumulative=True)
