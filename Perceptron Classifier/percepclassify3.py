import sys,string
import pickle
import pickletools

finalvocabulary = {}
bias_c1 = 0
weights_c1 = []
bias_c2 = 0
weights_c2 = []

stopwords = []
f = open("stopwords.txt","r")
for line in f:
	stopwords.append(line.strip('\n'))

model_file_name = sys.argv[1]  
dev_file_name = sys.argv[2]

with open(model_file_name,'rb') as file:								#read in the model
	pickled = pickle.load(file)
finalvocabulary = pickled[0]
bias_c1 = pickled[1]
weights_c1 = pickled[2]
bias_c1 = pickled[3]
weights_c2 = pickled[4]

vocabulary_size = len(finalvocabulary)

def WordCount(tokens,finalvocabulary,vocabulary_size):
	arr = [0] * vocabulary_size
	vocab_keys = finalvocabulary.keys()
	for word in tokens:
		if word in vocab_keys:
			arr[finalvocabulary[word]-1] = 1
	return arr
	
def classify():
	result = []
	g = open(dev_file_name,"r")  										#pre-process the lines
	for line in g:
		sum_c1 = 0
		sum_c2 = 0
		myarray = line.split(" ")
		id = myarray[0]
		mystr = " ".join(line.split(" ")[1:])
		translator = str.maketrans('', '', string.punctuation)
		mynewstr = mystr.translate(translator).lower().strip()
		temptokens = [word for word in mynewstr.split() if word not in stopwords]
		joinedlist = ' '.join(temptokens)
		joinedwithoutnumbers = ''.join([i for i in joinedlist if not i.isdigit()]) 
		temptokens2 = joinedwithoutnumbers.split()
		features = WordCount(temptokens2,finalvocabulary,vocabulary_size) #get the line's features
		for i in range(len(features)):									  #find dot product of features and weights
			sum_c1 = sum_c1+features[i]*weights_c1[i]
			sum_c2 = sum_c2+features[i]*weights_c2[i]
		activation_c1 = sum_c1 + bias_c1
		activation_c2 = sum_c2 + bias_c2
		if activation_c1 > 0:
			class1 = "True"
		else:
			class1 = "Fake"

		if activation_c2 > 0:
			class2 = "Pos"
		else:
			class2 = "Neg"
		result.append([id, class1, class2])
	return result
	
result = classify()

with open("percepoutput.txt", "w") as f:
	for r in result:
		f.write(" ".join(r) + "\n")
		