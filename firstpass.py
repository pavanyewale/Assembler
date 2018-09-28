import sys
from print_table import print_table

register=["eax","ecx","edx","ebx","esp","ebp","esi","edi"]
data=[("db",1),("dd",4),("resb",1),("resd",4)]
lines=[]
sym_struct=["Name","Size","No.elements","sym/label","declare/used","Address","Value","Hex"]

def issymbol(sym):
    for i in sym:
        if(ord('a')>ord(i)) or ord(i)>ord('z'):
            return False
    return True

def isdigit(strr):
    for i in strr:
        if(ord(i)<ord('0')) or (ord(i)>ord('9')):
            return False
    return True

def strtohex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)
    return reduce(lambda x,y:x+y, lst)



def indexof(inn,off):
    for i in range(len(inn)):
        if(off==inn[i]):
            return i
    return -1
def searchdata(st):
	for j in data:
		if(j[0]==st):
			return j[1]
	return None 
	
def makeEntry(name,dsize,n,typ,dou,address,value): 
	return [name,dsize,n,typ,dou,address,value,"Not done"]
errorsymbol_tbl=[]
intermediate_code=[]   #output of first_pass
symbol_tbl=[]      #["Name","Size","No.elements","sym/label","declare/used","Address","Value","Hex"]
literal_tbl=[]  #structure ["Literal","Ascii"] 
addr=0

def processdata(l):
	global symbol_tbl,addr,data,intermediate_code
	print("processing data")
	for k in range(l+1,len(lines)):
		if(lines[k][0]=="section"):
			return k
                intermediate_code.append(lines[k])
		if(lines[k][1]=="db"):
			d=lines[k][2]
			s=len(d)
		else:
			d=lines[k][2].split(',')
			s=len(d)
		ds=searchdata(lines[k][1])
		symbol_tbl.append(makeEntry(lines[k][0],ds,s,"S","D",addr,d))
		addr+=s*ds
	return k
		
			
def processbss(l):
	global symbol_tbl,addr,data,intermediate_code
	for k in range(l+1,len(lines)):
		if(lines[k][0]=="section"):
			return k
                intermediate_code.append(lines[k])
		d=None
		s=int(lines[k][2])
		ds=searchdata(lines[k][1])
		symbol_tbl.append(makeEntry(lines[k][0],searchdata(lines[k][1]),s,"S","D",addr,d))
		addr+=s*ds
	return k

def updatesymbol_tbl(name,dou,s):
	global symbol_tbl,addr,data
	f=1
	e=[name,None,None,"L",dou,s,None]
        for k in range(len(symbol_tbl)):
		if(symbol_tbl[k][0]==name):
			f=0
			if(dou=="D"):
				symbol_tbl[k]=e
	if(f):
		symbol_tbl.append(e)

            #if operand is 32 bit register then there is 00 and then register no
            #if operand is 16 bit register then there is 01 and then register no
            #if operand is symbol then there is 10 and then index of symbol symbol_tbl entry of operand

def processoprands1(ops):
        if(isdigit(ops)):
            #handle number literal here
            literal_tbl.append((hex(int(ops))))
            return "lit#"+str(len(literal_tbl))
            return ops 
        if(ops[0]=='"') or (ops[0]=="'"):
                #handle string literal here
                literal_tbl.append(strtohex((ops[:len(ops)-1])[1:]))
                return "lit#"+str(len(literal_tbl))
                return ops
        op1=ops.split('+')
        if(len(op1)>1):
            op11=[]
            for i in op1:
                op11.append(processoprands(i))
            return joinwith(op11,'+')
        else:
            op1=ops.split('*')
            op11=[]
            if(len(op1)>1):
                for i in op1:
                    op11.append(processoprands(i))
                return joinwith(op11,"*")
            else: 
                return processoprands(ops)
def searchsymbol(sym):
    global symbol_tbl
    for i in range(len(symbol_tbl)):
        if((symbol_tbl[i])[0]==sym):
            return i
    return -1
def processoprands(opp):
    global register,symbol_tbl
    k=indexof(register,opp)
    if(k!=-1):
        return "reg#"+str(k)
    if(opp[:5]=="dword"):
        return "dword["+processoprands1(opp[6:len(opp)-1])+"]"
    if(opp[:4]=="byte"):
        return "byte["+processoprands(opp[5:len(opp)-1])+"]"
    if(issymbol(opp)):
        k=searchsymbol(opp)
        if(k!=-1):
            return "sym#"+str(k)
        symbol_tbl.append([opp,None,None,"S","U",None,None])
        return "sym#"+str(len(symbol_tbl)-1)
    else:
        return processoprands1(opp)

def joinwith(li,sym):
    new=""
    for i in range(len(li)):
        new=new+str(li[i])
        if(i==(len(li)-1)):
            return new
        new+=sym
    return new

def processtext(l):
	global symbol_tbl,addr,data,intermediate_code,register
	for k in range(l+1,len(lines)):
            nl=[]
            if((lines[k][0])[len(lines[k][0])-1:]==":"):
                intermediate_code.append(lines[k])
                updatesymbol_tbl((lines[k][0])[:len(lines[k][0])-1],"D",k)
	    else:
			if(lines[k][0] in ["jmp","jnz","jz","call"]):
				updatesymbol_tbl(lines[k][1],"U",None)
                        if(len(lines[k])>1):
                            new=[]
                            new.append(lines[k][0])
                            oprands=lines[k][1].split(',')
                            new1=[]
                            for o in oprands:
                                new1.append(processoprands(o))
                            new.append(joinwith(new1,','))
                            intermediate_code.append(new)
                        else:
                            intermediate_code.append(lines[k])
	return k
def first_pass(fname):
    global lines
    f=open(fname,"r").readlines()
    lines=[[k.strip() for k in i] for i in [i.split(' ') for i in f]]
    for l in range(len(lines)):
	    if(lines[l][0]=="section"):
                    intermediate_code.append(lines[l])
		    if(lines[l][1]==".data"):
			    l=processdata(l)
		    else:
			    if(lines[l][1]==".bss"):
				    l=processbss(l)
			    else:
				    if(lines[l][1]==".text"):
					    l=processtext(l)	

def write_intermediate(fname):
    f2=open(fname+".i","w")
    for i in intermediate_code:
        if(i[0]=="section")|((i[0])[len(i[0])-1:]==":"):
            f2.write(joinwith(i," ")+"\n")
        else:
            f2.write("\t"+joinwith(i," ")+"\n")


first_pass("class1.asm")
print_table("symbol_table",sym_struct,symbol_tbl)

#**************2nd pass****************

