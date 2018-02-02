import nltk
from nltk.tokenize import word_tokenize
from nltk.text import Text
from nltk import FreqDist
import io
import csv
import itertools
import numpy as np
import matplotlib.pyplot as plt


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
        words.append(token)
    text = nltk.Text(words)
    return text

def clean_text(path):
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

def get_top_words_from_csv(path, number_of_words):
    reader = csv.reader(open(path, 'r', encoding= "utf-8"))
    freq_dictionary = {}
    next(reader)
    for row in itertools.islice(reader, number_of_words):
        k, v = row
        freq_dictionary[k] = v
    word_list = []
    for key in freq_dictionary.keys():
        word_list.append(key)
    return word_list

def get_top_words_from_bg_freq_dict(number_of_words):
    reader = csv.reader(open('datasets/D-Fiction0001_byFreq.csv', 'r', encoding= "utf-8"))
    freq_dictionary = {}
    for row in itertools.islice(reader, number_of_words):
        row_text = row
        k_v = row_text[0].split("\t")
        k = k_v[0]
        v = k_v[1]
        freq_dictionary[k] = v
    word_list = []
    for key in freq_dictionary.keys():
        word_list.append(key)
    return word_list

def plot_dispersions_for_text(text, path):
    top_text_words = get_top_words_from_csv(path, 50)
    top_dict_words = get_top_words_from_bg_freq_dict(50)
    text.dispersion_plot(top_text_words)
    text.dispersion_plot(top_dict_words)
    

def plot_frequency_distribution(text, number_of_words):
    freq_dist = FreqDist(text)
    freq_dist.plot(number_of_words)
    plot_freqdist_freq(freq_dist, number_of_words)


def plot_freqdist_freq(fd, max_num=None, cumulative=False, title='Frequency plot', linewidth=2):

    tmp = fd.copy()
    norm = fd.N()
    for key in tmp.keys():
        tmp[key] = float(fd[key]) / norm

    if max_num:
        tmp.plot(max_num, cumulative=cumulative,
                 title=title, linewidth=linewidth)
    else:
        tmp.plot(cumulative=cumulative, 
                 title=title, 
                 linewidth=linewidth)

    return

def tokenize_bg_freq_dict(number_of_words):
    reader = csv.reader(open('datasets/D-Fiction0001_byFreq.csv', 'r', encoding= "utf-8"))
    freq_dictionary = {}
    for row in itertools.islice(reader, number_of_words):
        row_text = row
        k_v = row_text[0].split("\t")
        k = k_v[0]
        v = k_v[1]
        freq_dictionary[k] = v
    return freq_dictionary



############################# Execute functions ############################

# text = tokenize_text("texts/kadiiski.txt")
# text2 = clean_text("texts/kadiiski.txt")
# plot_dispersions_for_text(text, "datasets/poem_set.csv")
# plot_frequency_distribution(text2, 50)

# text.concordance("свят")
# text.concordance("слънцето")
# text.concordance("ден")

# tokenize_bg_freq_dict(50)