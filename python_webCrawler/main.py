from python_webCrawler.spellCrawler import multi_thread_crawler
from python_webCrawler.spellCrawler import mono_thread_crawler
from python_webCrawler.spellCrawler import home_crawler
from python_webCrawler.spellCrawler import put_spells_in_json

from python_webCrawler.driverPath import get_browser

from time import time


if __name__ == '__main__':
    start = time()

    browser = get_browser()

    home_crawler(browser)
    multi_thread_crawler(browser)
    put_spells_in_json()

    end = time()
    print("\nExecution time: ", end - start, " s")
