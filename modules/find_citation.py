import re 
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
from lxml.etree import tostring
from lxml import etree
from nltk.tokenize import sent_tokenize


def is_cited(text, reference_id):
    cited_in_text = False
    if re.search(reference_id, str(text), re.IGNORECASE) != None:
        cited_in_text = True
    return cited_in_text


def sentences(text, reference_id):
    sentences_citing = []
    for sentence in sent_tokenize(str(text)):
        if reference_id in sentence:
            sentences_citing.append(sentence)
            return sentences_citing

