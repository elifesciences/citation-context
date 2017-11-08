# TAKING PAPERS FORM TEST

import os
import subprocess
from bs4 import BeautifulSoup
import glob
    
import sys
sys.path.insert(0, "/project/elife/modules")
import find_section
    
os.chdir('/project/FTP_PUBMED_papers_test')
os.getcwd()



def get_article_list(DOI):
    
    
    ####### Papers in all the .tar.gz files 
    import subprocess
    
    DOI_cited_in  = " "
    for filename in glob.iglob('/project/FTP_PUBMED_papers_test/*'):
        try:
            print('%s' % filename)
            just_filename = filename.replace('/project/FTP_PUBMED_papers_test/', ' ')
            bashCommand = "zgrep -a " + DOI + " " + just_filename
            DOI_cited_in_bytes = subprocess.check_output(bashCommand, shell=True)
            DOI_cited_in = DOI_cited_in + " " + DOI_cited_in_bytes.decode("utf-8") # conver bytes into strings
        
        except subprocess.CalledProcessError as e:
            print('zgrep returned non-zero exit status 1 when searching at %s' % filename)
            print("Subprocess output:", e.output)
  
  
    list_articles_citing = []
    DOI_cited_in_BS = BeautifulSoup(DOI_cited_in, "lxml")
    for article in DOI_cited_in_BS.prettify().split('</article>'):
        article_BS = BeautifulSoup(article, "lxml")# Not all the articles start or finish with this tag.
        for article2 in article_BS.prettify().split('</back>'): #('<article article-type'): #In some cases the seaparation between 2 articles i<\ref> <article article-type> 
            if (DOI in article2) and (len(str(article2)) > 800): #To remove spliting of some end-tags
                list_articles_citing.append(article2)
    
    return list_articles_citing    


import re
import pandas as pd
import find_reference_id
import find_section
import find_citation
    #for filename in glob.iglob('../PMC_sample_1943/PMC_sample_1943/**/*.nxml', recursive=True):
    
    # To avoid the sstem reading just the cache module:
import imp
imp.reload(find_reference_id)
imp.reload(find_section)
imp.reload(find_citation)


def get_df(DOI):

    list_articles_citing = get_article_list(DOI)
    
    
    #list_articles_citing (1)
    articles_citing_doi = [] # (2)
    #articles_citing_pmid = [] # (2-bis)
    reference_id_list = [] #(3)
    
    introduction_list = [] #(4)
    introduction_found_list = [] #(5)
    cited_in_introduction_list = [] #(6)
    
    maintext_list = []
    maintext_found_list = []
    cited_in_maintext_list = []
    
    
    discussion_list = []
    discussion_found_list = []
    cited_in_discussion_list = []
    
    conclusions_list = []
    conclusions_found_list = []
    cited_in_conclusions_list = [] 
    
    #citing_sentences_intro = []
    #citing_sentences_intro_list = []
    # citing_sentences_fulltext_list = []
    
    
    
    
    for article in list_articles_citing:
        
        # DOI
        article_doi = find_section.doi(article)
        articles_citing_doi.append(article_doi)
        
        #article_pmid = find_section.pmid(article)
        #print("PMID: ", article_pmid)
        #articles_citing_pmid.append(article_pmid)
        
        # Reference number
        reference_id = find_reference_id.find_id(article, DOI)
        reference_id_list.append(reference_id)
        
        # INTRODUCTION
        introduction = find_section.introduction(article)
        introduction_list.append(introduction)
        if introduction == ["Introduction not found"]: 
            introduction_found_list.append(False)
        else: 
            introduction_found_list.append(True)
        cited_in_introduction = find_citation.is_cited(str(introduction), reference_id)
        cited_in_introduction_list.append(cited_in_introduction)
        
        #citing_sentences_intro = find_citation.sentences(introduction, reference_id)
        #citing_sentences_intro_list.append(citing_sentences_intro)
    
        # MAIN TEXT 
        maintext = find_section.discussion(article)
        discussion_list.append(maintext)
        if maintext == ["Maintext not found"]: 
            maintext_found_list.append(False)
        else: 
            maintext_found_list.append(True)
        cited_in_maintext = find_citation.is_cited(str(maintext), reference_id)
        cited_in_maintext_list.append(cited_in_maintext)
        
        # DISCUSSION
        discussion = find_section.discussion(article)
        discussion_list.append(discussion)
        if discussion == ["Discussion not found"]: 
            discussion_found_list.append(False)
        else: 
            discussion_found_list.append(True)
        cited_in_discussion = find_citation.is_cited(str(discussion), reference_id)
        cited_in_discussion_list.append(cited_in_discussion)
        
        # CONCLUSIONS
        conclusions = find_section.conclusions(article)
        conclusions_list.append(conclusions)
        if conclusions == ["Conclusions not found"]: 
            conclusions_found_list.append(False)
        else: 
            conclusions_found_list.append(True)
        cited_in_conclusions = find_citation.is_cited(str(conclusions), reference_id)
        cited_in_conclusions_list.append(cited_in_conclusions)
        
        # REFERENCES
        # references = find_section.references(article)
        # references_list.append(references)
    
       # citing_sentences_fulltext = find_citation.sentences(article, reference_id)
       # citing_sentences_fulltext_list.append(citing_sentences_fulltext)
        
        
    # print(list_articles_citing[0])
    #print(articles_citing_doi)
    
    df = pd.DataFrame({'cited_DOI': DOI,
                        'citing_article_DOI': articles_citing_doi,
                       #'citing_article_PMID': articles_citing_pmid,
                       'reference_id': reference_id_list,
                       
                       #'introduction': introduction_list,
                       'introduction_found': introduction_found_list,
                       'cited_in_introduction': cited_in_introduction_list,
                       #'sentence_citing_intro': citing_sentences_intro_list,
                       
                       'maintext_found': maintext_found_list,
                       'cited_in_maintext': cited_in_maintext_list,
                                          
                       'discussion_found': discussion_found_list,
                       'cited_in_discussion': cited_in_discussion_list,
                       
                       'conclusions_found': conclusions_found_list,
                       'cited_in_conclusions': cited_in_conclusions_list
                       #'sentence_citing_article': citing_sentences_fulltext_list
                      })
    
    #csv to write data to 
    #out_csv = '/project/elife/data/df_cited_section.csv'
    #df.to_csv(out_csv,header=False, mode='a', sep='\t', encoding='utf-8', names = ["cited_DOI", "citing_article_DOI", "reference_id", "introduction_found", "cited_in_introduction", "maintext_found", "cited_in_maintext", "discussion_found", "cited_in_discussion", "conclusions_found", "cited_in_conclusions"])
    
    
    return df
    