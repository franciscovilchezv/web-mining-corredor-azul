class Tweet:

    def __init__(self):

        id_tweet    = None

        id_author   = None

        body_tweet	= None

        date        = None

        esRT        = None

        estado      = None



def main():

    with open("artutufile.txt",'r') as f:

    lines = f.readlines()



        contador = 0;

        listatweets = []



    for line in lines:

        if(line == "FIN TWEET"):

            tweetauxiliar.estado = 0

            contador = 0

            listatweets.append(tweetauxiliar)

        elif(contador == 1):

            tweetauxiliar.id_tweet = line

            contador++

        elif(contador == 2):

            tweetauxiliar.date = line

            contador++

        elif(contador == 5):

            tweetauxiliar.id_author = (line.splits(" "))[0]

            contador++

        elif(contador == 15):

            tweetauxiliar.body_tweet = line

            if "RT" not in line: tweetauxiliar.esRT = 0

            elif: tweetauxiliar.esRT = 1

            contador++

        else:

            contador++


main()


