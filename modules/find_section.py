"""
find_section

.doi
	Finds DOI.
.introduction
	It finds introduction directly
.maintext
	It determines the maintext by substracting the other sections.
.discussion
	It finds the discussion directly
.conclusions
	It finds the conclusions directly
.references
	If finds the references directly
"""

import re 
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
from lxml.etree import tostring
from lxml import etree


def doi(text):
    
    manuscript_BS = BeautifulSoup(text, "lxml")
    for sub_heading in manuscript_BS.find_all("front"):
        doi_section = sub_heading.find_all("article-id", {"pub-id-type":"doi"})
        if doi_section != []: #is not None:
            doi_section_BS = BeautifulSoup(str(doi_section[0]), "lxml")
            return doi_section_BS.text
    
        if manuscript_BS.find_all("article-id", {"pub-id-type":"doi"}) != []: #None:
            doi_section = manuscript_BS.find_all("article-id", {"pub-id-type":"doi"})
            if doi_section != []: #is not None: 
                doi_section_BS = BeautifulSoup(str(doi_section[0]), "lxml")
                return doi_section_BS.text

    return "DOI not found"
    #else:
    #    return  doi_section_BS.text
    
    ##### The following code works in jupyter notebook, but not in the module!!!
    # manuscript_BS = BeautifulSoup(text, "lxml")
    # front_part =  manuscript_BS.front
    # doi_section = front_part.find_all("article-id", {"pub-id-type":"doi"})
    # doi_section_BS = BeautifulSoup(str(doi_section[0]), "lxml")
    # return doi_section_BS.text

def pmid(text):
    
    #for reference in  manuscript_BS.find_all('ref'):
    
    manuscript_BS = BeautifulSoup(text, "lxml")
    
    
    pmid_section = manuscript_BS.find_all("pub-id", {"pub-id-type":"pmid"})
    #print("pmid:  ", str(pmid_section))
    if len(pmid_section) > 0:
        pmid_section_BS = BeautifulSoup(str(pmid_section[0]), "lxml")
        return pmid_section_BS.text

    return "PMID not found"
    



def introduction(text):
    manuscript = BeautifulSoup(text, "lxml")
    paragraph_intro = []
    regex = ["introduction", "background"]
    
    # Remove front part
    try:
        manuscript.front.extract()
    except AttributeError:
        pass

    # Remove abstract
    try:
        manuscript.abstract.extract()
    except AttributeError:
        pass
    
    for sub_heading in manuscript.find_all('title'):
        for expression in regex:
            if re.search(expression, sub_heading.text, re.IGNORECASE) != None:
                paragraph_intro = sub_heading.parent
                if paragraph_intro != []:
                    return paragraph_intro         

    if paragraph_intro == []:
        paragraph_intro = manuscript.find_all("sec", {"id":"sec1"})
        if paragraph_intro != []:
            return paragraph_intro
    
    if paragraph_intro == []:
        paragraph_intro = manuscript.find_all("sec", {"sec-type":"Introduction"})
        if paragraph_intro != []:
            return paragraph_intro
        
    if paragraph_intro == []:
        paragraph_intro == manuscript.find_all("sec", {"sec-type":"introduction"})
        if paragraph_intro != []:
            return paragraph_intro
        
    if paragraph_intro == []:
        paragraph_intro = manuscript.find_all("sec", {"sec-type":"INTRODUCTION"})
        if paragraph_intro != []:
            return paragraph_intro
    
    if paragraph_intro == []:
        paragraph_intro = manuscript.find_all("sec", {"sec-type":"Background"})
        if paragraph_intro != []:
            return paragraph_intro
        
        
        
    if paragraph_intro == []:
        paragraph_intro == manuscript.find_all("sec", {"sec-type":"background"})
        if paragraph_intro != []:
            return paragraph_intro
        
    if paragraph_intro == []:
        paragraph_intro = manuscript.find_all("sec", {"sec-type":"BACKGROUND"})
        if paragraph_intro != []:
            return paragraph_intro

    if paragraph_intro == []:
        return ["Introduction not found"]



def maintext(text):
    
    intro_sect = introduction(text)
    conclusions_sect = conclusions(text)
    discussion_sect = discussion(text)
    references_sect = references(text)
    
    
    try:
        text.front.extract()
    except AttributeError:
        pass

    try:
        text.abstract.extract()
    except AttributeError:
        pass
    
    # BeautifulSoup do not conserve the number of spaces between tags
    # Use re.sub and for the left spaces remaining in some lines lstrip()
    


    intro_sect_clean = re.sub(' +',' ', str(introduction(text))).strip().replace('\n', '') 
    conclusions_sect_clean = re.sub(' +',' ', str(conclusions(text))).strip().replace('\n', '')
    discussion_sect_clean = re.sub(' +',' ', str(discussion(text))).strip().replace('\n', '')
    references_sect_clean = re.sub(' +',' ', str(references(text))).strip().replace('\n', '')
    
    text_clean = re.sub(' +',' ', str(text)).strip().replace('\n', '')
    text_clean = text_clean.replace('> <', '><')
    
    section = ""
    if (intro_sect != ["Introduction not found"]) and (intro_sect != []):
        section = text.partition(intro_sect_clean[-50:-2])[2] #take the text following the Introduction
    
    if (conclusions_sect != ["Conclusions not found"]) and (conclusions_sect != []):
        if section == "":
            section = text_clean.partition(conclusions_sect_clean[2:50])[0] #take the text before the  discussion
        else:
            section = section.partition(conclusions_sect_clean[2:50])[0] #
    if (discussion_sect != ["Discussion not found"]) and (discussion_sect != []):
        if section == "":
            section = text_clean.partition(discussion_sect_clean[2:50])[0]
        else:
            section = section.partition(conclusions_sect_clean[2:50])[0] 
    if (references_sect != ["References not found"]) and (references_sect != []):
        if section == "":
            section = text_clean.partition(references_sect_clean[2:50])[0]
        else:
            section = section.partition(references_sect_clean[2:50])[0]
            
   
    if (section != "") and (section != []) and (section is not None):
        section_BS = BeautifulSoup(section, "lxml")
        return section_BS
    else:
        return "Main section not found"
    
    
    

      
