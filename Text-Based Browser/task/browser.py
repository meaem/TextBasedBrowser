import sys
import os
import requests
from bs4 import BeautifulSoup
from colorama import Fore


def is_valid_url(user_input):
    return '.' in user_input


def convert_to_file_name(url):
    url = url.replace('https://', '')
    return url[0:url.rindex('.')]


def save(text, filename, folder):
    with open(os.path.join(folder, filename), 'w', encoding='utf-8') as f:
        f.write(text)


def print_cached_page(filename, folder, history):
    fn = os.path.join(folder, filename)
    if os.access(fn, os.F_OK):
        with open(fn, 'r', encoding='utf-8') as f:
            print(f.read())
        history.append(filename)
    else:
        print("error: page not caches yet!!")


def send_get_request(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/70.0.3538.77 Safari/537.36"

    if not url.startswith("https://"):
        url = "https://" + url

    response = requests.get(url, headers={'User-Agent': user_agent})
    return response.text


def get_human_readable(html):
    soup = BeautifulSoup(html)
    all_tags = soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "a", "ul", "ol", "li"])
    return "\n".join(
        [Fore.BLUE + a.get_text() + Fore.BLACK if a.name == 'a' else a.get_text() for a in all_tags if a.get_text()])


def browse(url, cache_dir, history):
    if is_valid_url(url):
        history.append(url)
        html = send_get_request(url)
        txt = get_human_readable(html)
        print(txt)
        save(txt, convert_to_file_name(url), cache_dir)
    else:
        print("Incorrect URL")


def main():
    history = []

    if len(sys.argv) != 2:
        print("Invalid call to the program, please specify a directory to save pages")
        return
    cache_dir = sys.argv[1]
    if not os.access(cache_dir, mode=os.F_OK):
        os.mkdir(cache_dir)

    while True:
        url = input()
        if url == "exit":
            break

        if url == "back":
            if len(history) > 0:
                history.pop()

            if len(history) > 0:
                url = history.pop()

        browse(url, cache_dir, history)


main()
