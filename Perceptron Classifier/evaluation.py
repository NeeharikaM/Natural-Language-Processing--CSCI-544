f1 = open("dev-key.txt")
f2 = open("percepoutput.txt")

counter = 0

data_in = []
data_out = []

data_in += f1
data_out += f2

for i in range(0, len(data_in)):
	l1 = data_in[i].split()
	l2 = data_out[i].split()
	if(l1[1]==l2[1] and l1[2]==l2[2]):
		counter += 1
print (len(data_in))
print (counter)