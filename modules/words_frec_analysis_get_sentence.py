import re
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from copy import deepcopy


def filter_sentence(citing_sentence):

    """
	It removes citations, html labels and stop words
    """

    if citing_sentence == None:
        return " " #filtered_sentences_noNone.append(" ")

    if citing_sentence != None:
        citing_sentence = re.sub("[\<\[].*?[\>\]]", "", citing_sentence) #to remove citations
        #citing_sentence = re.sub("[*?]", "", citing_sentence) #to remove citations
        citing_sentence = re.sub('[0-9]+', '', citing_sentence)
        to_delete = ["Introduction", "Background", "Conclusions","the", "and", "therefore", "thus", "et", "al."]#, "\n", "<\sub>", "bibr", "ref", "rid", "type", "xref"] #, "/p\np\n", "\p"]
        for word in to_delete:
            citing_sentence = re.sub(word, "", citing_sentence)
            #print(word)
            #print(citing_sentence)
        #citing_sentence = re.sub("\?", "", citing_sentence) #to remove citations
        citing_sentence = ' '.join([word for word in citing_sentence.split() if word not in (stopwords.words('english'))])
        return citing_sentence 

def analysis(citing_sentences_list):

    """
	Frequency analysis of most common words. It provides the X most frequent words and bigrams.

    """

    citing_sentences_original = deepcopy(citing_sentences_list) # This is a list of lists, so you need deepcopy. We are keeping a copy because we are going to modify = citing_sentences_list
    filtered_sentences_list = citing_sentences_list.apply(filter_sentence)
    #print("Sentences where the paper was cited: ")
    #print(filtered_sentences_list)

    count_vectorizer = CountVectorizer(max_features=5) # We will check the X most  frequent words  (max_features = X)
    # count_vectorizer = CountVectorizer(max_features) 
    count_vectorizer.fit_transform(filtered_sentences_list) #backToBytes

    try:
        frequent_words = count_vectorizer.get_feature_names()
        print("Most frequent words: ", frequent_words)
    except ValueError:
        print("No sentences to analyse") #It may happen that we hava filetered out all the words in the sentence!!!
        return


    count_vectors = count_vectorizer.transform(filtered_sentences_list)
    word_frequency = count_vectors.toarray()

    number_words_in_sentence = np.sum(count_vectors.toarray(),axis=1).tolist()

    print("Frequent words included: ", number_words_in_sentence)
    print("Maximum words in the same sentence  = ", max(number_words_in_sentence))

    sentence_length = []
    for sentence in citing_sentences_list:
        if sentence == None:
            sentence_length.append(0)
        if sentence != None:
            sentence_length.append(len(sentence))

    df_sentences = pd.DataFrame({"number_frequent_words" : number_words_in_sentence,
                                    "citing_sentence" : citing_sentences_original,
                                    "citing_sentence_filtered" : citing_sentences_list, 
                                    "sentence_length": sentence_length})
    
    
    # We pick the sentences that includes the maximum number of frequent words. In case there are several such sentences we choose the shortes one.
    sentences_toCheck = df_sentences[(df_sentences["number_frequent_words"] == max(df_sentences["number_frequent_words"]))] #['sentence_citing_intro']
    min_length = min(sentences_toCheck["sentence_length"][:]) 
    
    sentence = sentences_toCheck[sentences_toCheck['sentence_length'] == min_length]["citing_sentence"]
    
    # To print the full content
    print("\n Representative sentence:")
    import sys
    sentence.to_csv(sys.stdout)
    
    #return [frequent_words, sentence, df_sentences]


########################### FOR FRQUENCY ANALYSIS: WORDS AND BIGRAMS #######################

# filter_sentence_technicisms = filter_sentence + filter out words not in the dictionary



