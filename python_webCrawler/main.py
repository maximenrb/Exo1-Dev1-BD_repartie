from python_webCrawler.spellCrawler import multi_thread_crawler
from python_webCrawler.spellCrawler import multi_process_crawler
from python_webCrawler.spellCrawler import mono_thread_crawler
from python_webCrawler.spellCrawler import home_crawler
from time import time

start = time()
if __name__ == '__main__':
    mono_thread_crawler()

end = time()
print(str(end - start) + " s")