# import argparse
import sys
import os
import requests
import _locale

_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])


def is_valid_url(user_input):
    return '.' in user_input


# write your code here
def convert_to_file_name(url):
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
    # print(response.headers)
    # response.encoding = 'utf-8'
    # print("****response.encoding*****",response.encoding)

    return response.text


# bloomberg.com
# nytimes.com
# back
def browse(url, cache_dir, history):
    # print(f"browsing: {url}")
    if is_valid_url(url):
        history.append(url)
        html = send_get_request(url)  # .rstrip("\n")
        idx = html.find(chr(160))
        with open('ttt.txt ','a') as ff:
            print("@@@@@@@@@@",idx,file=ff)
            for c in html[idx-1:idx+2]:
                print(c , ord(c),file=ff)

        # print(chr(160))
        print(html)
        save(html, convert_to_file_name(url), cache_dir)

    else:
        print_cached_page(url, cache_dir, history)
        # raise Exception("incorrrect url")


def main():
    # print(sys.argv)
    history = []

    if len(sys.argv) != 2:
        print("Invalid call to the program, please specify a directory to save pages")
        return
    cache_dir = sys.argv[1]
    # print(os.access(cache_dir, mode=os.F_OK))
    if not os.access(cache_dir, mode=os.F_OK):
        os.mkdir(cache_dir)

    while True:
        url = input()
        if url == "exit":
            break

        if url == "back":
            # print(len(history))
            # print(history)
            if len(history) > 0:
                history.pop()

            if len(history) > 0:
                url = history.pop()

        browse(url, cache_dir, history)


main()
