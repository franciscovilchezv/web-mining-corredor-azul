# -*- coding: utf-8 -*-
import json

import csv

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

	def __init__(self,post):
		self.id_tweet    = post[0]
		self.id_author   = post[1]

		self.tweet_original = post[2]
		self.body_tweet  = post[3].split()

		self.date        = post[4]
		self.esRT = post[5]
		self.estado = post[6]
		self.cant_terminos = post[7]

def main():

	print "Inicio..."

	with open("Corredor Azul/Modificados/Dias/output.csv",'rb') as csvfile:
		lines = csvfile.readlines()


	# En esta variable estan todos los tweets
	tweets = []

	for line in lines:
		line = line.replace("\n","")
		line = line.replace("\r","")

		fields = line.split('|')
	
		tweet = Tweet(fields)

		tweets.append(tweet)


	print "Done"

main()