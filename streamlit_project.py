import streamlit as st
import spacy 
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest
from summarizer import Summarizer,TransformerSummarizer
def spacy_summarizer(doc):
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(doc)
    len(list(doc.sents))
    keyword = []
    stopwords = list(STOP_WORDS)
    pos_tag = ['PROPN','ADJ','NOUN','VERB']
    for token in doc:
        if(token.text in stopwords or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            keyword.append(token.text)

    #counting word freq
    freq_word = Counter(keyword)
    freq_word.most_common(5)

    #normalization
    max_freq = Counter(keyword).most_common(1)[0][1]


    for word in freq_word.keys():
        freq_word[word] = (freq_word[word]/max_freq)
    freq_word.most_common(5)
    #weighing sentences
    sent_strength = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent]+=freq_word[word.text]
                else:
                    sent_strength[sent]=freq_word[word.text]
    #print(sent_strength)
    summarized_sentences = nlargest(3,sent_strength,key=sent_strength.get)
    return summarized_sentences
def bert_summarizer(doc):
    bert_model = Summarizer()
    bert_summary = ''.join(bert_model(doc, min_length=60))
    return bert_summary






def main():
    "TEXT SUMMARIZATION STREAMLIT APP"
    st.title("TEXT SUMMARIZER")
    st.subheader('summarize document')
    raw_text = st.text_area('enter text here','Type Here')
    summarizer_algorithm = st.selectbox('summarizer algorithm',['SPACY','BERT'])
    if st.button('summarize'):
        if summarizer_algorithm == 'SPACY':
            summary_result = spacy_summarizer(raw_text)
            st.write(summary_result)

        if summarizer_algorithm == 'BERT':
            summary_result = bert_summarizer(raw_text)
            st.write(summary_result)




    
   

    





if __name__ == '__main__':
    main()