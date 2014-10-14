# -*- coding: utf-8 -*-
import json

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
        self.body_tweet  = texto

        self.date        = post["created_at"]

        if "RT" in post["text"]: 
            self.esRT = 1
        else: 
            self.esRT = 0

        self.estado      = 0 #Sin calificar


    def to_CSV(self):
        output = ""
        output += str(self.id_tweet) + "||"
        output += str(self.id_author) + "||"
        output += str(self.body_tweet.encode('utf-8')) + "||"
        output += str(self.date) + "||"
        output += str(self.esRT) + "||"
        output += str(self.estado) + "\n"

        return output

def main():

    with open("corredor_azul_stream.txt",'r') as f:
        lines = f.readlines()

    escritor = open("stream.out",'w')

    contador = 0

    for line in lines:

        if ('{' in line[0]):

            var_json = json.loads(line)

            tweetauxiliar = Tweet(var_json)

            print
            print tweetauxiliar.to_CSV()
            print

            if (tweetauxiliar.esRT == 0):
                escritor.write(tweetauxiliar.to_CSV())
            else:
                pass

            contador = contador + 1

        else:
            pass


main()

