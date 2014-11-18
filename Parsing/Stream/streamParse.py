# -*- coding: utf-8 -*-
import json

import string

import warnings
warnings.filterwarnings("ignore")

import unicodedata

import csv

import re
#import regex
from nltk.corpus import stopwords

DELIMITER = '|'

ARCHIVO_SALIDA_ORIGINAL = "Corredor Azul/Modificados/Dias/corredor_azul_stream.csv"
ARCHIVO_SALIDA = 'Corredor Azul/Modificados/Dias/output_vAO.csv'

ARCHIVOS_ENTRADA = [
    "Corredor Azul/Modificados/Dias/1/1.txt",
    "Corredor Azul/Modificados/Dias/2/2.txt",
    "Corredor Azul/Modificados/Dias/3/3.txt",
    "Corredor Azul/Modificados/Dias/4/4.txt",
    "Corredor Azul/Modificados/Dias/5/5.txt",
    "../Search/output.csv"
]

CARACTERES = [
    '“',
    '¿',
    '►',
    '¡',
    '“',
    '”',
    '«',
    '»',
    '´',
    '`',
    '’'
]
CARACTERES_UTF8 = [u'►', u'“', u'”', u'’', u'´', u'`', u'¿', u'¡', u'«', u'»']

class Tweet:

    id_tweet    = None
    id_author   = None
    tweet_original  = None
    body_tweet  = None
    date        = None
    esRT        = None
    estado      = None
    cant_terminos = None


    def __init__(self):
        self.id_tweet    = None
        self.id_author   = None
        self.tweet_original  = None
        self.body_tweet  = None
        self.date        = None
        self.esRT        = None
        self.estado      = None
        self.cant_terminos = None
        

    def load_json(self,post):
        self.id_tweet    = post["id"]
        self.id_author   = post["user"]["id"]

        texto = post["text"].replace('\n',". ")
        texto = texto.replace('\r'," ")

        self.tweet_original = str(texto.encode('utf-8'))

        self.body_tweet  = str(texto.encode('utf-8'))

        self.date        = post["created_at"]

        if ("retweeted_status" in post.keys()) or ("RT" in self.body_tweet.split()):
            self.esRT = 1
        else: 
            self.esRT = 0

        self.estado      = 0 # Sin calificar (se agina automaticamente de acuerdo a las caritas)
        self.cant_terminos = 0 # se asignara el valor correcto luego de la limpieza

    def load_csv(self,post):
        
        #print post

        self.id_tweet    = post[0]
        self.id_author   = post[1]

        texto = post[2].replace('\n',". ")
        texto = texto.replace('\r'," ")

        self.tweet_original = texto
        self.body_tweet  = texto

        self.date        = post[4]
        self.esRT = post[5]
        self.estado = post[6]
        self.cant_terminos = post[7]

    
    def to_CSV(self):
        output = ""
        output += str(self.id_tweet) + DELIMITER
        output += str(self.id_author) + DELIMITER
        output += str(self.tweet_original) + DELIMITER
        output += str(self.body_tweet) + DELIMITER
        output += str(self.date) + DELIMITER
        output += str(self.esRT) + DELIMITER
        output += str(self.estado) + DELIMITER
        output += str(self.cant_terminos) + "\n"

        return output
    

    def to_sequence(self,tipo):

        if(tipo == 1):
            sequence = [self.id_tweet, self.id_author, self.tweet_original, self.body_tweet, self.date, self.esRT, self.estado, self.cant_terminos]
        else:
            sequence = [self.id_tweet, self.id_author, self.tweet_original, self.body_tweet, self.date, self.esRT, str(0)]

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

def limpieza_retweets(vector_tweets,fuente):
    dev = []

    for var_json in vector_tweets:

        item = Tweet()
        if(fuente == "txt"):
            item.load_json(var_json)
        else:
            try:
                if(len(var_json.split("|")) == 8):
                    item.load_csv(var_json.split("|"))
                else:
                    continue
            except:
                continue


        # Eliminar RT
        if (item.esRT):
            continue

        dev.append(item)

    return dev



def limpiezaNLTK(body_tweet):

    
    scentence = body_tweet

    #remove punctuation and split into seperate words
    regex_punctuation = re.compile('[%s]' % re.escape(string.punctuation))
    scentence = regex_punctuation.sub(' ', scentence)
    #scentence = scentence.translate(string.maketrans("",""), string.punctuation)

    for chara in CARACTERES:
        scentence.replace(chara,' ')
    #for chara in CARACTERES_UTF8:
    #    scentence.decode('utf-8').replace(chara,' ').encode('utf-8')
        #scentence.replace(chara,' ')

    #Remove numbers
    scentence = re.sub('[0-9]', '', scentence)
    scentence = re.sub(ur'(?iu)[¿¡´`“”►«»·]', '', scentence.decode('utf-8')).encode('utf-8')
    #scentence = regex.sub(u'[^\p{Spanish}\p{Zs}]', '', scentence.decode('utf-8')).encode('utf-8')

    #We only want to work with lowercase for the comparisons
    #scentence = scentence.lower()
    #Para convertir a minusculas las palabras acentuadas y la Ñ
    scentence = scentence.decode('utf-8').lower().encode('utf-8')
    scentence = re.sub(ur'(?iu)[^a-záéíóúñü ]', '', scentence.decode('utf-8')).encode('utf-8')
    #scentence = re.sub('[¿¡´`“”►«»]', '', scentence, re.UNICODE)

    # split
    words = scentence.split() #re.findall(r'\w+', scentence,flags =  0)

    #This is the simple way to remove stop words
    important_words=[]
    cadena = ""
    for word in words:
        try:
            #if word not in stopwords.words('spanish'):
            if word.decode('utf-8') not in stopwords.words('spanish'):
                #print word.decode('utf-8'), word
                important_words.append(word)
                cadena = cadena + " " + word
        except:
            pass

    
    if ((cadena != "") and (' ' in cadena[0])):
        cadena = cadena[1:]

    return cadena


    #This is the more pythonic way
    #important_words = filter(lambda x: x not in stopwords.words('spanish'), words)

    #print important_words 


