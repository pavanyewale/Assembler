import sys
from tabulate import tabulate
register=["eax","ecx","edx","ebx","esp","ebp","esi","edi"]
data=[("db",1),("dd",4),("resb",1),("resd",4)]
lines=[]
sym_struct=["Name","Size","No.elt","s/lbl","dc/ud","Addr","Value","line no"]
error_tbl=[]
intermediate_code=[]   #output of first_pass
symbol_tbl=[]      #["Name","Size","No.elements","sym/label","declare/used","Address","Value","Hex"]
literal_tbl=[]  #structure ["Literal","Ascii"] 
addr=0
spass=[]
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

def inttohex(intt):
    ss="00000000"
    ss+=hex(intt)[2:]
    return (ss[len(ss)-8:]).upper()

def indexof(inn,off):
    for i in range(len(inn)):
        if(off==inn[i]):
            return i
    return -1

def big_endian(hexx):
    return hexx[6:]+hexx[4:6]+hexx[2:4]+hexx[0:2]

def sizeofdata(st):
	for j in data:
		if(j[0]==st):
			return j[1]
	return None 
	

def insert_symbol_tbl(entry):
    global symbol_tbl
    for i in range(len(symbol_tbl)):
        if(entry[0]==symbol_tbl[i][0]):
            if(symbol_tbl[i][4]=='U') and (entry[4]=='D'):
                symbol_tbl[i]=entry
            return i
    symbol_tbl.append(entry)
    return len(symbol_tbl)-1

def processdata(l):
    global symbol_tbl,addr,data,intermediate_code,spass
    print("processing data")
    for k in range(l+1,len(lines)):
	if(lines[k][0]=="section"):
	    return k
	if(lines[k][1]=="db"):
	    d=lines[k][2]
            literal_tbl.append([lines[k][2],strtohex(lines[k][2])])
	    s=len(d)
	else:
	    d=lines[k][2].split(',')
	    literal_tbl.append([lines[k][2],inttohex(int(lines[k][2]))])
            s=len(d)
	ds=sizeofdata(lines[k][1])
        symlen=len(symbol_tbl)
	new=insert_symbol_tbl([lines[k][0],ds,s,"S","D",addr,d,k+1])
        intermediate_code.append(["sym#"+str(new),lines[k][1],"lit#"+str(len(literal_tbl))])
        spass.append(["sym#"+str(new),lines[k][1],"lit#"+str(len(literal_tbl))])
        if(new<symlen):
            error_tbl.append(["Line No:"+str(k)+" Redeclaration of symbol "+lines[k][0]])
	addr+=s*ds
    return k
		
			
def processbss(l):
	global symbol_tbl,addr,data,intermediate_code
	for k in range(l+1,len(lines)):
		if(lines[k][0]=="section"):
			return k
                if(len(lines[k])<3):
                    error_tbl.append("Line "+str(k)+" instruction expected")
                    continue
                d=None
		s=int(lines[k][2])
		ds=sizeofdata(lines[k][1])
		symlen=len(symbol_tbl)
                ss=insert_symbol_tbl([lines[k][0],sizeofdata(lines[k][1]),s,"S","D",addr,d,k+1])
                
                if(ss<symlen):
                    error_tbl.append(["Line No:"+str(k)+" Redeclaration of symbol "+lines[k][0]])
		
                addr+=s*ds
                intermediate_code.append(["sym#"+str(ss),lines[k][1],lines[k][2]])
                spass.append(["sym#"+str(ss),lines[k][1],lines[k][2]])
	return k

def updatesymbol_tbl(name,dou,s,k):
	global symbol_tbl,addr,data
	f=1
	e=[name,None,None,"L",dou,s+1,None,k+1]
        for k in range(len(symbol_tbl)):
            if(symbol_tbl[k][0]==name):
			f=0
			if(dou=="D"):
				symbol_tbl[k]=e
                        return k
	if(f):
		symbol_tbl.append(e)
                return len(symbol_tbl)-1

            #if operand is 32 bit register then there is 00 and then register no
            #if operand is 16 bit register then there is 01 and then register no
            #if operand is symbol then there is 10 and then index of symbol symbol_tbl entry of operand

