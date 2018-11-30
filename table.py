f = open("array.asm","r")
f1 = open("onepass","w")
t =[]
def searchlabel(arr,label):
	m=0
	for i in arr:
		m+=1
		if i[0]==label:
			i[6]='D'
			return [0]+[m]
	return [1]+[m]
#find symbol in symbol table if there return symbol entry +20(for symbol) if not there add entry in symbol table
def findsymbol(sym):
	j=1;
	for i in t:
		if(i[0]==sym):
			return "20"+str(j)
		j+=1
	#t.append([sym]+[m[1]]+[1]+[len(m[1])]+[1*len(m[1])]+['S']+['D']+[size])
	t.append([sym]+['-']+['-']+['-']+['-']+['S']+['U']+["line number"])
	return "20"+str(j)
	
#change register by some number for matchin level
def regentry(arr):
	arr = arr.strip().split(",")
	reg = [("eax","000"),("ebx","001"),("ecx","011"),("edx","100"),("esp","101"),("ebp","101"),("edi","110")]
	for i in reg:
		if dict(reg).get(str(arr[0])) and dict(reg).get(str(arr[1])):
			return dict(reg).get(str(arr[0]))+" "+dict(reg).get(str(arr[1]))
		if dict(reg).get(str(arr[0])):
			return dict(reg).get(str(arr[0]))+" "+findsymbol(str(arr[1]))
		if dict(reg).get(str(arr[1])):
			return findsymbol(str(arr[0]))+" "+dict(reg).get(str(arr[1]))
size =0
for line in f:
	if ".bss" in line:
		break
	if "\"" in line:	
		m = line.strip().split("\"")
		
		t.append([(str(m[0]).split(" "))[0]]+[m[1]]+[1]+[len(m[1])]+[1*len(m[1])]+['S']+['D']+[size])
		size +=1*len(m[1])
		
	elif "dd" in line:
		m = line.strip().split(" ")
		vlen = len(str(m[2]).split(","))
		t.append([m[0]]+[m[2]]+[4]+[vlen]+[vlen*4]+['S']+['D']+[size])
		size+=4*vlen
	f1.write(line) #writing in tmp file

lineno =0
#for i in reg:
#	print(dict(reg).get("eax"))

f1.write(line) #writing in tmp file
for line in f:
	lineno+=1
	if ":" in line:
		m=(line.split(":"))[0]
		if searchlabel(t,m):
			t.append([m]+['-']+['-']+['-']+['-']+['L']+['U']+[lineno])
		f1.write(line) #writing in tmp file
		
	elif "jnz" in line or "jmp" in line or "jz" in line:
		m=(line.strip().split(" "))
		xx=searchlabel(t,m[1])
		if(xx[0]==1):
			t.append([m]+['-']+['-']+['-']+['-']+['L']+['U']+['-'])
		f1.write(str(m[0])+" "+str(xx[1])+"\n") #writing in tmp file
		

	elif "mov" in line:
		f1.write("mov "+regentry(line.split(" ")[1])+"\n")
	else:
		f1.write(line) #writing in tmp file
print(t)
