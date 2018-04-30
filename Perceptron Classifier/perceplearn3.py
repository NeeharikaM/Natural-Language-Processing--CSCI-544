import sys,string
import pickle
import pickletools

 
finalvocabulary = {}
vocabulary_size= 0
file_name = sys.argv[1]
	
stopwords = []								#reading in the stopwords from stopwords.txt and placing them in the list 
f = open("stopwords.txt","r")
for line in f:
	stopwords.append(line.strip('\n'))
	
vocabulary = []
f = open(file_name,"r")
for line in f:
	myarray = line.split(" ")													#split every line and read in the id, true/fake , pos/neg
	id = myarray[0]
	classifier1 = myarray[1]
	classifier2 = myarray[2]
	mystr = " ".join(line.split(" ")[1:])
	translator = str.maketrans('', '', string.punctuation) 						#removing punctuation marks
	mynewstr = mystr.translate(translator).lower().strip()						#converting the sentence to lower case
	temptokens = [word for word in mynewstr.split() if word not in stopwords] 	#removing stopwords
	joinedlist = ' '.join(temptokens)
	joinedwithoutnumbers = ''.join([i for i in joinedlist if not i.isdigit()]) 	#remove digits
	temptokens2 = joinedwithoutnumbers.split()
	vocabulary.extend(temptokens2)												#add it to the vocabulary seen so far
vocabulary = list(set(vocabulary))												#convert into a set to removes duplicates and convert back to a list
vocabulary_size = len(vocabulary)
for i in range(vocabulary_size):
	finalvocabulary[vocabulary[i]]=i+1											#numbering all the words consecutively Ex: {demand:1,seriously:2......}



def WordCount(tokens,finalvocabulary,vocabulary_size):
	arr = [0] * vocabulary_size													#declare an array containing all 0's
	vocab_keys = finalvocabulary.keys()
	for word in tokens:															#if word in present in our vocabulary set the corresponding index to 1 in arr
		if word in vocab_keys:													#no duplicates will be present here
			arr[finalvocabulary[word]-1] = 1
	return arr


def perceptraining():
	g = open(file_name,"r")				
	outputfile_name = ""
	weights_c1 = [0] * vocabulary_size
	weights_c2 = [0] * vocabulary_size
	bias_c1 = 0
	bias_c2 = 0
	iterations = 20
	featurecounts = []
	c1 = []
	c2 = []
	for line in g:
		myarray = line.split(" ")												#for every review do all the pre-processing steps again
		id = myarray[0]
		classifier1 = myarray[1]
		classifier2 = myarray[2]
		mystr = " ".join(line.split(" ")[3:])
		translator = str.maketrans('', '', string.punctuation)
		mynewstr = mystr.translate(translator).lower().strip()
		temptokens = [word for word in mynewstr.split() if word not in stopwords]
		joinedlist = ' '.join(temptokens)
		joinedwithoutnumbers = ''.join([i for i in joinedlist if not i.isdigit()]) 
		temptokens2 = joinedwithoutnumbers.split()
		featurecounts.append(WordCount(temptokens2,finalvocabulary,vocabulary_size))	#collect features array for every review and append
		if classifier1=='True':
			c1.append(1)
		else:
			c1.append(-1)
		if classifier2=='Pos':
			c2.append(1)
		else:
			c2.append(-1)
	weights_for_avg_c1 = [0] * vocabulary_size
	weights_for_avg_c2 = [0] * vocabulary_size
	for iter in range(iterations):														#iterate 20 times for all the sentences
		for i in range(len(featurecounts)): 											#for all sentences
			sum_c1 = 0
			sum_c2 = 0
			for j in range(len(featurecounts[i])): 										#take its corresponding feature array
				sum_c1 = sum_c1 + featurecounts[i][j]*weights_c1[j]						#find dot product of weights*features
				sum_c2 = sum_c2 + featurecounts[i][j]*weights_c2[j]
			activation_c1 = sum_c1 + bias_c1
			activation_c2 = sum_c2 + bias_c2
			if (activation_c1*c1[i]) <= 0:												#if activation is <=0 update the weights and bias: w(weight)=w(weight)+x(feature) bias=bias+y(classification)
				for k in range(len(featurecounts[i])):
					weights_c1[k] = weights_c1[k] + (c1[i]* featurecounts[i][k])
				bias_c1 = bias_c1 + c1[i]
				weights_for_avg_c1 = [a+b for a, b in zip(weights_for_avg_c1, weights_c1)] #and add updated weights to a list stored for calculating averaged perceptron
			else:
				weights_for_avg_c1 = [a+b for a, b in zip(weights_for_avg_c1, weights_c1)] #if >0 simply add to the list stored for calculating averaged perceptron
			if (activation_c2*c2[i]) <= 0:													#repeat procedure for 2nd classifier
				for k in range(len(featurecounts[i])):
					weights_c2[k] = weights_c2[k] + (c2[i]* featurecounts[i][k])
				bias_c2 = bias_c2 + c2[i]
				weights_for_avg_c2 = [a+b for a, b in zip(weights_for_avg_c2, weights_c2)]
			else:
				weights_for_avg_c2 = [a+b for a, b in zip(weights_for_avg_c2, weights_c2)]
	weights_for_avg_c1[:] = [x / len(weights_for_avg_c1) for x in weights_for_avg_c1]    #find averages of all the features by dividing by length
	weights_for_avg_c2[:] = [x / len(weights_for_avg_c2) for x in weights_for_avg_c2]
	output_vanilla_file_name = "vanillamodel.txt"										#write to model files.
	output_averaged_file_name = "averagedmodel.txt"
	with open(output_vanilla_file_name, 'wb') as fd:
		pickle.dump([finalvocabulary,bias_c1,weights_c1,bias_c2,weights_c2],fd,protocol = 0)
	with open(output_averaged_file_name, 'wb') as fd:
		pickle.dump([finalvocabulary,bias_c1,weights_for_avg_c1,bias_c2,weights_for_avg_c2],fd,protocol = 0)
		
perceptraining()
