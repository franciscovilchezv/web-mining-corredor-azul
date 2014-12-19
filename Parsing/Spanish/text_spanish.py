# -*- coding: utf-8 -*-
import nltk

def bag_of_words():
    raw_words = []
    file = open("raw_words.txt", 'r')
    #words = file.readlines()
    for line in file:
        words = line.split(' ')
        processed = []
        for word in words:
            if (word != '') & (word != '\n'):
                word = word.replace('\n', '')
                processed.append(word)
        #print words
        raw_words.extend(processed)
    file.close()
    print len(raw_words)
    bag_of_words = list(set(raw_words))
    print len(bag_of_words)
    #print bag_of_words
    bag_of_words = sorted(bag_of_words)
    #print bag_of_words

    fout = open("bag_of_words.txt", "w")
    for word in bag_of_words:
        fout.write(word + ' ')
    fout.close()


def process_spanish():
    file_valid = open('valid_words.txt', "r")
    lines = file_valid.readlines()
    valid_words = lines[0].split(' ')
    print len(valid_words)
    file_valid.close()
    #valid_words = set(valid_words)

    file = open("raw_words.txt", 'r')
    fileout = open("spanish_words_servicio.txt", 'w')
    for line in file:
        words = line.split(' ')
        processed = []
        ini_line = True
        for word in words:
            if (word != '') & (word != '\n') & (word != 'servicio') & (word != 'servicio\n'):
                word = word.replace('\n', '')
                if word in valid_words:
                    processed.append(word)
                    if ini_line:
                        fileout.write(word)
                        ini_line = False
                    else:
                        fileout.write(' ' + word)
        fileout.write('\n')
    file.close()
    fileout.close()


def process_spanish_owned():
    from inflector import Inflector, Spanish
    inflector = Inflector(Spanish)

    from nltk.stem import SnowballStemmer
    stemmer = SnowballStemmer("spanish")

    file_valid = open('valid_words.txt', "r")
    lines = file_valid.readlines()
    valid_words = lines[0].split(' ')
    print len(valid_words)
    file_valid.close()
    #valid_words = set(valid_words)
    owned_words = ['cúster', 'custer', 'cústers', 'custers', 'combi', 'combis', 'susana', 'villaran', 'villarán', 'castañeda']

    file = open("raw_words.txt", 'r')
    fileout = open("spanish_words_owned.txt", 'w')
    fout_sing = open("spanish_words_sing.txt", 'w')
    fout_stem = open("spanish_words_stem.txt", 'w')
    nline = 0

    for line in file:
        nline += 1
        words = line.split(' ')
        processed = []
        ini_line = True
        for word in words:
            if (word != '') & (word != '\n') & (word != 'servicio') & (word != 'servicio\n'):
                word = word.replace('\n', '')
                if (word in valid_words) | (word in owned_words):
                    processed.append(word)
                    if word != 'bus':
                        word_singular = inflector.singularize(word)
                        #word_singular = word_singular.replace(u'\xF3'.encode('utf-8'), 'o')
                    else:
                        word_singular = word
                    word_stemmed = stemmer.stem(word.decode('utf-8')).encode('utf-8')
                    if ini_line:
                        fileout.write(word)
                        fout_sing.write(word_singular)
                        fout_stem.write(word_stemmed)
                        ini_line = False
                    else:
                        fileout.write(' ' + word)
                        fout_sing.write(' ' + word_singular)
                        fout_stem.write(' ' + word_stemmed)
                    print nline, word, word_singular, word_stemmed
        fileout.write('\n')
        fout_sing.write('\n')
        fout_stem.write('\n')
    file.close()
    fileout.close()
    fout_sing.close()
    fout_stem.close()

def twitter_datetime():
    from datetime import datetime
    file = open('fechas_twitter.txt', 'r')
    fout = open('fechas_python.txt', 'w')
    for line in file:
        line = line.replace('\n', '')
        if len(line) > 20:
            #print line
            ts = datetime.strptime(line, '%a %b %d %H:%M:%S +0000 %Y')
            #print ts
            fout.write(str(ts)+'\n')
            #ts = datetime.strftime('%m-%d-%Y %H:%M:%S', ts)
            #print ts
        else:
            #print line
            fout.write(line+'\n')

#process_spanish_owned()
twitter_datetime()