def conclusions(text):
    manuscript = BeautifulSoup(text, "lxml")
    paragraph_conclusion = []
    regex = ["conclusion", "outlook"]
    
    

    try:
        manuscript.front.extract()
    except AttributeError:
        pass

    try:
        manuscript.abstract.extract()
    except AttributeError:
        pass
    
    for sub_heading in manuscript.find_all('title'):
        for expression in regex:
            if re.search(expression, sub_heading.text, re.IGNORECASE) != None:
                paragraph_conclusion = sub_heading.parent
                if paragraph_conclusion != []:
                    return paragraph_conclusion         

    if paragraph_conclusion == []:
        paragraph_conclusion = manuscript.find_all("sec", {"sec-type":"Conclusion"})
        if paragraph_conclusion != []:
            return paragraph_conclusion
    
    if paragraph_conclusion == []:
        paragraph_conclusion = manuscript.find_all("sec", {"sec-type":"Conclusions"})
        if paragraph_conclusion != []:
            return paragraph_conclusion

    if paragraph_conclusion == []:
            paragraph_conclusion = manuscript.find_all("sec", {"sec-type":"conclusion"})
            if paragraph_conclusion != []:
                return paragraph_conclusion
    
    if paragraph_conclusion == []:
        paragraph_conclusion = manuscript.find_all("sec", {"sec-type":"conclusions"})
        if paragraph_conclusion != []:
            return paragraph_conclusion

    if paragraph_conclusion == []:
        paragraph_conclusion = manuscript.find_all("sec", {"sec-type":"CONCLUSION"})
        if paragraph_conclusion != []:
            return paragraph_conclusion
    
    if paragraph_conclusion == []:
        paragraph_conclusion = manuscript.find_all("sec", {"sec-type":"CONCLUSIONS"})
        if paragraph_conclusion != []:
            return paragraph_conclusion

    if paragraph_conclusion == []:
        paragraph_conclusion = manuscript.find_all("sec", {"sec-type":"Outlook"})
        if paragraph_conclusion != []:
            return paragraph_conclusion
    
    if paragraph_conclusion == []:
        paragraph_conclusion = manuscript.find_all("sec", {"sec-type":"OUTLOOK"})
        if paragraph_conclusion != []:
            return paragraph_conclusion

    if paragraph_conclusion == []:
        return ["Conclusions not found"]


def discussion(text):
    manuscript = BeautifulSoup(text, "lxml")
    paragraph_discussion = []
    regex = ["discussion"]

    try:
        manuscript.front.extract()
    except AttributeError:
        pass

    try:
        manuscript.abstract.extract()
    except AttributeError:
        pass
    
    for sub_heading in manuscript.find_all('title'):
        for expression in regex:
            if re.search(expression, sub_heading.text, re.IGNORECASE) != None:
                paragraph_discussion = sub_heading.parent
                if paragraph_discussion != []:
                    return paragraph_discussion         

    if paragraph_discussion == []:
        paragraph_discussion = manuscript.find_all("sec", {"sec-type":"Discussion"})
        if paragraph_discussion != []:
            return paragraph_discussion
    
    if paragraph_discussion == []:
        paragraph_discussion = manuscript.find_all("sec", {"sec-type":"discussion"})
        if paragraph_discussion != []:
            return paragraph_discussion

    if paragraph_discussion == []:
        paragraph_discussion = manuscript.find_all("sec", {"sec-type":"DISCUSSION"})
        if paragraph_discussion != []:
            return paragraph_discussion
    
    if paragraph_discussion == []:
        return ["Discussion not found"]


def references(text):
    manuscript_BS = BeautifulSoup(text, "lxml")
    
    
    # You could use the same code for finding the reference number given a doi_section_BS
    # (find_reference_id) and then get the parent. However, in order to find the maintext
    # it will be better avoiding using a particular DOI
    
    manuscript = BeautifulSoup(text, "lxml")
    paragraph_references = []
    regex = ["References"]
    
    if paragraph_references == []:
        paragraph_references = manuscript.find_all("References")
        if paragraph_references != []:
            return paragraph_references

    if paragraph_references == []:
        paragraph_references = manuscript.find_all("ref-list")
        if paragraph_references != []:
            return paragraph_references
    
    
    if paragraph_references == []:
        paragraph_references = manuscript.find_all("sec", {"sec-type":"References"})
        if paragraph_references != []:
            return paragraph_references
    
    if paragraph_references == []:
        paragraph_references = manuscript.find_all("sec", {"sec-type":"Ref"})
        if paragraph_references != []:
            return paragraph_references
    
    if paragraph_references == []:
        paragraph_references = manuscript.find_all("sec", {"sec-type":"Ref-list"})
        if paragraph_references != []:
            return paragraph_references
    
    
    for sub_heading in manuscript.find_all('title'):
        for expression in regex:
            if re.search(expression, sub_heading.text, re.IGNORECASE) != None:
                paragraph_discussion = sub_heading.parent
                if paragraph_discussion != []:
                    print("through title")
                    return paragraph_discussion
    

    if paragraph_references == []:
        return ["References section not found"]

    