def limpia_mal(tweet):

    # item.body_tweet = re.sub('\\b' + palabra + '\\b', '', item.body_tweet, flags=re.IGNORECASE)

    devolver = ""

    tweet = tweet.replace("#CorredorAzul","servicio")
    tweet = tweet.replace("#corredorazul","servicio")

    insensitive_string = re.compile(re.escape('corredor azul'), re.IGNORECASE)
    tweet = insensitive_string.sub('servicio', tweet)

    insensitive_string = re.compile(re.escape('corredorazul'), re.IGNORECASE)
    tweet = insensitive_string.sub('servicio', tweet)

    for word in tweet.split():
        if("#" in word):
            continue

        if("@" in word):
            continue

        if ("http://" in word):
            continue

        if(devolver == ""):
            devolver = word
        else:
            devolver = devolver + " " + word


    return devolver


def limpieza_de_datos(vector_tweets,fuente):
    dev = []
    porcentaje = 0

    for var_json in vector_tweets:

        item = Tweet()
        if(fuente == "txt"):
            item.load_json(var_json)
        else:
            try:
                if(len(var_json.split("|")) == 8):
                    item.load_csv(var_json.split("|"))
                else:
                    continue
            except:
                continue

        if(fuente == "txt"):
            # Eliminar RT
            if (item.esRT):
                continue
        else:
            if( item.esRT == 1):
                continue

        # Valorizacion automatica por los emoticones en el body_tweet :) :D =) =( :(
        happy_faces = [':)', ':D', '=)', '(:', '(=', ';)']
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

        if (fuente == "txt"):
            # Limpieza de Usuarios (Se procederá a eliminar a los usuarios en los textos)
            for user in var_json["entities"]["user_mentions"]:
                usuario = "@" + user["screen_name"]           
                item.body_tweet = item.body_tweet.replace(usuario.encode('utf-8'),'')


            # Limpieza de links (Se prodecerá a eliminar los links en los textos)
            for url in var_json["entities"]["urls"]:
                item.body_tweet = item.body_tweet.replace(url["url"].encode('utf-8'),'')


            # Limpieza de hashtags (Se reemplaza #CorredorAzul por servicio y tambien 'corredor azul' y 'corredorazul' y se eliminan los restantes)
            #item.body_tweet = item.body_tweet.decode('unicode_escape').encode('ascii','replace')

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

        else:
            # Limpieza a la mala del CSV
            item.body_tweet = limpia_mal(item.body_tweet)

        
        # LimpiezaNLTK
        item.body_tweet = limpiezaNLTK(item.body_tweet)

        # Limpieza de palabras con longitud menor a 3
        for palabra in item.body_tweet.split():
            if (len(palabra.decode('utf-8')) < 3):
                item.body_tweet = re.sub('\\b' + palabra + '\\b', '', item.body_tweet, flags=re.IGNORECASE)

        # Guardar la cantidad de terminos que quedaron
        item.cant_terminos = len(item.body_tweet.split())


        # Elimino los que quedaron vacios
        if (item.body_tweet == ""):
            continue


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
        vector_tweets_limpio    = []    # Arreglo de Tweets purificados
        vector_tweets_sequence  = []    # Arreglo de Tweets.to_sequence()


        # Determino la fuente de donde viene (csv, txt)
        fuente = ""
        if ('.csv' in in_file):
            fuente = "csv"
            print "Archivo tipo CSV"
        else:
            fuente = "txt"
            print "Archivo tipo JSON"



        for line in lines:

            if (fuente == "txt"):
                if ('{' in line):
                    try:
                        var_json        = json.loads(line)
                        vector_tweets.append(var_json)
                    except:
                        pass
            else:
                if (line[0] == '"'):
                    line = line[1:-3]
                if(len(line) > 10):
                    vector_tweets.append(line)


        vector_tweets_limpio    = limpieza_de_datos(vector_tweets,fuente)
        vector_tweets_sequence  = sequenciar_tweets(vector_tweets_limpio,1)


        writer.writerows(vector_tweets_sequence)
        writer_original.writerows(sequenciar_tweets(limpieza_retweets(vector_tweets,fuente),2))    



    output.close()
    output_original.close()

    print "...Fin del procesamiento"
    print

    print "Archivo limpieza de tweets:  " + ARCHIVO_SALIDA
    print "Archivo sin retweets: " + ARCHIVO_SALIDA_ORIGINAL

    print


main()

