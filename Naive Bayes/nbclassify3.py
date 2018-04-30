import sys, string
import math

priorprobs = {} 
tokenprobs = {}
output=open("nboutput.txt",'w')

f = open('nbmodel.txt',"r")
for line in f:
	input = line.strip().split("|")
	#print(type(input[0]))
	#print(input[0])
	if (len(input)==2):
		priorprobs[input[0]] = float(input[1])
	else:
		tokenprobs[input[0]] = [float(input[1]),float(input[2]),float(input[3]),float(input[4])]
		
#print (priorprobs)
#print (tokenprobs)		

stopwords = []
f = open("stopwords.txt","r")
for line in f:
	stopwords.append(line.strip('\n'))

file_name = sys.argv[1]
#print (file_name)

def naivebayesclassifier():	
	g = open(file_name,"r")
	mystr = ""
	tokens = []
	for line in g:
		myarray = line.split(" ")
		#mytokens = line.split(" ")[3:]
		mystr = " ".join(line.split(" ")[3:])
		#print(myarray)
		#for j in range(3,len(myarray)):
			#mystr+=myarray[j]+" "
		#print(mystr)
		translator = str.maketrans('', '', string.punctuation)
		mynewstr = mystr.translate(translator).lower().strip()
		temptokens = [word for word in mynewstr.split() if word not in stopwords]
		joinedlist = ' '.join(temptokens)
		joinedwithoutnumbers = ''.join([i for i in joinedlist if not i.isdigit()]) 
		temptokens2 = joinedwithoutnumbers.split()
		#for i in range(len(temptokens)):
			#temptokens2 = []
			#if (temptokens[i].isdigit()==False):
				#temptokens2.append(temptokens[i])
		true_prob = 0
		fake_prob = 0 
		pos_prob = 0
		neg_prob = 0
		for i in temptokens2:	
			if(i in tokenprobs):
				true_prob += math.log(tokenprobs[i][0])
				fake_prob += math.log(tokenprobs[i][1])
				pos_prob +=math.log(tokenprobs[i][2])
				neg_prob += math.log(tokenprobs[i][3])
		true_prob += math.log(priorprobs['True'])
		fake_prob += math.log(priorprobs['Fake'])
		pos_prob += math.log(priorprobs['Pos'])
		neg_prob += math.log(priorprobs['Neg'])
		if (true_prob>fake_prob):
			first_classification = 'True'
		else:
			first_classification = 'Fake'
		if (pos_prob>neg_prob):
			second_classification = 'Pos'
		else:
			second_classification = 'Neg'
		output.write(myarray[0]+" "+first_classification+" "+second_classification)
		output.write("\n")
naivebayesclassifier()