def processoprands1(ops):
        if(isdigit(ops)):
            #handle number literal here
            literal_tbl.append([ops,(inttohex(int(ops)))])
            return "lit#"+str(len(literal_tbl))
            return ops 
        if(ops[0]=='"') or (ops[0]=="'"):
                #handle string literal here
                literal_tbl.append([ops,strtohex((ops[:len(ops)-1])[1:])])

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
        return "byte["+processoprands1(opp[5:len(opp)-1])+"]"
    if(issymbol(opp)):
        k=searchsymbol(opp)
        if(k!=-1):
            return "sym#"+str(k)
        ss=insert_symbol_tbl([opp,None,None,"S","U",None,None,k,None])
        return "sym#"+str(ss)
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
	global symbol_tbl,addr,data,intermediate_code,register,spass
	for k in range(l+1,len(lines)):
            nl=[]
            if((lines[k][0])[len(lines[k][0])-1:]==":"):
                intermediate_code.append(lines[k])
                ss=updatesymbol_tbl((lines[k][0])[:len(lines[k][0])-1],"D",k,k)
                spass.append("sym#"+str(ss))
	    else:
			if(lines[k][0] in ["jmp","jnz","jz","call"]):
				updatesymbol_tbl(lines[k][1],"U",k,k)
                        if(len(lines[k])>1):
                            new=[]
                            new.append(lines[k][0])
                            oprands=lines[k][1].split(',')
                            new1=[]
                            for o in oprands:
                                new1.append(processoprands(o))
                            new.append(joinwith(new1,','))
                            intermediate_code.append(new)
                            spass.append([lines[k][0],new1])
                        else:
                            intermediate_code.append(lines[k])
                            spass.append(lines[k])
	return k
def first_pass(fname):
    global lines
    f=open(fname,"r").readlines()
    lines=[[k.strip() for k in i] for i in [i.split(' ') for i in f]]
    for l in range(len(lines)):
	    if(lines[l][0]=="section"):
                    intermediate_code.append(lines[l])
                    spass.append(lines[l])
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

def checkError():
    for e in symbol_tbl:
        if(e[4]=="U"):
            error_tbl.append(["Line"+str(e[7])+":symbol "+e[0]+" used but not declared"])

first_pass(sys.argv[1])
write_intermediate(sys.argv[1])


#**************2nd pass****************

registeropp=["000","001","010","011","100","101","110","111"]

def shaperatesection(lists):
    lll=[]
    for i in range(len(lists)):
        if(lists[i][0]=="section"):
            start=i
            sec=lists[i][1]
            li=[]
            for i in range(i+1,len(lists)):
                if(lists[i][0]=="section"):
                    break
                else:
                    li.append(lists[i])
            lll.append((sec,li,start))
    return lll
            

def modrm(mod,reg,rm,extra):
    mod+=reg
    if(rm!=None):
        return (hex(int(mod+rm,2)))[2:]
    else:
        return (hex(int(mod+extra,2)))[2:]
def sib(s,i,b):
    i="000"+bin(int(i,16))[2:]
    i=i[len(i)-3:]
    s="00"+bin(int(s,16))[2:]
    s=s[len(s)-2:]
    return hex(int(s+i+b,2))[2:]
lst=[]

def lstdata(data):
    global lst
    lst.append("")
    addr=0
    for i in data:
        lst.append(inttohex(addr)+"  "+literal_tbl[int((i[2])[4:])-1][1] )
        ss=int((i[0])[4:])
        addr+=int(symbol_tbl[ss][1])*int(symbol_tbl[ss][2])

def lstbss(bss):
    global lst
    lst.append("")
    addr=0
    for i in bss:
        ss=int((i[0])[4:]) 
        size=inttohex(int(symbol_tbl[ss][1])*int(symbol_tbl[ss][2]))
        lst.append(inttohex(addr)+"  "+"<res "+size+">")
        addr+=int(size,16)

def getopp(inst,no):
    opps=[("mov",["89","B8","8B"]),("add",["01","05","03"]),("sub",["29","2D","2B"])]
    for i in opps:
        if(inst==i[0]):
            return i[1][no]

