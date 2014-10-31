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
		self.id_tweet    = post[0]
		self.id_author   = post[1]

		self.body_tweet  = post[2].split()

		self.date        = post[3]
		self.esRT = post[4]
		self.estado = post[5]

def main():

	print "Inicio..."

	with open("output.csv",'rb') as csvfile:
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