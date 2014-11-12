# -*- coding: utf-8 -*-
import json


import unicodedata

import csv

import re
from nltk.corpus import stopwords

DELIMITER = '|'

ARCHIVO_SALIDA_ORIGINAL = "Corredor Azul/Modificados/Dias/corredor_azul_stream.csv"
ARCHIVO_SALIDA = 'Corredor Azul/Modificados/Dias/output.csv'

ARCHIVOS_ENTRADA = [
#    "Corredor Azul/Modificados/Dias/1/1.txt",
#    "Corredor Azul/Modificados/Dias/2/2.txt",
#    "Corredor Azul/Modificados/Dias/3/3.txt",
#    "Corredor Azul/Modificados/Dias/4/4.txt",
    "Corredor Azul/Modificados/Dias/5/5.txt"
]

class Tweet:

    id_tweet    = None
    id_author   = None
    body_tweet  = None
    date        = None
    esRT        = None
    estado      = None
    cant_terminos = None


    def __init__(self,post):
        self.id_tweet    = post["id"]
        self.id_author   = post["user"]["id"]

        texto = post["text"].replace('\n',". ")
        texto = texto.replace('\r'," ")
        self.body_tweet  = str(texto.encode('utf-8'))

        self.date        = post["created_at"]

        if ("retweeted_status" in post.keys()) or ("RT" in self.body_tweet.split()):
            self.esRT = 1
        else: 
            self.esRT = 0

        self.estado      = 0 # Sin calificar
        self.cant_terminos = 0 # se asignara el valor correcto luego de la limpieza

    
    def to_CSV(self):
        output = ""
        output += str(self.id_tweet) + DELIMITER
        output += str(self.id_author) + DELIMITER
        output += str(self.body_tweet) + DELIMITER
        output += str(self.date) + DELIMITER
        output += str(self.esRT) + DELIMITER
        output += str(self.estado) + DELIMITER
        output += str(self.cant_terminos) + "\n"

        return output
    

    def to_sequence(self,tipo):

        if(tipo == 1):
            sequence = [self.id_tweet, self.id_author, self.body_tweet, self.date, self.esRT, self.estado, self.cant_terminos]
        else:
            sequence = [self.id_tweet, self.id_author, self.body_tweet, self.date, self.esRT, str(0)]

        return sequence


def sequenciar_tweets(vector_tweets_limpio,tipo):
    dev = []

    if(tipo == 1):
        for item in vector_tweets_limpio:
            dev.append(item.to_sequence(1))
    else:
        for item in vector_tweets_limpio:
            dev.append(item.to_sequence(2))

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



def limpiezaNLTK(body_tweet):

    
    scentence = body_tweet

    #We only want to work with lowercase for the comparisons
    scentence = scentence.lower() 

    #remove punctuation and split into seperate words
    words = re.findall(r'\w+', scentence,flags = re.UNICODE | re.LOCALE) 

    #This is the simple way to remove stop words
    important_words=[]
    cadena = ""
    for word in words:
        if word not in stopwords.words('spanish'):
            important_words.append(word)
            cadena = cadena + " " + word

    
    if ((cadena != "") and (' ' in cadena[0])):
        cadena = cadena[1:]

    return cadena


    #This is the more pythonic way
    #important_words = filter(lambda x: x not in stopwords.words('spanish'), words)

    #print important_words 