def lstmovsubadd(t,lineno,addr):
    if(len(t)<2) or (len(t[1])<2):
        error_tbl.append("Line "+str(lineno)+" operands mismatch ")
        return addr
    op1=t[1][0]
    op2=t[1][1]
    if(op1[0:3]=='reg'):
        if(op2[0:3]=='reg'):
            mr=modrm("11",registeropp[int(op1[4:])],registeropp[int(op2[4:])],None)
            op=getopp(t[0],0)
            lst.append(inttohex(addr)+"   "+op+mr)
            return addr+2
        if(op2[0:3]=="lit"):
            op=getopp(t[0],1)
            literal_tbl[int(op2[4:])-1][1]
            nn=big_endian(literal_tbl[int(op2[4:])-1][1])
            lst.append(inttohex(addr)+"   "+hex(int(op,16)+1)[2:]+nn)
            return addr+len(nn)/2
        if(len(op2)>5):
            if(op2[:5]=="dword"):
                if(op2[6:9]=="sym"):
                    if(t[0]=="mov") and int(op1[4:])==0:
                        ad=big_endian(inttohex(int(symbol_tbl[int(op2[10:11])][5])))
                        lst.append(inttohex(addr)+"   "+"A1"+"["+ ad +"]")
                        return addr+5
                       
                    else:
                        op=getopp(t[0],2)
                        s=big_endian(inttohex(int(symbol_tbl[int(op2[10:11])][5])))
                        mr=modrm("01",registeropp[int(op1[4:])],None,"101")
                        lst.append(inttohex(addr)+"   "+op+mr+"["+s+"]")
                        return addr+3
                    

                else:
                    op=getopp(t[0],2)
                    i=10
                    b=op2[i:i+1]
                    i+=1
                    if(isdigit(op2[i:i+1])):
                        b+=op2[i:i+1]
                        i+=1
                    i+=5
                    s=op2[i:i+1]
                    i+=1
                    if(isdigit(op2[i:i+1])):
                        s+=op2[i:i+1]
                        i+=1
                    i+=5
                    index=op2[i:i+1]
                    i+=1
                    if(isdigit(op2[i:i+1])):
                        index+=op2[i:i+1]

                    s=sib(literal_tbl[int(b)][1],literal_tbl[int(index)][1],registeropp[int(b)])
                    mr=modrm("01",registeropp[int(op1[4:])],None,"101")
                    lst.append(inttohex(addr)+"   "+op+mr+s)
                    return addr+3

        else:
            if(op2[:3]=="sym"):
                op=getopp(t[0],2)
                op=hex(int(op,16)+int(op1[4:]))[2:]
            
                lst.append(inttohex(addr)+"   "+op+"["+big_endian(inttohex(int(symbol_tbl[int(op2[4:])][5])))+"]")

                return addr
            lst.append("")
            error_tbl.append("Line "+str(lineno)+" operands mismatch ")
            return addr

    else:
        lst.append("")    
        return addr
            
def lstmuldiv(t,lineno,addr):
    if(len(t)<2)or len(t[1])>2:
        error_tbl.append("Line "+str(lineno)+":operand mismatch")
        return addr
    else:
        if(t[0]=="mul"):
            op="07E"
        else:
            op="07F"
        if((t[1][0])[:3]=="reg"):
            op+=t[1][0][4:]
            lst.append(inttohex(addr)+"   "+op)
            return addr+2
        else:
            lst.append("")
            error_tbl.append("Line "+str(lineno)+":operand mismatch")
            return addr

def lstpushpop(t,lineno,addr):
    if(len(t)<2) or len(t[1])>2:
        error_tbl.append("Line "+str(lineno)+":error: invalid combination of opcode and operands")
        return addr
    else:
        if(t[0]=="pop"):
            if t[1][0][:3]=="reg":
                lst.append(inttohex(addr)+"   "+hex(int("58",16)+int(t[1][0][4:]))[2:])
                return addr+1
            else:
                error_tbl.append("Line "+str(lineno)+":error: invalid combination of opcode and operands")
                return addr
                
        else:
            if t[1][0][:3]=="sym":
                lst.append(inttohex(addr)+"   "+"68"+"["+big_endian(inttohex(int(symbol_tbl[int(t[1][0][4:])][5])))+"]")
                return addr+5
             
            if t[1][0][:3]=="lit":
                lst.append(inttohex(addr)+"   "+"6A"+"["+big_endian(inttohex(int(literal_tbl[int(t[1][0][4:])][1],16)))+"]")
                return addr +5
        
            if t[1][0][:3]=="reg":
                lst.append(inttohex(addr)+"   "+hex(int("50",16)+int(t[1][0][4:]))[2:])
                return addr +5

                
            error_tbl.append("Line "+str(lineno)+":error: invalid combination of opcode and operands")
            lst.append("")
            return addr



            

def lsttext(text,lineno):
    global lst
    addr=0
    lst.append("")
    lineno+=1
    for t in text:
        if t[0] in ["mov","sub","add"]:
            addr=lstmovsubadd(t,lineno,addr)
        else:
            if t[0] in ["mul","div"]:
                addr=lstmuldiv(t,lineno,addr)
            else:
                if t[0] in ["push","pop"]:
                    addr=lstpushpop(t,lineno,addr)
                else:
                    lst.append("")


        

def secondpass():
    global spass
    spass=shaperatesection(spass)

    for j in spass:
        if(j[0]==".data"):
            lstdata(j[1])
        if(j[0]==".bss"):
            lstbss(j[1])
        if(j[0]==".text"):
            lsttext(j[1],j[2])

def combineopcodeasm():
    new=[]
    lines=open(sys.argv[1],"r").readlines()
    for i in range(len(lines)):
        new.append([i+1,lst[i],lines[i]])
    return new

secondpass()
f=open((sys.argv[1])[:len(sys.argv[1])-4]+".lst","w")
print(tabulate(symbol_tbl))
new=combineopcodeasm()
f.write(tabulate(new))
