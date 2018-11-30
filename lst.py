#!/usr/bin/env python3
from literaltable import *
from sys import argv
import sys
import os

addr1=0
addr2=0
addr3=0

op_val=[]

cnt=1
lno=1
bara =['eax','ebx','ecx','edx','esp','ebp','esi','edi']
reg_eax=['eax','ax','al']
reg_ebx=['ebx','bx','bl']
reg_ecx=['ecx','cx','cl']
reg_edx=['edx','dx','dl']
reg_esp=['esp','sp','ah']
reg_ebp=['ebp','bp','bh']
reg_esi=['esi','si','cl']
reg_edi=['edi','di','dl']

data_sym=['.data','db','dw','dd','dq','dt','equ']
bss_sym=['.bss','resb','resw','resd','resq','rest']
txt_sym=['.text','main:','global','extern']
ins_sym=['mov']
reg_sym32=['0','eax','1','ebx','2','ecx','3','edx','4','esp','5','ebp','6','esi','7','edi']

if not os.path.exists(".symbol_table.txt"):
    open(".symbol_table.txt","w").close()

if not os.path.exists(".literal_table.txt"):
    open(".literal_table.txt","w").close()

fp2=open(".symbol_table.txt","r")
fp4=open(".literal_table.txt","r")
line2=(fp2.read().split())
line4=(fp4.read()).split()


def conv_str_hex(val1):
    print(val1)
    s=""
    for i in val1:
        for x in i:
            s+=hex(ord(x))
    return s

def conv_int_hex(val1,x):
    val=[]
    val2=val1.split(',')

    for i in range(len(val2)):
        val3=int(val2[i])
        val4=((hex(val3))[2:])
        val5='{:0>2}'.format(val4)
        val6='{:0<{}}'.format(val5,x)
        val7=val6.upper()
        val.append(val7)

    val8=','.join(val)
    val9=val8.replace(",","")
    return val9

def append_str(line1,val1,ln,sta,end,lnn):
    line_no=[]
    address=[]
    opcode=[]
    orignal=[]
    sym=[]
    global addr1
    global lno
    list1=line1.split()
    temp=list1[0]


    if ln>=18 and ln!=0:
        line_no.append('{0:02}'.format(lno))
        lno+=1
        hadd='{0:0>8}'.format(hex(addr1)[2:])
        address.append(hadd.upper())
        addr1+=9
        opcode.append((val1[sta:end]).upper()+'-')
        sta+=18
        end+=18
        if len(val1)==ln:
            orignal.append(line1.rstrip())
        else:
            orignal.append('')
        sym.append(temp)
        op_val.append(line_no+address+opcode+orignal+sym)
        ln-=18
        return append_str(line1,val1,ln,sta,end,lnn)

    if ln<18 and ln!=0:
        line_no.append('{0:02}'.format(lno))
        lno+=1
        hadd='{0:0>8}'.format(hex(addr1)[2:])
        address.append(hadd.upper())
        addr1+=int(ln/2)
        if(len(val1[sta:end])) <=10:
            opcode.append((val1[sta:end]).upper()+'       ')
        else:
            opcode.append((val1[sta:end]).upper())
        sta+=19
        end+=18
        if ln==lnn:
            orignal.append(line1.rstrip())
        else:
            orignal.append('')
        sym.append(temp)
        op_val.append(line_no+address+opcode+orignal+sym)
        ln=0
        return addr1

    else:
        return addr1

def append_section(line1,addr):
    line_no=[]
    address=[]
    opcode=[]
    orignal=[]
    sym=[]
    global lno

    line_no.append('{0:02}'.format(lno))
    lno+=1
    address.append('        ')
    opcode.append('                  ')
    ol=line1.rstrip()
    orignal.append(ol)
    sym.append('no')
    op_val.append(line_no+address+opcode+orignal+sym)
    return addr


