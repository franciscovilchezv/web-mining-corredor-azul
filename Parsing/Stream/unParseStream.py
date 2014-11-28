# -*- coding: utf-8 -*-
import json
import csv
import nltk

DELIMITER = '|'

class Tweet:

    id_tweet    = None
    id_author   = None
    tweet_original = None
    body_tweet  = None
    date        = None
    esRT        = None
    estado      = None
    cant_terminos = None
    cant_adj = None
    tweet_tagged = None

    def __init__(self,post):
        self.id_tweet    = post[0]
        self.id_author   = post[1]
        self.tweet_original = post[2]
        self.body_tweet  = post[3]
        self.date        = post[4]
        self.esRT = post[5]
        self.estado = post[6]
        self.cant_terminos = post[7]
    
    #def to_CSV_adj(self):
    #    output = ""
    #    output += str(self.id_tweet) + DELIMITER
    #    output += str(self.id_author) + DELIMITER
    #    output += str(self.tweet_original) + DELIMITER
    #    output += str(self.body_tweet) + DELIMITER
    #    output += str(self.date) + DELIMITER
    #    output += str(self.esRT) + DELIMITER
    #    output += str(self.estado) + DELIMITER
    #    output += str(self.cant_terminos) + DELIMITER
    #    output += str(self.cant_adj) + "\n"

    #   return output
    
    def to_CSV(self):
        output = []
        output.append(str(self.id_tweet))
        output.append(str(self.id_author))
        output.append(self.tweet_original)
        output.append(self.body_tweet)
        output.append(self.date)
        output.append(str(self.esRT))
        output.append(str(self.estado))
        output.append(str(self.cant_terminos))
        output.append(str(self.cant_adj))
        output.append(self.tweet_tagged)
        return output

def main():

    print "Inicio..."
    with open("Corredor Azul/Modificados/Dias/output_final_AO.csv", 'rb') as csvfile:
        lines = csvfile.readlines()
    # En esta variable estan todos los tweets
    tweets = []
    for line in lines:
        line = line.replace("\n","")
        line = line.replace("\r","")
        fields = line.split('|')    
        tweet = Tweet(fields)
        tweets.append(tweet)
    
    #archivo de salida
    output = open("Corredor Azul/Modificados/Dias/output_tagged.csv", 'wb')
    filewriter = csv.writer(output, delimiter=DELIMITER, quotechar="'")

    #importando el tagger en español de Stanford NLP
    from nltk.tag.stanford import POSTagger
    st = POSTagger('/Applications/XAMPP/htdocs/Proyectos/Stanford/stanford-postagger-full-2014-08-27/models/spanish-distsim.tagger','/Applications/XAMPP/htdocs/Proyectos/Stanford/stanford-postagger-full-2014-08-27/stanford-postagger-3.4.1.jar',encoding='utf-8')
    #st = POSTagger('/Applications/XAMPP/htdocs/Proyectos/Stanford/stanford-postagger-full-2014-08-27/models/spanish.tagger','/Applications/XAMPP/htdocs/Proyectos/Stanford/stanford-postagger-full-2014-08-27/stanford-postagger-3.4.1.jar',encoding='utf-8')
    #st = POSTagger('C:\Data\stanford-postagger-full-2014-08-27\models\spanish.tagger', 'C:\Data\stanford-postagger-full-2014-08-27\stanford-postagger-3.4.1.jar', encoding='utf-8')

    n=0
    for tweet in tweets:
        n+=1
        print tweet.body_tweet
        #Ejemplo: st.tag('What is the airspeed of an unladen swallow ?'.split())
        tweet_tagged = st.tag((tweet.body_tweet).split())
        #Ejem_output: [('What', 'WP'), ('is', 'VBZ'), ('the', 'DT'), ('airspeed', 'NN'), ('of', 'IN'), ('an', 'DT'), ('unladen', 'JJ'), ('swallow', 'VB'), ('?', '.')]
        #print tweet_tagged
        n_adj = 0
        for tag in tweet_tagged:
            if tag[1] == 'rg': 
                #print tag[1]
                n_adj+=1
        tweet.cant_adj = n_adj
        tweet.tweet_tagged = tweet_tagged
        filewriter.writerow(tweet.to_CSV())
        if n % 100 == 0: print n
    print "Done"
    output.close()

main()