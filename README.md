# citation-context

The aim to analyzed the context of the citation of any paper in other papers included in the the PMC Open Access Subset (PMC OAS) 
(https://www.ncbi.nlm.nih.gov/pmc/tools/openftlist/).  
This is a collection of open access papers that can be accessed through a FTP service. The format of the papers is XML.


____________________________________________________________________________________________________________________
PROGRAMS

____________________________________________________________________________________________________________________
get_papers.ipynb

•	It takes a list of DOIs (directly from the code or reads them from a file).
•	It finds papers in FTP_PUBMED citing these DOIs. For each DOI it saves the list of papers in a file (out_csv)
•	Preprocessing data. Remove random spaces and store in a new file. 

____________________________________________________________________________________________________________________
analyse_papers.ipynb

	Analysis of several papers 
•	Analyse file containing papers citing a particular DOI. This DOI can be read from a file (the one used in get_papers) or directly introduced in a list.
•	By calling get_df_analise_section it generates a dataframe containing:
    
    # df['cited_DOI', 'citing_DOI', 'reference_id', 'introduction_found', 
    #   'cited_in_introduction', 'maintext_found', 'cited_in_maintext', 
    #   'discussion_found', 'cited_in_discussion', 'conclusions_found', 
    #   'cited_in_conclusions', 'sentence_citing_intro', 
    #   'sentence_citing_maintext', 'sentence_citing_discussion', 
    #   'sentence_citing_conclusions']
    
-	reference_id is the number of reference of the cited paper in a particular paper. 
-	'introduction_found', 'maintext_found', 'discussion_found' and 'conclusions_found' get True/False value depending on whether a particular section has been found.
-	'cited_in_introduction', 'cited_in_maintext', 'cited_in_discussion', 'cited_in_conclusions' get True/False values depending on whether the paper is cited in these sections.
-	'sentence_citing_intro',  'sentence_citing_maintext', 'sentence_citing_discussion',    'sentence_citing_conclusions' are the sentences in each section where the paper is cited.

•	It also generates another dataframe with information about how many times the paper has been cited in each section: 

     # dict_citation_hyst ['DOI_cited', 'total_papers_citing', 'papers_all_sections_found',  
     #   'cited_in_introduction', 'cited_in_maintext', 'cited_in_discussion', 'cited_in_conlusions']

•	It saves the dataframes in two files. 
Note: For “df” only the information of the last paper (cited_DOI) analysed is saved (I am not using later this for further analysis, but using it for checking)

•	Plot the analysis (file_df_analysis_hist). 
-	For multiple papers (used to plot the analysis of papers having the same number of citations)

Analysis of just one DOI 
•	Plot and analysis of just one paper. 

____________________________________________________________________________________________________________________
find_word_freq_readfiles.ipynb

•	It reads the dataframe with the analysis (file_df_analysis) and the dataframe with the histogram (file_df_analysis_hist) information created by “analyse_papers.ipynb”.
•	Frequency analysis of the sentence were a paper was cited. It finds a representative sentence showing how the a paper has been cited in the different sections. It is selected by getting the list of sentences containing the maximum number of most frequent words used when citing the paper (in each section). If there are several sentences it picks the shortest one.
•	Sentiment analysis using NLTK.

criticism_detection.ipynb
•	It analysis papers citing another one that has been retracted.
•	It takes papers that triggered the retraction and classify them as highly_critical.
•	Papers published a year before the first highly_critical paper are classified as non_critical.
•	Papers published after the highly_critical papers are classified as critical (they are not used in the analysis later on because they may contain mixed criticism).
•	Date of publication of the papers are taken from the “PMC-ids.csv.gz” file, available through the PMC FTP service:
https://www.ncbi.nlm.nih.gov/pmc/pmctopmid/
•	It takes all the sentences citing a particular DOI in all the papers disregarding its section. 
•	It shows that clustering algorithms such as PCA and TSNE fail if trying to cluster the sentences from non_critical and high_critical papers just using vader lexicon.
•	It gets all the sentences in the high_critical papers and a similar number of sentences from the non_critical papers. It finds the words and bigrams used in the high_critical set and are not used in the non_critical set.


____________________________________________________________________________________________________________________
MODULES:

____________________________________________________________________________________________________________________
bs_preprocess.py

.bs_preprocess
	Removes distracting whitespaces and newline characters.
Used to avoid problems with random newlines when getting the sections of the papers. In particular with the maintext function in find_section.py

____________________________________________________________________________________________________________________
find_section.py

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

____________________________________________________________________________________________________________________
find_reference_id.py

. find_id
	It finds the number of reference of the cited paper in the list of references

____________________________________________________________________________________________________________________
get_df_analise_section.py

. get_df	

Returns dataframe:
df['cited_DOI', 'citing_DOI', 'reference_id', 'introduction_found', 'cited_in_introduction', 'maintext_found', 'cited_in_maintext', 'discussion_found', 'cited_in_discussion', 'conclusions_found', 'cited_in_conclusions', 'sentence_citing_intro', 'sentence_citing_maintext', 'sentence_citing_discussion', 'sentence_citing_conclusions']

____________________________________________________________________________________________________________________
words_frec_analysis_get_sentence.py

.filter_sentence
	It removes citations, some words that may be labels and stop words
.analysis
	Frequency analysis of most common words. It provides the most X frequent words and bigrams.
. filter_sentence_technicisms
	It also removes technical words by checking if the words are in a list of about 2e(5) English words that are found in the .txt file english_words/wordsEn.txt
.analysis_nolimit
	Similar to .analysis, but there is no limit of words studied.
. analyse_bigrams
	Most frequent bi-grams.
