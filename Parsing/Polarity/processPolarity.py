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

        return output


def main():

    print "Inicio..."
    with open("tweets_a_procesar.csv", 'rb') as csvfile:
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
    output = open("tweets_procesados_diccionario.csv", 'wb')
    filewriter = csv.writer(output, delimiter=DELIMITER)

    n=0
    for tweet in tweets:
        n+=1
        print tweet.body_tweet

        #Aqui: procesar los 3 archivos con diccionarios para: "spanish_text"
        #Tambien procesar usando el POSTagger, incrementado por adjetivos

        filewriter.writerow(tweet.to_CSV())
        if n % 100 == 0: print n
    print "Done"

    output.close()

main()