def find_data_sec(line1,list1):
    line_no=[]
    address=[]
    opcode=[]
    orignal=[]
    sym=[]
    global addr1
    global lno
    global sta
    global end


    for i in range(len(list1)):
        if list1[i]=='section' or list1[i]=='equ':                      #find opcode section .data and equ
            addr=append_section(line1,addr1)
            return addr1

        if list1[i]=='db':                                              #find opcode db
            val1=[]
            for j in range(i+1,len(list1)):
                if(list1[j]!='0'):
                    val1.append(list1[j])
            val2=conv_str_hex(val1)                                     #convet string to hex
            sta=0
            end=18
            addt=append_str(line1,val2,len(val2),sta,end,len(val2))     #find opcode and append db
            return addr1


        if list1[i] in data_sym[2:-1]:
            if list1[i]=='dd':
                val2=conv_int_hex(list1[i+1],8)                          #convert int to hex
                sta=0
                end=18
                addt=append_str(line1,val2,len(val2),sta,end,len(val2))  #find and append dd
                return addr1
            return addr1


def find_bss_sec(line1,list1):
    line_no=[]
    address=[]
    opcode=[]
    orignal=[]
    sym=[]
    global addr2
    global lno

    for i in range(len(list1)):
        if list1[i]=='section':                      #find opcode section .data and equ
            addr=append_section(line1,addr1)
            return addr2

        if list1[i] in bss_sym[1:]:
            if list1[i]=='resd':
                addr=append_res(line1,list1,4)
                return addr2
            return addr2


def check_sym(val2,n):
    val3=list(val2)
    val4=val3[n:-1]
    val5=','.join(val4)
    val6=val5.replace(",","")
    return val6
def check_reg(val1,val2):
    p=192
    for i in bara:
        if(i==val2):
            for x in range(len(bara)):
                if bara[x]==val1:
                    p=hex(p+x).split('x')
                    return p[1].upper()
        p+=8
def find_sym_add(sym,x):
    val9=0
    for i in range(len(op_val)):
        if sym in op_val[i][4]:
            addr=(op_val[i][1])
            val1=list(addr)
            val2=val1[-2:]
            val3=','.join(val2)
            val4=val3.replace(",","")
            val5=int(val4,16)
            val6=hex(val5)[2:]
            val7='{:0>2}'.format(val6)
            val8='{:0<{}}'.format(val7,x)
            val9='['+str(val8.upper())+']'
            break
    return val9

def find_lit_add(lit,x):
    val1=int(lit)
    val6=hex(val1)[2:]
    val7='{:0>2}'.format(val6)
    val8='{:0<{}}'.format(val7,x)
    val9=str(val8.upper())
    return val9

def find_sym_opcode(reg):
    if reg in reg_eax:
        return "05"
    if reg in reg_ebx:
        return "0D"
    if reg in reg_ecx:
        return "15"
    if reg in reg_edx:
        return "1D"
    if reg in reg_esp:
        return "25"
    if reg in reg_ebp:
        return "2D"
    if reg in reg_esi:
        return "35"
    if reg in reg_edi:
        return "3D"


def find_mov_opcode(list1):
    temp1=list1[1]
    temp2=temp1.split(",")
    val1=temp2[0]
    val2=temp2[1]

    if val1 in reg_sym32 and val2 in reg_sym32:                      # mov reg32 reg32
        mod=check_reg(val1,val2)
        return "89"+mod+"             "

                                                                      # mov reg** *****[mem]opcod and mod r/m
    if val1 in reg_sym32 and len(val2)>=6:                            # mov reg32 dword[mem]
        val6=check_sym(val2,6)
        if val6 in line2:
            if val1=="eax":
                addr=find_sym_add(val6,8)
                return "A1"+addr+"      "
            else:
                addr1=find_sym_opcode(val1)
                addr2=find_sym_add(val6,8)
                return "8B"+addr1+addr2+"    "
    if val1 in reg_sym32 and (val2 in line4 or val2 in line2):         # mov reg32 img | mem
        for i in range(len(reg_sym32)):
            if val1==str(reg_sym32[i]):
                val=8+int(reg_sym32[i-1])
        if val2 not in line4:
            addr=find_sym_add(val2,8)
            return "B"+str(val)+str(addr)+"    "
        v1=int(val2)
        val1='{0:0<8}'.format(hex(v1)[2:]).upper()
        return "B"+hex(val)[2:].upper()+val1+"       "
                                                                      # mov *****[mem] reg** opcod and mod r/m
    if val2 in reg_sym32 and len(val1)>=6:                            # mov dword[mem] reg32
        val6=check_sym(val1,6)
        if val6 in line2:
            if val2=="eax":
                addr=find_sym_add(val6,8)
                return "A3"+addr+"    "
            else:
                addr1=find_sym_opcode(val2)
                addr2=find_sym_add(val6,8)
                return "89"+addr1+addr2+"   "
    if val2 in line4 and len(val1)>=6:                               # mov dword[mem] img32
        val6=check_sym(val1,6)
        if val6 in line2:
            addr1=find_sym_add(val6,8)
            addr2=find_lit_add(val2,8)
            val="C705"+addr1+addr2
            return val
    if val2 in line4 and len(val1)>=6:                               # mov word[mem] img16
        val6=check_sym(val1,5)
        val5=list(val1)
        val4=val5[0]
        if val6 in line2 and val4=='w':
            addr1=find_sym_add(val6,8)
            addr2=find_lit_add(val2,4)
            val="66C705"+addr1+addr2
            return val
    if val2 in line4 and len(val1)>=6:                               # mov byte[mem] reg08
        val6=check_sym(val1,5)
        val5=list(val1)
        val4=val5[0]
        if val6 in line2 and val4=='b':
            addr1=find_sym_add(val6,8)
            addr2=find_lit_add(val2,2)
            val="C605"+addr1+addr2
            return val

