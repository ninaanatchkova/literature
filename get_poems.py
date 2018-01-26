import requests
import os
import lxml
from bs4 import BeautifulSoup

base = "https://liternet.bg/publish11/k_kadiiski/ezdach/"
allpoems = requests.get("https://liternet.bg/publish11/k_kadiiski/ezdach/content.htm")
encoding = allpoems.headers['content-type'].split('charset=')[1]
soup = BeautifulSoup(allpoems.text, from_encoding="cp1252")

def get_links(index):
    allpoems = requests.get(index)
    encoding = allpoems.headers['content-type'].split('charset=')[1]
    soup = BeautifulSoup(allpoems.text, from_encoding="cp1252")
    links = []
    for p in soup.find_all('p'):
        for a in p.find_all('a'):
            if a['href'] == "../index.html" or a['href'] == "index.html":
                continue
            else:
                links.append(base + a['href'])
    return(links)

# Create dir
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating folder ' + directory)
        os.makedirs(directory)

# Save links to file
def save_poem_links_to_file(index):
    links = get_links(index)
    create_project_dir("links")
    file_name = "poetry_links.txt"
    path = "links/" + file_name
    f = open(path, 'w')
    for link in links:
        f.write(link + "\n")
    f.close()

save_poem_links_to_file("https://liternet.bg/publish11/k_kadiiski/ezdach/content.htm")