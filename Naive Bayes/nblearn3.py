import sys, string

stopwords = []
f = open("stopwords.txt","r")
for line in f:
	stopwords.append(line.strip('\n'))

identifiers = []
file_name = sys.argv[1]
f = open(file_name,"r")
for line in f:
	array = line.split(" ")
	identifiers.append(array[0])
     
countdict = {}							#for every word, initialising the counts/incrementing the respective true/fake/pos/neg counts
def addcount(tokenlist,position):
	for t in tokenlist:
		if t in countdict:
			countdict[t][position]=countdict[t][position]+1
		else:
			countdict[t]=[0,0,0,0]
			countdict[t][position]=countdict[t][position]+1
	#print ('---------------------------------------------------------------------------------')
	#print (countdict)

g = open(file_name,"r")
for line in g:
	myarray = line.split(" ")
	mystr = " ".join(line.split(" ")[3:])
	translator = str.maketrans('', '', string.punctuation)
	mynewstr = mystr.translate(translator).lower().strip()
	temptokens = [word for word in mynewstr.split() if word not in stopwords]
	joinedlist = ' '.join(temptokens)
	joinedwithoutnumbers = ''.join([i for i in joinedlist if not i.isdigit()]) 
	temptokens2 = joinedwithoutnumbers.split()
	if (myarray[0] in identifiers):
		if (myarray[1]=='True'):
			addcount(temptokens2,0)
		else:
			addcount(temptokens2,1)
		if (myarray[2]=='Pos'):
			addcount(temptokens2,2)
		else:
			addcount(temptokens2,3)

def smoothing():
    for key in countdict.keys():
        for i in range(0,4):
            countdict[key][i]+=1
smoothing()

TOT_TRUE=0
TOT_FAKE = 0
TOT_POS = 0
TOT_NEG = 0
def count_totals():
	global TOT_TRUE,TOT_FAKE,TOT_POS,TOT_NEG
	for k in countdict.keys():
		TOT_TRUE += countdict[k][0]					#total no.of true words
		TOT_FAKE += countdict[k][1]
		TOT_POS += countdict[k][2]
		TOT_NEG += countdict[k][3]
count_totals()

prob_class1 =TOT_TRUE+TOT_FAKE
prob_class2 = TOT_POS+TOT_NEG

# calculate probabilities
def calc_prob():
    for key, val in countdict.items():
         countdict[key][0] /= TOT_TRUE
         countdict[key][1] /= TOT_FAKE
         countdict[key][2] /= TOT_POS
         countdict[key][3] /= TOT_NEG
calc_prob()

priorOfClassTrue=TOT_TRUE/float(prob_class1)
priorOfClassFake=TOT_FAKE/float(prob_class1)
priorOfClassPos=TOT_POS/float(prob_class2)
priorOfClassNeg=TOT_NEG/float(prob_class2)

def writemodel():
	with open("nbmodel.txt",'w') as g:
		g.write("True" + '|' + str(priorOfClassTrue) + '\n')
		g.write("Fake" + '|' + str(priorOfClassFake) + '\n')
		g.write("Pos" + '|' + str(priorOfClassPos) + '\n')
		g.write("Neg" + '|' + str(priorOfClassNeg) + '\n')
		for k in countdict.keys():
			g.write(k + '|' + str(countdict[k][0]) + '|' + str(countdict[k][1]) + '|' + str(countdict[k][2]) + '|' + str(countdict[k][3]) + '\n')
writemodel()