import sys
import math
from collections import OrderedDict
from _collections import defaultdict
import io
import json
import pickle

transitionprobs = defaultdict(int)
emissionprobs = defaultdict(int)
tagcounts = defaultdict(int)
taglist=[]
possibletags = {}

transitions = defaultdict(int)
emissions = defaultdict(int)
wordswiththeirtags = {}
allAvailableTags = set()
countofemissions= defaultdict(int)
countoftransitions= defaultdict(int)
anslist = []

with open('hmmmodel.txt','rb') as file:
	pickled = pickle.load(file)
transitionprobs = pickled[0]
emissionprobs = pickled[1]
possibletags = pickled[2]
tagcounts = pickled[3]

def writeOutput(backpointerdict, myprevioustag,index,line):
	#print 'writing to file!!!'
	#print backpointerdict
		for i in range(index):
			if (index==0):
				break
			taglist.append(backpointerdict[index][myprevioustag])
			#print taglist
			myprevioustag = backpointerdict[index][myprevioustag]
			#print myprevioustag
			index-=1
			#print index
		if (index ==0):
			reversedtaglist = []
			#print taglist
			y = len(taglist)
			#print y
			for j in range(len(taglist)-1,-1,-1):
				#print j
				reversedtaglist.append(taglist[j])
			#print reversedtaglist
			words = []
			words = line.split(" ")
			#print words
			halftaggedans=""
			for i in range(0, len(words)):
				halftaggedans=halftaggedans+" "+words[i].rstrip()+ "/" + str(reversedtaglist[i])
				#print (halftaggedans)
			anslist.append(halftaggedans.lstrip().rstrip())

def writetofile():
	with io.open("hmmoutput.txt", 'w', encoding='utf-8') as f1:
		for i in range(len(anslist)):
			f1.write(anslist[i])
			f1.write('\n')
	f1.close()
	#seeoutput()
'''
def writeOutput(backpointerdict, myprevioustag,index,line):
	#print 'writing to file!!!'
	#print backpointerdict
	with io.open("hmmoutput.txt", 'w', encoding='utf-8') as f1:
		for i in range(index):
			if (index==0):
				break
			taglist.append(backpointerdict[index][myprevioustag])
			#print taglist
			myprevioustag = backpointerdict[index][myprevioustag]
			#print myprevioustag
			index-=1
			#print index
		if (index ==0):
			reversedtaglist = []
			#print taglist
			y = len(taglist)
			#print y
			for j in range(len(taglist)-1,-1,-1):
				#print j
				reversedtaglist.append(taglist[j])
			#print reversedtaglist
			words = []
			words = line.split(" ")
			#print words
			halftaggedans=""
			for i in range(0, len(words)):
				halftaggedans=halftaggedans+" "+words[i].rstrip()+ "/" + str(reversedtaglist[i])
				#print halftaggedans
			f1.write(halftaggedans.lstrip().rstrip())
			f1.write('\n')
			f1.close()
	#seeoutput()
'''
'''	
def seeoutput():
	g = open('hmmoutput.txt', "r", encoding='utf-8')
	count = 0
	for line in g:
		count = count+1
		print (line)
	print (count)
'''
		
def tracelasttag(backpointerdict, seentransactions,line):
	#print backpointerdict
	lasttag = max(seentransactions, key=lambda k: seentransactions[k])
	taglist.append(lasttag[1])
	#answer.append(lasttag[0]+"/"+lasttag[1])
	writeOutput(backpointerdict,lasttag[1],lasttag[2],line)


		
def TagMyData():
		#print (possibletags)
		g = open(sys.argv[1], "r", encoding='utf-8')
		for line in g:
			tokens = line.strip().split(" ")
			level = 0
			backpointerdict = dict()
			seentransactions = {}
			count = 0
			answer = []
			for token in tokens:
				temporarylist = {}
				if (count==0):
					if(token in possibletags):
						#print ('jhlkjfdols')
						for currenttag in possibletags[token]:
							#print (currenttag)
							transtuple = ('Q0',currenttag)
							transprob = transitionprobs[transtuple]
							emissiontuple = (token,currenttag)
							emissionprob = emissionprobs[emissiontuple]
							myprob = math.log(float(transprob),10) + math.log(float (emissionprob),10)
							seentransactions[tuple([token,currenttag,level])]= myprob
							#print (seentransactions)
					else:
						#print 'word unseen!' 
						#print transitionprobs
						for j in transitionprobs:
							#print j
							if j[0] == 'Q0' and j[1]!= 'Q0':
								seentransactions[tuple([token, j[1], level])] = math.log(transitionprobs[j],10)
								#print seentransactions		
				else:
					if(token in possibletags):
						tempD={}
						temptag = ''
						tempseentransaction = ''
						for currenttag in possibletags[token]:
							max = -float("inf")
							#print seentransactions
							for i in seentransactions:
								#print i
								#print seentransactions[i]
								#print 'errrrrrr'
								transprob = transitionprobs[tuple([i[1],currenttag])]
								emissionprob = emissionprobs[tuple([token,currenttag])]
								myprob = math.log(float(transprob),10) + math.log(float (emissionprob),10) + float (seentransactions[i])
								if(myprob>max):
									max = myprob
									temptag = currenttag
									tempseentransaction = i
							tempD[tuple([token, temptag, level])] = max
							temporarylist[temptag]=tempseentransaction[1]
					else:
						#print 'word not first and unseen!'
						tempdict={}
						tempD = {}
						for k1 in seentransactions:
							#print k1
							for keys in transitionprobs:
								#print keys
								if k1[1] == keys[0]:
									val2 =math.log(transitionprobs[keys],10) + float(seentransactions[k1])
									tempdict[tuple([keys[0],keys[1],level])]=val2
									#print tempdict
						tempdictsorted = OrderedDict(sorted(tempdict.items(), key=lambda x: x[1],reverse=True)) #desc sort
						#print tempdictsorted
						tempdict2={}
						tagdict={}
						for k in tempdictsorted:
							#print tagdict
							#print k[1]	
							if(k[1] not in tagdict):
								tempdict2[k]=tempdictsorted[k]
							#print tempdict2
							tagdict[k[1]] = 1
							#print tagdict
						for k1 in tempdict2:
							tempD[tuple([token, k1[1], level])] = tempdict2[k1]
							#print tempD
							temporarylist[k1[1]] = k1[0]
							#print temporarylist
				count = count+1
				backpointerdict[level]=temporarylist
				if count>1:
					seentransactions=tempD
				level += 1
			#print (seentransactions)
			tracelasttag(backpointerdict, seentransactions,line)			

def main():
	TagMyData()
	#print (anslist)
	writetofile()

if __name__ == "__main__":
     main()
