import re 
from bs4 import BeautifulSoup



def find_id(manuscript, DOI_cited):
    
    """
    It finds the number of the reference of the cited paper in the list of references in the citing paper

    """


    
    manuscript_BS = BeautifulSoup(manuscript, "lxml") 

    reference_searched = " " # in case the reference is not found [] will be returned

    
    for reference in  manuscript_BS.find_all('ref'):
        if re.search(DOI_cited, reference.text, re.IGNORECASE) != None:
            reference_searched = reference
    
    #print(reference_searched)
    
    if reference_searched != " ":
        return(reference_searched.get('id')) # gets just the id of the reference
    else:
        return "Not found"
    
    #return(reference_searched.attrs) # shows attributes

    # To get the exact tag used:
    #pru = str(reference_searched)
    #pru2 = pru.split('\n')
    #return(pru2[0])
    
    