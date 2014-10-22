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

        if "retweeted_status" in post.keys():
            self.esRT = 1
        else: 
            self.esRT = 0

        self.estado      = 0 # Sin calificar

    
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


def sequenciar_tweets(vector_tweets_limpio):
    dev = []

    for item in vector_tweets_limpio:
        dev.append(item.to_sequence())

    return dev

def limpieza_retweets(vector_tweets):
    dev = []

    for var_json in vector_tweets:

        item = Tweet(var_json)

        # Eliminar RT
        if (item.esRT):
            continue

        dev.append(item)

    return dev

def limpieza_de_datos(vector_tweets):
    dev = []

    for var_json in vector_tweets:

        item = Tweet(var_json)


        # Eliminar RT
        if (item.esRT):
            continue

        # Limpieza de Usuarios (Se procederá a eliminar a los usuarios en los textos)
        for user in var_json["entities"]["user_mentions"]:

            usuario = "@" + user["screen_name"]           
            item.body_tweet = item.body_tweet.replace(usuario.encode('utf-8'),'')


        # Limpieza de links (Se prodecerá a eliminar los links en los textos)
        for url in var_json["entities"]["urls"]:
            item.body_tweet = item.body_tweet.replace(url["url"].encode('utf-8'),'')



        # Limpieza de hashtags (Se reemplaza #CorredorAzul por servicio y se eliminan los restantes)

        item.body_tweet = item.body_tweet.replace("#CorredorAzul","servicio")
        for tag in var_json["entities"]["hashtags"]:
            hashtag = "#" + tag["text"].encode('utf-8')
            item.body_tweet = item.body_tweet.replace(hashtag,'')


        # Limpieza de fotos (Se borrará el link de la foto ubicado en el texto)

        if "extended_entities" in var_json.keys():
            for media in var_json["extended_entities"]["media"]:
                item.body_tweet = item.body_tweet.replace(media["url"].encode('utf-8'),'')


        # Agrego a los que sobrevivieron
        dev.append(item)

    return dev

def main():

    print "Procesando..."

    with open("corredor_azul_stream.txt",'r') as f:
        lines = f.readlines()

    output = open('output.csv', 'wb')
    writer = csv.writer(output, delimiter=DELIMITER)

    output_original = open('output_original.csv', 'wb')
    writer_original = csv.writer(output_original, delimiter=DELIMITER)

    vector_tweets           = []    # Arreglo de clase Tweets
    vector_tweets_limpio    = []    # Arreglo de Tweets putificados
    vector_tweets_sequence  = []    # Arreglo de Tweets.to_sequence()

    for line in lines:
        if ('{' in line[0]):
            var_json        = json.loads(line)
            vector_tweets.append(var_json)

    vector_tweets_limpio    = limpieza_de_datos(vector_tweets)
    vector_tweets_sequence  = sequenciar_tweets(vector_tweets_limpio)

    writer.writerows(vector_tweets_sequence)
    writer_original.writerows(sequenciar_tweets(limpieza_retweets(vector_tweets)))    

    output.close()
    output_original.close()
    print "Fin del procesamiento: output.csv"


main()

