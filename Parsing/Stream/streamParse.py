# -*- coding: utf-8 -*-
import json

import csv

DELIMITER = '|'

class Tweet:

    id_tweet    = None
    id_author   = None
    body_tweet  = None
    date        = None
    esRT        = None
    estado      = None


    def __init__(self,post):
        self.id_tweet    = post["id"]
        self.id_author   = post["user"]["id"]

        texto = post["text"].replace('\n',". ")
        texto = texto.replace('\r'," ")
        self.body_tweet  = str(texto.encode('utf-8'))

        self.date        = post["created_at"]

        if "RT" in post["text"]: 
            self.esRT = 1
        else: 
            self.esRT = 0

        self.estado      = 0 #Sin calificar

    
    def to_CSV(self):
        output = ""
        output += str(self.id_tweet) + DELIMITER
        output += str(self.id_author) + DELIMITER
        output += str(self.body_tweet) + DELIMITER
        output += str(self.date) + DELIMITER
        output += str(self.esRT) + DELIMITER
        output += str(self.estado) + "\n"

        return output
    

    def to_sequence(self):

        sequence = [self.id_tweet, self.id_author, self.body_tweet, self.date, self.esRT, self.estado]

        return sequence


def main():

    print "Procesando..."

    with open("corredor_azul_stream.txt",'r') as f:
        lines = f.readlines()

    output = open('output.csv', 'wb' )
    writer = csv.writer(output, delimiter=DELIMITER)

    contador = 0

    vector_tweets = []

    for line in lines:

        if ('{' in line[0]):

            var_json = json.loads(line)

            tweetauxiliar = Tweet(var_json)

            #print tweetauxiliar.to_CSV()            

            if (tweetauxiliar.esRT == 0):
                vector_tweets.append(tweetauxiliar.to_sequence())
            else:
                pass

            contador = contador + 1

        else:
            pass

    writer.writerows(vector_tweets)

    output.close()

    print "Fin del procesamiento: output.csv"
    
main()

