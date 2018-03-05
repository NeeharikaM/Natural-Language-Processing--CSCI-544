from collections import defaultdict
import sys
import itertools
import pickle
import pickletools
import json

#using default dicts so that we dont need to check for existence of a particular key before inserting
countofemissions= defaultdict(int)
countoftransitions= defaultdict(int)
transitions = defaultdict(int)
emissions = defaultdict(int)
wordswiththeirtags = {}
allAvailableTags = set()

transitionprobs = defaultdict(int)
emissionprobs = defaultdict(int)
possibletags = {}
tagcounts = defaultdict(int)

def main():
	f = open(sys.argv[1],"r",encoding='utf-8')
	for line in f:
		startnode="Q0"
		countofemissions[startnode] += 1
		tokens = line.strip().split(" ")
		for token in tokens:
			countoftransitions[startnode] += 1
			slashindex= token.rfind('/')
			currentword = token[:slashindex]
			currenttag = token[slashindex+1:]
			countofemissions[currenttag] += 1
			transitions[(startnode, currenttag)] += 1
			#print transitions
			allAvailableTags.add(startnode)
			allAvailableTags.add(currenttag)
			emissions[(currentword, currenttag)] += 1
			if currentword not in wordswiththeirtags:
				wordswiththeirtags[currentword] = set()
			wordswiththeirtags[currentword].add(currenttag)
			startnode = currenttag
	writemodel()
	file_name = "hmmmodel.txt"
	with open(file_name, 'wb') as fd:
		pickle.dump([transitionprobs,emissionprobs,possibletags,tagcounts],fd,protocol = 0)
		#pickletools.dis(pickle.dumps([transitionprobs,emissionprobs,possibletags,tagcounts]),out=fd)



def writemodel():
	for i in itertools.combinations_with_replacement(allAvailableTags,2):
			if(i not in transitions) and (i[1] != 'Q0'):
				transitions[i]=0
			if(tuple([i[1],i[0]]) not in transitions) and (i[0] != 'Q0'):
				transitions[tuple([i[1],i[0]])]=0
			for key in transitions:
				val=((transitions[key]+1) / (float(len(countoftransitions)-1) + countoftransitions[str(key[0])]))
				transitionprobs[(str(key[0]),str(key[1]))] = float(str(val))
	for key in emissions:
			val= float((emissions[key]) / (float(countofemissions[str(key[1])])))
			emissionprobs[(str(key[0]),str(key[1]))] = float(str(val))
	for key, value in wordswiththeirtags.items():
			possibletags[key] = tuple(value)
	for key, value in countofemissions.items():
			tagcounts[key] = float(str(value))

			
'''    
def writemodel():
	with open("hmmmodel.txt", mode='w+') as g:
		g.write("<---Words with the associated tags-->" + '\n')
		for key, value in wordswiththeirtags.items():
			g.write(key + " " + ','.join([str(i) for i in value]) + "\n")
		g.write("<---Number of occurences of tags-->" + '\n')
		for key, value in countofemissions.items():
			g.write(key + " " + str(value) + "\n")
'''
if __name__ == "__main__":
     main()