def limpieza_de_datos(vector_tweets):
    dev = []
    porcentaje = 0

    for var_json in vector_tweets:

        item = Tweet(var_json)

        # Eliminar RT
        if (item.esRT):
            continue


        # Valorizacion automatica por los emoticones en el body_tweet :) :D =) =( :(
        happy_faces = [':)', ':D', '=)', '(:', 'D:', '(=', ';)']
        sad_faces = ['=(',':(','):', ')=']

        felicidad = False
        tristeza = False

        for face in happy_faces:
            if (face in item.body_tweet):
                felicidad = True
                break

        for face in sad_faces:
            if (face in item.body_tweet):
                tristeza = True
                break

        if(tristeza and felicidad):
            item.estado = 0
        elif(felicidad):
            item.estado = 1
        elif(tristeza):
            item.estado = -1
        else:
            item.estado = 0


        # Limpieza de Usuarios (Se procederá a eliminar a los usuarios en los textos)
        for user in var_json["entities"]["user_mentions"]:
            usuario = "@" + user["screen_name"]           
            item.body_tweet = item.body_tweet.replace(usuario.encode('utf-8'),'')


        # Limpieza de links (Se prodecerá a eliminar los links en los textos)
        for url in var_json["entities"]["urls"]:
            item.body_tweet = item.body_tweet.replace(url["url"].encode('utf-8'),'')


        # Limpieza de hashtags (Se reemplaza #CorredorAzul por servicio y tambien 'corredor azul' y 'corredorazul' y se eliminan los restantes)
        item.body_tweet = item.body_tweet.decode('unicode_escape').encode('ascii','ignore')

        item.body_tweet = item.body_tweet.replace("#CorredorAzul","servicio")

        insensitive_string = re.compile(re.escape('corredor azul'), re.IGNORECASE)
        item.body_tweet = insensitive_string.sub('servicio', item.body_tweet)

        insensitive_string = re.compile(re.escape('corredorazul'), re.IGNORECASE)
        item.body_tweet = insensitive_string.sub('servicio', item.body_tweet)

        for tag in var_json["entities"]["hashtags"]:
            hashtag = "#" + tag["text"].encode('utf-8')
            item.body_tweet = item.body_tweet.replace(hashtag,'')


        # Limpieza de fotos (Se borrará el link de la foto ubicado en el texto)

        if "extended_entities" in var_json.keys():
            for media in var_json["extended_entities"]["media"]:
                item.body_tweet = item.body_tweet.replace(media["url"].encode('utf-8'),'')


        # LimpiezaNLTK
        item.body_tweet = limpiezaNLTK(item.body_tweet)
        if (item.body_tweet == ""):
            continue


        # Limpieza de palabras con longitud menor a 3
        for palabra in item.body_tweet.split():
            if (len(palabra) < 3):
                item.body_tweet = item.body_tweet.replace(str(palabra),'')


        # Guardar la cantidad de terminos que quedaron
        item.cant_terminos = len(item.body_tweet.split())

        
        # Loading
        if ((porcentaje % 500) == 0):
            print('...')
        porcentaje = porcentaje + 1

        # Agrego a los que sobrevivieron
        dev.append(item)

    return dev

def main():

    print "Procesando..."


    output = open(ARCHIVO_SALIDA, 'wb')
    writer = csv.writer(output, delimiter=DELIMITER)

    output_original = open(ARCHIVO_SALIDA_ORIGINAL, 'wb')
    writer_original = csv.writer(output_original, delimiter=DELIMITER)


    for in_file in ARCHIVOS_ENTRADA:

        print "Procesando archivo: " + in_file

        with open(in_file,'r') as f:
            lines = f.readlines()

        vector_tweets           = []    # Arreglo de clase Tweets
        vector_tweets_limpio    = []    # Arreglo de Tweets putificados
        vector_tweets_sequence  = []    # Arreglo de Tweets.to_sequence()

        for line in lines:

            if ('{' in line):

                try:
                    var_json        = json.loads(line)
                    vector_tweets.append(var_json)
                except:
                    pass

        vector_tweets_limpio    = limpieza_de_datos(vector_tweets)
        vector_tweets_sequence  = sequenciar_tweets(vector_tweets_limpio,1)

        writer.writerows(vector_tweets_sequence)
        writer_original.writerows(sequenciar_tweets(limpieza_retweets(vector_tweets),2))    



    output.close()
    output_original.close()

    print "...Fin del procesamiento"
    print

    print "Archivo limpieza de tweets:  " + ARCHIVO_SALIDA
    print "Archivo sin retweets: " + ARCHIVO_SALIDA_ORIGINAL

    print


main()

