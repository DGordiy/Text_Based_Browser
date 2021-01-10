import os
import argparse
import requests
from colorama import init, Fore

from bs4 import BeautifulSoup


def reform(r):
    soup = BeautifulSoup(r.content, 'html.parser')

    tags = soup.find_all(['p', 'a', 'ul', 'ol', 'li'])
    for t in tags:
        if t.name == 'a':
            print(Fore.BLUE + t.text)
        else:
            print(t.text)

    return soup.text.replace('\n\n', '')


def choice_site():
    address = input()
    if address.startswith("http"):
        r = requests.get(address)
        file_name = address[address.rfind("//")]
        return reform(r), file_name
    elif '.' in address:
        file_name = address
        address = 'https://' + address
        r = requests.get(address)
        return reform(r), file_name
    elif 'exit' == address:
        return '', '0'
    else:
        return 'Error: Incorrect URL', '-1'


def main():
    init(True)

    parser = argparse.ArgumentParser(description="taking directory")
    parser.add_argument("directory", help="Give directory for caching pages")
    args = parser.parse_args()

    if not os.path.exists(args.directory):
        os.mkdir(args.directory)

    while True:
        content, name = choice_site()

        if name == '0':
            break
        if name == '-1':
            continue

        with open(f'{args.directory}/{name}', 'w', encoding='utf-8') as f:
            f.write(content)


main()
