# -*- coding: utf-8 -*-
import json
import csv
import nltk

DELIMITER = '|'

class Tweet:

    id_tweet    = None
    id_author   = None
    date        = None

    original_text = None
    processed_text = None #tweet limpiado
    spanish_text = None #solo palabras validadas por dicc en español
    tweet_tagged = None #generado por el POSTagger

    #esRT        = None, ya no lo ponemos porque ya limpiamos todos
    auto_polarity = None #generado por Emoticons y Noticias
    auto_polarity_reviewed = None #revision de lo generado anteriormente
    manual_polarity = None #clasificado por nosotros
    polarity_test = None #auto_polarity_reviewed OR manual_polarity

    word_count = None #cantidad de palabras de processed_text
    spanish_count = None #cantidad de palabras de spanish_text

    polarity_dic1 = None #ElhPolar dictionary
    polarity_dic2 = None #fullStrenght dictionary
    polarity_dic3 = None #mediumStrenght dictionary

    polarity_dic1_pos = None #ElhPolar dictionary usando POS Tagger
    polarity_dic2_pos = None #fullStrenght dictionary usando POS Tagger
    polarity_dic3_pos = None #mediumStrenght dictionary usando POS Tagger

    important_words = None

    def __init__(self,post):
        self.id_tweet    = post[0]
        self.id_author   = post[1]
        self.date        = post[2]

        self.original_text = post[3]
        self.processed_text  = post[4]
        self.spanish_text = post[5]
        self.tweet_tagged = post[6]

        #self.esRT = post[5]
        self.auto_polarity = post[7]
        self.auto_polarity_reviewed = post[8]
        self.manual_polarity = post[9]
        self.polarity_test = post[10]

        self.word_count = post[11]
        self.spanish_count = post[12]

        self.important_words = None

    
    def to_CSV(self):
        output = []
        output.append(str(self.id_tweet))
        output.append(str(self.id_author))
        output.append(self.date)

        output.append(self.original_text)
        output.append(self.processed_text)
        output.append(self.spanish_text)
        output.append(self.tweet_tagged)

        #output.append(str(self.esRT))
        output.append(str(self.auto_polarity))
        output.append(str(self.auto_polarity_reviewed))
        output.append(str(self.manual_polarity))
        output.append(str(self.polarity_test))

        output.append(str(self.word_count))
        output.append(str(self.spanish_count))

        output.append(str(self.polarity_dic1))
        output.append(str(self.polarity_dic2))
        output.append(str(self.polarity_dic3))
        output.append(str(self.polarity_dic1_pos))
        output.append(str(self.polarity_dic2_pos))
        output.append(str(self.polarity_dic3_pos))

        output.append(self.important_words)

        return output

def main():

    print "Inicio..."
    with open("tweets_a_procesar_v2.csv", 'rb') as csvfile:
        lines = csv.reader(csvfile, delimiter=DELIMITER, quotechar="'")
        # En esta variable estan todos los tweets
        tweets = []
        for line in lines:
            tweet = Tweet(line)
            #print tweet.spanish_text.split()
            tweets.append(tweet)
        
    #archivo de salida
    output = open("output_tagged_v2.csv", 'wb')
    filewriter = csv.writer(output, delimiter=DELIMITER, quotechar="'")

    #importando el tagger en español de Stanford NLP
    from nltk.tag.stanford import POSTagger
    st = POSTagger('/Applications/XAMPP/htdocs/Proyectos/Stanford/stanford-postagger-full-2014-08-27/models/spanish-distsim.tagger','/Applications/XAMPP/htdocs/Proyectos/Stanford/stanford-postagger-full-2014-08-27/stanford-postagger-3.4.1.jar',encoding='utf-8')
    #st = POSTagger('/Applications/XAMPP/htdocs/Proyectos/Stanford/stanford-postagger-full-2014-08-27/models/spanish.tagger','/Applications/XAMPP/htdocs/Proyectos/Stanford/stanford-postagger-full-2014-08-27/stanford-postagger-3.4.1.jar',encoding='utf-8')
    #st = POSTagger('C:\Data\stanford-postagger-full-2014-08-27\models\spanish.tagger', 'C:\Data\stanford-postagger-full-2014-08-27\stanford-postagger-3.4.1.jar', encoding='utf-8')

    n=0
    for tweet in tweets:
        n+=1
        print tweet.spanish_text
        #Ejemplo: st.tag('What is the airspeed of an unladen swallow ?'.split())
        tweet_tagged = st.tag((tweet.spanish_text).split())
        #Ejem_output: [('What', 'WP'), ('is', 'VBZ'), ('the', 'DT'), ('airspeed', 'NN'), ('of', 'IN'), ('an', 'DT'), ('unladen', 'JJ'), ('swallow', 'VB'), ('?', '.')]
        #print tweet_tagged

        important_words = []
        n_adj = 0
        for tag in tweet_tagged:
            inicial = tag[1][:1]
            if('a' in inicial):
                important_words.append(tag[0])
            if('r' in inicial):
                important_words.append(tag[0])
            if('n' in inicial):
                important_words.append(tag[0])
            if('v' in inicial):
                important_words.append(tag[0])

        #tweet.cant_adj = n_adj
        tweet.tweet_tagged = tweet_tagged
        tweet.important_words = important_words
        filewriter.writerow(tweet.to_CSV())
        if n % 100 == 0: print n
    print "Done"
    output.close()

main()