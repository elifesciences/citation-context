import re

def bs_preprocess(html):
    """
    Remove distracting whitespaces and newline characters.
    https://stackoverflow.com/questions/23241641/how-to-ignore-empty-lines-while-using-next-sibling-in-beautifulsoup4-in-python
    
    Used to avoid problems with random newlines when getting the sections of the papers.
    In particular with the maintext function in find_section.py 
    """

    
    pat = re.compile('(^[\s]+)|([\s]+$)', re.MULTILINE)
    html = re.sub(pat, '', html)       # remove leading and trailing whitespaces
    html = re.sub('\n', ' ', html)     # convert newlines to spaces
                                    # this preserves newline delimiters
    html = re.sub('[\s]+<', '<', html) # remove whitespaces before opening tags
    html = re.sub('>[\s]+', '>', html) # remove whitespaces after closing tags
    return html 