def find_len_op(val):
    val1=str(val)
    val2=val1.replace(" ","")
    val3=val2.replace("[","")
    val4=val3.replace("]","")
    val5=int(len(val4)/2)
    return val5

def append_mov(line1,list1):
    line_no=[]
    address=[]
    opcode=[]
    orignal=[]
    sym=[]
    global addr3
    global lno

    line_no.append('{0:02}'.format(lno))
    lno+=1
    hadd='{0:0>8}'.format(hex(addr3)[2:])
    address.append(hadd.upper())
    opcod=find_mov_opcode(list1)
    val=find_len_op(opcod)
    addr3+=val
    opcode.append(opcod)
    ol=line1.rstrip()
    orignal.append(ol)
    sym.append('no')
    op_val.append(line_no+address+opcode+orignal+sym)
    return addr3

def find_sym_add_opcode(reg):
    if reg in reg_eax:
        return "C0"
    if reg in reg_ebx:
        return "C1"
    if reg in reg_ecx:
        return "C2"
    if reg in reg_edx:
        return "C3"
    if reg in reg_esp:
        return "C4"
    if reg in reg_ebp:
        return "C5"
    if reg in reg_esi:
        return "C6"
    if reg in reg_edi:
        return "C7"



def find_add_opcode(list1):
    temp1=list1[1]
    temp2=temp1.split(",")
    val1=temp2[0]
    val2=temp2[1]


                                                                     # add reg** reg** opcod and mod r/m
    if val1 in reg_sym32 and val2 in reg_sym32:                      # add reg32 reg32
        mod=check_reg(val1,val2)
        return "01"+mod+"             "

                                                                      # add reg** *****[mem]opcod and mod r/m
    if val1 in reg_sym32 and len(val2)>=6:                            # add reg32 dword[mem]
        val6=check_sym(val2,6)
        if val6 in line2:
            if val1=="eax":
                addr=find_sym_add(val6,8)
                return "05"+addr+"      "
            else:
                addr1=find_sym_opcode(val1)
                addr2=find_sym_add(val6,8)
                return "03"+addr1+addr2+"    "
                                                                       # add reg** img | mem opcod and mod r/m

    if val1 in reg_sym32 and (val2 in line4 or val2 in line2):         # add reg32 img | mem
        val11=find_sym_add_opcode(val1)
        v1=int(val2)
        val12='{0:0<8}'.format(hex(v1)[2:]).upper()
        return "83"+val11+val12+"   "


                                                                      # add *****[mem] reg** opcod and mod r/m
    if val2 in reg_sym32 and len(val1)>=6:                            # add dword[mem] reg32
        val6=check_sym(val1,6)
        if val6 in line2:
            addr1=find_sym_opcode(val2)
            addr2=find_sym_add(val6,8)
            return "01"+addr1+addr2+"   "
    if val2 in reg_sym16 and len(val1)>=6:                            # add word[mem] reg16
        val6=check_sym(val1,5)
        if val6 in line2:
            addr1=find_sym_opcode(val2)
            addr2=find_sym_add(val6,8)
            return "6601"+addr1+addr2+"   "
                                                                     # add *****[mem] img** opcod and mod r/m
    if val2 in line4 and len(val1)>=6:                               # add dword[mem] img32
        val6=check_sym(val1,6)
        if val6 in line2:
            addr1=find_sym_add(val6,8)
            addr2=find_lit_add(val2,8)
            val="8305"+addr1+addr2
            return val
    if val2 in line4 and len(val1)>=6:                               # add word[mem] img16
        val6=check_sym(val1,5)
        val5=list(val1)
        val4=val5[0]
        if val6 in line2 and val4=='w':
            addr1=find_sym_add(val6,8)
            addr2=find_lit_add(val2,4)
            val="668305"+addr1+addr2
            return val
    if val2 in line4 and len(val1)>=6:                               # add byte[mem] reg08
        val6=check_sym(val1,5)
        val5=list(val1)
        val4=val5[0]
        if val6 in line2 and val4=='b':
            addr1=find_sym_add(val6,8)
            addr2=find_lit_add(val2,2)
            val="8005"+addr1+addr2
            return val


