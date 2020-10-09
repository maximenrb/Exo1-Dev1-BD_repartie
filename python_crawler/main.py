from spellCrawler import crawler
from spellCrawler import home_crawler

# Must install 'progress' package
from progress.bar import Bar
import time
import sys


crawler()

# with open('Data/Url') as f:
#     lines = f.read().splitlines()
#
# # Open a file with access mode 'a'
# with open("Data/url_short", "a") as file_object:
#     for line in lines:
#         print(line[46:])
#         # Append 'hello' at the end of file
#         file_object.write(line[46:] + '\n')
