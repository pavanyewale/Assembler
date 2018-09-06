register=["eax","ecx","edx","ebx","esp","ebp","esi","edi"]
data=[("db",1),("dd",4),("resb",1),("resd",4)]
def indexof(inn,off):
    for i in range(len(inn)):
        if(off==inn[i]):
            return i
    return -1
firstpass=[]
def searchdata(st):
	for j in data:
		if(j[0]==st):
			return j[1]
	return None 
	
def makeEntry(name,dsize,n,typ,dou,address,value):
	return [name,dsize,n,typ,dou,address,value]
errortable=[]
table=[]
addr=0
def processdata(l):
	global table,addr,data,firstpass
	print("processing data")
	for k in range(l+1,len(lines)):
		if(lines[k][0]=="section"):
			return k
                firstpass.append(lines[k])
		if(lines[k][1]=="db"):
			d=lines[k][2]
			s=len(d)
		else:
			d=lines[k][2].split(',')
			s=len(d)
		ds=searchdata(lines[k][1])
		table.append(makeEntry(lines[k][0],ds,s,"S","D",addr,d))
		addr+=s*ds
	return k
		
			
def processbss(l):
	global table,addr,data,firstpass
	for k in range(l+1,len(lines)):
		if(lines[k][0]=="section"):
			return k
                firstpass.append(lines[k])
		d=None
		s=int(lines[k][2])
		ds=searchdata(lines[k][1])
		table.append(makeEntry(lines[k][0],searchdata(lines[k][1]),s,"S","D",addr,d))
		addr+=s*ds
	return k
def updatetable(name,dou,s):
	global table,addr,data
	f=1
	e=[name,None,None,"L",dou,s,None]
	for k in range(len(table)):
		if(table[k][0]==name):
			f=0
			if(dou=="D"):
				table[k]=e
	if(f):
		table.append(e)

            #if operand is 32 bit register then there is 00 and then register no
            #if operand is 16 bit register then there is 01 and then register no
            #if operand is symbol then there is 10 and then index of symbol table entry of operand
def processoprands1(ops):
        op1=ops.split('+')
        if(len(op1)>1):
            op11=[]
            for i in op1:
                processoprands(i)
            return joinwith(op11,'+')
        else:
            op1=ops.split('*')
            op11=[]
            if(len(op1)>1):
                for i in op1:
                    processoperands(i)
                return joinwith(op11,"*")
            else: 
                return processoprands(ops)
def searchsymbol(sym):
    global table
    for i in range(len(table)):
        if((table[i])[0]==sym):
            return i
    return -1
def processoprands(opp):
    global register,table
    k=indexof(register,opp)
    if(k!=-1):
        return "00"+str(k)
    if(opp[:5]=="dword"):
        return "dword["+processoprands1(opp[6:len(opp)-1])+"]"
    if(opp[:4]=="byte"):
        return "byte["+processoprands(opp[5:len(opp)-1])+"]"
    k=searchsymbol(opp)
    if(k!=-1):
        return "10"+str(k)
    table.append([opp,None,None,"S","U",None,None])
    return "10"+str(len(table)-1)

def joinwith(li,sym):
    new=""
    for i in range(len(li)):
        new=new+str(li[i])
        if(i==(len(li)-1)):
            return new
        new+=sym
    return new

def processtext(l):
	global table,addr,data,firstpass,register
	for k in range(l+1,len(lines)):
            nl=[]
            if((lines[k][0])[len(lines[k][0])-1:]==":"):
                firstpass.append(lines[k])
                updatetable((lines[k][0])[:len(lines[k][0])-1],"D",k)
	    else:
			if(lines[k][0] in ["jmp","jnz","jz","call"]):
				updatetable(lines[k][1],"U",None)
                        if(len(lines[k])>1):
                            new=[]
                            new.append(lines[k][0])
                            oprands=lines[k][1].split(',')
                            new1=[]
                            for o in oprands:
                                new1.append(processoprands(o))
                            new.append(joinwith(new1,','))
                            firstpass.append(new)
                        else:
                            firstpass.append(lines[k])
	return k
#fname=input("enter file name")
#print(fname)
fname=str(input("Enter file name: "))
f=open(fname,"r").readlines()
lines=[[k.strip() for k in i] for i in [i.split(' ') for i in f]]
for l in range(len(lines)):
	if(lines[l][0]=="section"):
                firstpass.append(lines[l])
		if(lines[l][1]==".data"):
			l=processdata(l)
		else:
			if(lines[l][1]==".bss"):
				l=processbss(l)
			else:
				if(lines[l][1]==".text"):
					l=processtext(l)	

print(firstpass)
#output
#print(table)
f2=open(fname+".fp","w")
for i in firstpass:
    if(i[0]=="section")|((i[0])[len(i[0])-1:]==":"):
        f2.write(joinwith(i," ")+"\n")
    else:
        f2.write("\t"+joinwith(i," ")+"\n")

