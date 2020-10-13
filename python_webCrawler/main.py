from python_webCrawler.spellCrawler import multi_thread_crawler
from python_webCrawler.spellCrawler import mono_thread_crawler
from python_webCrawler.spellCrawler import home_crawler

from time import time


if __name__ == '__main__':
    start = time()

    multi_thread_crawler()

    end = time()
    print("")
    print("Execution time: " + str(end - start) + " s")