def filter_sentence_technicisms(citing_sentence):

    """
    It also removes technicism by checking if the words are in a list of about 2e(5) English words
    """

    if citing_sentence == None:
        return " " #filtered_sentences_noNone.append(" ")

    if citing_sentence != None:
        citing_sentence = re.sub("[\<\[].*?[\>\]]", "", citing_sentence) #to remove citations
        #citing_sentence = re.sub("[*?]", "", citing_sentence) #to remove citations
        citing_sentence = re.sub('[0-9]+', '', citing_sentence)
        to_delete = ["Introduction", "Background", "Conclusions","the", "and", "therefore", "thus", "et", "al."]#, "\n", "<\sub>", "bibr", "ref", "rid", "type", "xref"] #, "/p\np\n", "\p"]
        for word in to_delete:
            citing_sentence = re.sub(word, "", citing_sentence)
            #print(word)
            #print(citing_sentence)
        #citing_sentence = re.sub("\?", "", citing_sentence) #to remove citations
        with open('./english_words/wordsEn.txt', 'r') as word_file:
            english_words = list(word.strip().lower() for word in word_file)
        
        citing_sentence = ' '.join([word for word in citing_sentence.split() if ((word not in (stopwords.words('english'))) and (word in english_words))])
        return citing_sentence



def analysis_nolimit(citing_sentences_list):
    """
    Similar to .analysis, but there is no limit of words studied.
    """

    # This is a list of lists, so you need deepcopy. We are keeping a copy because we are going to modify = citing_sentences_list
    citing_sentences_original = deepcopy(citing_sentences_list)
    filtered_sentences_list = citing_sentences_list.apply(filter_sentence_technicisms)
    #print(filtered_sentences_list)
    
    count_vectorizer = CountVectorizer(max_features=100) # We will check the X most  frequent words  (max_features = X)
    # count_vectorizer = CountVectorizer(max_features) 
    count_vectorizer.fit_transform(filtered_sentences_list) #backToBytes

    try:
        frequent_words = count_vectorizer.get_feature_names()
        print(frequent_words)
    except ValueError:
        print("No sentences to analyse") #It may happen that we hava filetered out all the words in the sentence!!!
        return


    count_vectors = count_vectorizer.transform(filtered_sentences_list)
    word_frequency = count_vectors.toarray()

    number_words_in_sentence = np.sum(count_vectors.toarray(),axis=1).tolist()
    
    #print("Frequent words included: ", number_words_in_sentence)
    #print("Maximum words in the same sentence  = ", max(number_words_in_sentence))

    sentence_length = []
    for sentence in citing_sentences_list:
        if sentence == None:
            sentence_length.append(0)
        if sentence != None:
            sentence_length.append(len(sentence))

    df_sentences = pd.DataFrame({"number_frequent_words" : number_words_in_sentence,
                                    "citing_sentence" : citing_sentences_original,
                                    "citing_sentence_filtered" : citing_sentences_list, 
                                    "sentence_length": sentence_length})
    
    
    # We pick the sentences that includes the maximum number of frequent words. In case there are several such sentences we choose the shortes one.
    sentences_toCheck = df_sentences[(df_sentences["number_frequent_words"] == max(df_sentences["number_frequent_words"]))] #['sentence_citing_intro']
    min_length = min(sentences_toCheck["sentence_length"][:]) 

    sentence = sentences_toCheck[sentences_toCheck['sentence_length'] == min_length]["citing_sentence"]

    # To print the full content
    import sys
    sentence.to_csv(sys.stdout)

    return frequent_words




def analyse_bigrams(citing_sentences_list):
    """
    Most frequent bi-grams.
    """

    vectorizer = CountVectorizer()

    citing_sentences_original = deepcopy(citing_sentences_list) # This is a list of lists, so you need deepcopy. We are keeping a copy because we are going to modify = citing_sentences_list
    filtered_sentences_list = citing_sentences_list.apply(filter_sentence_technicisms)


    bigram_vectorizer = CountVectorizer(ngram_range=(2, 2))

    X_2 = bigram_vectorizer.fit_transform(filtered_sentences_list).toarray()
    vocab = bigram_vectorizer.vocabulary_
    count_values = X_2.sum(axis=0)
    counts = sorted([(count_values[i],k) for k,i in vocab.items()], reverse=True)
    return counts
