import requests
from time import time, sleep
from multiprocessing import Pool, Queue, Manager, cpu_count
from itertools import repeat
import sys


class NODE:


    set_url = set()
    all_found = set()

    
    def __init__(self, text = None):
        self.text = text
        self.set_url.add(text)
        self.all_found.add(text)

    def CheckUrl(self, curr_url):
        url = self.text
        if ' ' in curr_url: return 
        if '/' not in curr_url: return 
        if url in curr_url: curr_url = curr_url[len(url) - 1:]
        if '://' in curr_url: return 
        if len(curr_url) < 2: return
        if curr_url[-1] == '/': curr_url = curr_url[:-1]
        if curr_url[0] == '/': curr_url = curr_url[1:]
        return url + curr_url         


    def multi_runner(self):
        m = Manager()
        q = m.Queue()
        mistakes = m.Queue()
        old_len, curr_len, flag = 0, 1, 2
        self.set_url |= find_links(self)
        current_set = self.set_url - set(self.text)
        while flag and old_len < 20000:
            with Pool(cpu_count() * 8) as p:
                p.starmap(find_links, zip(repeat(self), list(current_set), repeat(q), repeat(mistakes)))
            p.close()
            p.join()
            while not q.empty(): self.all_found |= q.get()
            old_len, curr_len = curr_len, len(self.all_found)
            if old_len == curr_len: flag -= 1
            current_set = self.all_found - current_set
        while not mistakes.empty():
            self.all_found.discard(mistakes.get())


    def print_me(self):
        with open('out.txt', 'w', encoding = "utf-8") as f:
            for i in self.all_found: f.write(i + '\n')
            

def find_links(self, url = None, q = None, mistakes = None):
    found_links = set()
    if url is None: url = self.text
    try:
        rez = requests.get(url, timeout = 5)
    except Exception:
        if mistakes is not None: mistakes.put(url)
        return found_links
    found_links.add(url)
    found_links.add(None)
    i = 0
    while rez.text.find('<a href', i) > 0:
        i = rez.text.find('<a href', i + 1)
        found_links.add(self.CheckUrl(rez.text[i + 9:rez.text.find('"', i + 9)]))
    found_links.discard(None)
    if q is not None: q.put(found_links)
    return found_links


def main():
    print('Welcome!')
    if len(sys.argv) > 1:
        main_link = sys.argv[1]
    else:
        print('Please enter link to the main site in format: http://*/ or https://*/')
        main_link = input('Enter link:\n')
    if main_link[:4] != 'http' or main_link[-1] != '/': print('Uncorrect format. Try again.')
    else:
        print('Your link is correct. Starting..')
        start_time = time()
        tree = NODE(main_link)
        tree.multi_runner()
        finish_time = time()
        tree.print_me()
        print(f"All done. Found {len(tree.all_found)} links.")
        print('They are saved in the same path named "out.txt".')
        print(f"It took {int(finish_time - start_time)} seconds.")
        print('Have a good day!')


if __name__ == '__main__':
    main()