def append_add(line1,list1):
    line_no=[]
    address=[]
    opcode=[]
    orignal=[]
    sym=[]
    global addr3
    global lno

    line_no.append('{0:02}'.format(lno))
    lno+=1
    hadd='{0:0>8}'.format(hex(addr3)[2:])
    address.append(hadd.upper())
    opcod=find_add_opcode(list1)
    val=find_len_op(opcod)
    addr3+=val
    opcode.append(opcod)
    ol=line1.rstrip()
    orignal.append(ol)
    sym.append('no')
    op_val.append(line_no+address+opcode+orignal+sym)
    return addr3

def find_text_sec(line1,list1):
    line_no=[]
    address=[]
    opcode=[]
    orignal=[]
    sym=[]
    global addr3
    global lno
    temp1=list1[0]

    for i in range(len(list1)):
        if list1[i] in txt_sym:                      #find opcode section .data and equ
            addr=append_section(line1,addr1)
            return addr3
    if temp1=='mov':
        append_mov(line1,list1)
        return addr3
    if temp1=='add':
        append_add(line1,list1)
        return addr3

    return addr3


def find_opcode(line1,list1,lno):
    line_no=[]
    address=[]
    opcode=[]
    orignal=[]
    sym=[]
    global addr1
    global addr2
    global addr3
    global cnt

    if list1==[]:
        line_no.append('{0:02}'.format(lno))
        lno+=1
        address.append('        ')
        opcode.append('                  ')
        orignal.append('')
        sym.append('no')
        op_val.append(line_no+address+opcode+orignal+sym)
        cnt+=1
        return 0

    else:
        for i in range(len(list1)):                     #check .data section
            if list1[i] in data_sym:
                val1=find_data_sec(line1,list1)         #call data_sec function
                cnt+=1
                addr1=val1

            if list1[i] in bss_sym:                     #check .bss section
                val2=find_bss_sec(line1,list1)
                cnt+=1
                addr2=val2

        for i in range(len(list1)):
            if lno>=cnt:                                #check .text section
                val3=find_text_sec(line1,list1)
                cnt+=1
                addr3=val3
                break



def lst_table(fname):
    l_no=1
    fp1=open(fname,"r")
    line1=fp1.readline()
    while(line1!=""):
        list1=line1.split()
        find_opcode(line1,list1,l_no)   #call find opcode function-find the all opcode
        l_no+=1
        line1=fp1.readline()

def lst_disp():
    ln=len(op_val)
    # print('\n'"    Line No" '\t' "Address" '\t' "Inst Symbol"  '\t' '\t' "Original " '\n')
    for i in range(ln):
        print('',op_val[i][0] ,'',op_val[i][1],' ' ,op_val[i][2],'\t',op_val[i][3])
    print('\n')


def lst_write(filename):
    fo=open(filename,"w+")
    for i in range(len(op_val)):
        fo.write(''+str(op_val[i][0]) +'  '+str(op_val[i][1])+' ' +str(op_val[i][2])+'\t'+str(op_val[i][3])+'\n')


if __name__ == '__main__':

    script,filename=argv
    sym_table(filename)
    write_file()


    lit_table(filename)
    lit_write()

    lst_table(filename)    #call main opcode function
    lst_disp()                #call lst display function
    #lst_write("sp.lst")

