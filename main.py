import requests
from bs4 import BeautifulSoup
from cz import CZcrawl_novel
from cmb import cmb
import os
source = 1
#1 = czbook


output_folder = './output_epubs' 
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


urls = '''
https://czbooks.net/n/cr624/crdic?chapterNumber=0
https://czbooks.net/n/cr82a/crdic?chapterNumber=0
'''
if source == 1:
    for url in urls.split():
        os.makedirs("./tmp", exist_ok=True)
        book_title = CZcrawl_novel(url)
        cmb("./tmp", output_folder,f"{book_title}")
elif source == 2:
    pass
