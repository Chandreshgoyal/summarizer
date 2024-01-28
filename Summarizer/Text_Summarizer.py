import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

rawdocs ='''Amazon launched S3 in 2006. Amazon S3 is an object store and is the backbone for many other services used at Amazon. It has a nice web interface to store and retrieve any amount of data from anywhere around the world. The capacity of S3 is unlimited, which means there is no limit to the amount of data you can store in S3. It is highly durable and has 99.99999999999 percent durability. According to Amazon, this durability level corresponds to an average annual expected loss of 0.000000001 percent of objects. For example, if you store 10,000 objects with Amazon S3, you can on average expect to incur a loss of a single object once every 10,000,000 years. In addition, Amazon S3 is designed to sustain the concurrent loss of data in two facilities.'It is fundamentally different from other file repositories because it does not have a file system. All objects are stored in a flat namespace organized by buckets. It is a regional service; that is, content is automatically replicated within a region for durability. It is one of the most popular object stores available on the Internet today. In this chapter, you’ll first evaluate some of the advantages of Amazon S3, which makes it uniquely popular among customers.'''

#1
def summarizer(rawdocs):
    stopwords = list(STOP_WORDS)
    #print(stopwords)
    #2
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)
    #print(doc)
    #3
    token=[token.text for token in doc]
    #print(token)
    #4
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1
    #print(word_freq)
    #5
    max_freq=max(word_freq.values())
    #print(max_freq)

    #6
    for word in word_freq.keys():
        word_freq[word] -word_freq[word]/max_freq
    #print(word_freq)

    #7
    sent_tokens=[sent for sent in doc.sents]
    #print(sent_tokens)

    #8
    sent_scores={}
    for sent in sent_tokens:
         for word in sent:
             if word.text in word_freq.keys():
                 if sent not in sent_scores.keys():
                     sent_scores[sent] =word_freq[word.text]
                 else:
                     sent_scores[sent] +=word_freq[word.text]
    #print(sent_scores)   
                
    #9
    select_len=int(len(sent_tokens)*0.3)
    #print(select_len)

    #10
    summary = nlargest(select_len, sent_scores, key=sent_scores.get)
    #print(summary)

    #11
    final_summary = [word.text for word in summary]
    summary= ' '.join(final_summary)
    #print(summary)
    
    #12
    #print("Length of original Text ", len(rawdocs.split(' ')))
    #print("Length of summary Text ", len(summary.split(' ')))
    
    return summary, doc, len(rawdocs.split(' ')), len(summary.split(' '))





