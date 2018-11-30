#!/usr/bin/env python3
from symboltable import *
from literaltable import *
from sys import argv
import sys

addr1=234971409
add1=addr1
addr2=218169667
add2=addr2
addr3=168231828
add3=addr3

op_val=[]
op_dat=[]
op_bss=[]
op_txt=[]

cnt=1
lno=1

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

reg_sym08=['0','al','1','bl','2','cl','3','dl','4','ah','5','bh','6','ch','7','dh']
reg_sym16=['0','ax','1','bx','2','cx','3','dx','4','sp','5','bp','6','si','7','di']
reg_sym32=['0','eax','1','ebx','2','ecx','3','edx','4','esp','5','ebp','6','esi','7','edi']

if not os.path.exists("SymbolTable.txt"):
    open("SymbolTable.txt","w").close()

if not os.path.exists(".literal_table.txt"):
    open(".literal_table.txt","w").close()

fp2=open("SymbolTable.txt","r")
fp4=open(".literal_table.txt","r")
line2=(fp2.read().split())
line4=(fp4.read()).split()


def conv_str_hex(val1):
    val=[]
    val4=[]
    val2=','.join(val1)
    val3=val2.split(',')

    for i in range(len(val3)):
        if(val3[i]=='0'):
            for j in range(i):
                val4.append(val3[j])

    val5=','.join(val4)
    val6=val5.replace(","," ")
    val7=val6.replace('"','')

    for k in range(len(val7)):
       val8= hex(ord(val7[k]))
       val9=val8[2:4]
       val.append(val9)

    val.append('00'+'0a')
    val10=','.join(val)
    val11=val10.replace(',','')
    return val11

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
        op_dat.append(line_no+address+opcode+orignal+sym)
        ln-=18
        return append_str(line1,val1,ln,sta,end,lnn)

    if ln<18 and ln!=0:
        line_no.append('{0:02}'.format(lno))
        lno+=1
        hadd='{0:0>8}'.format(hex(addr1)[2:])
        address.append(hadd.upper())
        addr1+=int(ln/2)
        if(len(val1[sta:end])) <=10:
            opcode.append((val1[sta:end]).upper()+'           ')
        else:
            opcode.append((val1[sta:end]).upper()+'      ')
        sta+=19
        end+=18
        if ln==lnn:
            orignal.append(line1.rstrip())
        else:
            orignal.append('')
        sym.append(temp)
        op_val.append(line_no+address+opcode+orignal+sym)
        op_dat.append(line_no+address+opcode+orignal+sym)
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

            if list1[i]=='dw':
                val2=conv_int_hex(list1[i+1],4)                         #convert int to hex
                sta=0
                end=18
                addt=append_str(line1,val2,len(val2),sta,end,len(val2)) #find and append dw
                return addr1

            if list1[i]=='dq':
                val2=conv_int_hex(list1[i+1],16)                        #convert int to hex
                sta=0
                end=18
                addt=append_str(line1,val2,len(val2),sta,end,len(val2)) # find and append dq
                return addr1

            return addr1


def append_res(line1,list1,n):
    line_no=[]
    address=[]
    opcode=[]
    orignal=[]
    sym=[]
    val1=list1[0]
    val2=list1[1]
    val3=list1[2]
    val=int(val3)*n
    valh=hex(val)[2:]
    global addr2
    global lno
    temp=list1[0]


    line_no.append('{0:02}'.format(lno))
    lno+=1
    hadd='{0:0>8}'.format(hex(addr2)[2:])
    address.append(hadd.upper())
    addr2+=val
    opcode.append("<res"+ " "+'{0:0>8}'.format(valh).upper()+">"+"      ")
    ol=line1.rstrip()
    orignal.append(ol)
    sym.append(temp)
    op_val.append(line_no+address+opcode+orignal+sym)
    op_bss.append(line_no+address+opcode+orignal+sym)
    return addr2


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
            if list1[i]=='resb':
                addr=append_res(line1,list1,1)
                return addr2
            if list1[i]=='resw':
                addr=append_res(line1,list1,2)
                return addr2
            if list1[i]=='resd':
                addr=append_res(line1,list1,4)
                return addr2
            if list1[i]=='resq':
                addr=append_res(line1,list1,8)
                return addr2
            if list1[i]=='rest':
                addr=append_res(line1,list1,10)
                return addr2

            return addr2


def check_sym(val2,n):
    val3=list(val2)
    val4=val3[n:-1]
    val5=','.join(val4)
    val6=val5.replace(",","")
    return val6

def check_reg(val1,val2):                             # mov reg32 reg32 mod R/M
    if val1 in reg_eax and val2 in reg_eax:
        return "C0"
    if val1 in reg_ebx and val2 in reg_eax:
        return "C1"
    if val1 in reg_ecx and val2 in reg_eax:
        return "C2"
    if val1 in reg_edx and val2 in reg_eax:
        return "C3"
    if val1 in reg_esp and val2 in reg_eax:
        return "C4"
    if val1 in reg_ebp and val2 in reg_eax:
        return "C5"
    if val1 in reg_esi and val2 in reg_eax:
        return "C6"
    if val1 in reg_edi and val2 in reg_eax:
        return "C7"
                                                     # mov reg32 ebx/bx/bl mod R/M
    if val1 in reg_eax and val2 in reg_ebx:
        return "C8"
    if val1 in reg_ebx and val2 in reg_ebx:
        return "C9"
    if val1 in reg_ecx and val2 in reg_ebx:
        return "CA"
    if val1 in reg_edx and val2 in reg_ebx:
        return "CB"
    if val1 in reg_esp and val2 in reg_ebx:
        return "CC"
    if val1 in reg_ebp and val2 in reg_ebx:
        return "CD"
    if val1 in reg_esi and val2 in reg_ebx:
        return "CE"
    if val1 in reg_edi and val2 in reg_ebx:
        return "CF"
                                                      # mov reg32 ecx/cx/cl mod R/M
    if val1 in reg_eax and val2 in reg_ecx:
        return "D0"
    if val1 in reg_ebx and val2 in reg_ecx:
        return "D1"
    if val1 in reg_ecx and val2 in reg_ecx:
        return "D2"
    if val1 in reg_edx and val2 in reg_ecx:
        return "D3"
    if val1 in reg_esp and val2 in reg_ecx:
        return "D4"
    if val1 in reg_ebp and val2 in reg_ecx:
        return "D5"
    if val1 in reg_esi and val2 in reg_ecx:
        return "D6"
    if val1 in reg_edi and val2 in reg_ecx:
        return "D7"
                                                       # mov reg32 edx/dx/dl mod R/M
    if val1 in reg_eax and val2 in reg_edx:
        return "D8"
    if val1 in reg_ebx and val2 in reg_edx:
        return "D9"
    if val1 in reg_ecx and val2 in reg_edx:
        return "DA"
    if val1 in reg_edx and val2 in reg_edx:
        return "DB"
    if val1 in reg_esp and val2 in reg_edx:
        return "DC"
    if val1 in reg_ebp and val2 in reg_edx:
        return "DD"
    if val1 in reg_esi and val2 in reg_edx:
        return "DE"
    if val1 in reg_edi and val2 in reg_edx:
        return "DF"
                                                       # mov reg32 esp/sp/ah mod R/M
    if val1 in reg_eax and val2 in reg_esp:
        return "E0"
    if val1 in reg_ebx and val2 in reg_esp:
        return "E1"
    if val1 in reg_ecx and val2 in reg_esp:
        return "E2"
    if val1 in reg_edx and val2 in reg_esp:
        return "E3"
    if val1 in reg_esp and val2 in reg_esp:
        return "E4"
    if val1 in reg_ebp and val2 in reg_esp:
        return "E5"
    if val1 in reg_esi and val2 in reg_esp:
        return "E6"
    if val1 in reg_edi and val2 in reg_esp:
        return "E7"
                                                       # mov reg32 ebp/bp/bl mod R/M
    if val1 in reg_eax and val2 in reg_ebp:
        return "E8"
    if val1 in reg_ebx and val2 in reg_ebp:
        return "E9"
    if val1 in reg_ecx and val2 in reg_ebp:
        return "EA"
    if val1 in reg_edx and val2 in reg_ebp:
        return "EB"
    if val1 in reg_esp and val2 in reg_ebp:
        return "EC"
    if val1 in reg_ebp and val2 in reg_ebp:
        return "ED"
    if val1 in reg_esi and val2 in reg_ebp:
        return "EE"
    if val1 in reg_edi and val2 in reg_ebp:
        return "EF"
                                                       # mov reg32 esi/si/ch mod R/M
    if val1 in reg_eax and val2 in reg_esi:
        return "F0"
    if val1 in reg_ebx and val2 in reg_esi:
        return "F1"
    if val1 in reg_ecx and val2 in reg_esi:
        return "F2"
    if val1 in reg_edx and val2 in reg_esi:
        return "F3"
    if val1 in reg_esp and val2 in reg_esi:
        return "F4"
    if val1 in reg_ebp and val2 in reg_esi:
        return "F5"
    if val1 in reg_esi and val2 in reg_esi:
        return "F6"
    if val1 in reg_edi and val2 in reg_esi:
        return "F7"
                                                       # mov reg32 edi/di/dh mod R/M
    if val1 in reg_eax and val2 in reg_edi:
        return "F8"
    if val1 in reg_ebx and val2 in reg_edi:
        return "F9"
    if val1 in reg_ecx and val2 in reg_edi:
        return "FA"
    if val1 in rFB_edx and val2 in reg_edi:
        return "FB"
    if val1 in reg_esp and val2 in reg_edi:
        return "FC"
    if val1 in reg_ebp and val2 in reg_edi:
        return "FD"
    if val1 in reg_esi and val2 in reg_edi:
        return "FE"
    if val1 in reg_edi and val2 in reg_edi:
        return "FF"

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

def find_sym_add1(sym,x):
    val9=0

    for i in range(len(op_val)):
        if sym in op_val[i][4]:
            addr=(op_val[i][1])
            val9='['+str(addr.upper())+']'
            break
    return val9

def find_mov_opcode(list1):
    temp1=list1[1]
    temp2=temp1.split(",")
    val1=temp2[0]
    val2=temp2[1]

                                                                     # mov reg** reg** opcod and mod r/m
    if val1 in reg_sym08 and val2 in reg_sym08:                      # mov reg08 reg08
        mod=check_reg(val1,val2)
        return "88"+mod+"             "
    if val1 in reg_sym16 and val2 in reg_sym16:                      # mov reg16 reg16
        mod=check_reg(val1,val2)
        return "6689"+mod+"           "
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
                addr2=find_sym_add1(val6,8)
                return "8B"+addr1+addr2+"    "
    if val1 in reg_sym16 and len(val2)>=6:                            # mov reg16 word[mem]
        val6=check_sym(val2,5)
        val5=list(val2)
        val4=val5[0]
        if val6 in line2 and val4=='w':
            if val1=="ax":
                addr=find_sym_add(val6,8)
                return "66A1"+addr+"     "
            else:
                addr1=find_sym_opcode(val1)
                addr2=find_sym_add1(val6,8)
                return "668B"+addr1+addr2+"    "
    if val1 in reg_sym08 and len(val2)>=6:                            # mov reg08 byte[mem]
        val6=check_sym(val2,5)
        val5=list(val2)
        val4=val5[0]
        if val6 in line2 and val4=='b':
            if val1=="al":
                addr=find_sym_add(val6,8)
                return "A0"+addr+"      "
            else:
                addr1=find_sym_opcode(val1)
                addr2=find_sym_add1(val6,8)
                return "8A"+addr1+addr2+"    "
                                                                       # mov reg** img | mem opcod and mod r/m
    if val1 in reg_sym08 and (val2 in line4 or val2 in line2):         # mov reg08 img | mem
        for i in range(len(reg_sym08)):
            if val1==str(reg_sym08[i]):
                val=8+int(reg_sym08[i-1])
        if val2 not in line4:
            addr=find_sym_add(val2,2)
            return "B"+str(val)+addr+"            "
        else:
            v1=int(val2)
            val1='{0:0<2}'.format(hex(v1)[2:]).upper()
            return "B"+hex(val)[2:].upper()+val1+"            "
    if val1 in reg_sym16 and (val2 in line4 or val2 in line2):         # mov reg16 img | mem
        for i in range(len(reg_sym16)):
            if val1==str(reg_sym16[i]):
                val=8+int(reg_sym16[i-1])
        if val2 not in line4:
            addr=find_sym_add(val2,4)
            return "66B"+str(val)+addr+"     "
        v1=int(val2)
        val1='{0:0<4}'.format(hex(v1)[2:]).upper()
        return "B"+hex(val)[2:].upper()+val1+"            "
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
                addr2=find_sym_add1(val6,8)
                return "89"+addr1+addr2+"   "
    if val2 in reg_sym16 and len(val1)>=6:                            # mov word[mem] reg16
        val6=check_sym(val1,5)
        if val6 in line2:
            if val2=="ax":
                addr=find_sym_add(val6,8)
                return "66A3"+addr+"    "
            else:
                addr1=find_sym_opcode(val2)
                addr2=find_sym_add1(val6,8)
                return "6689"+addr1+addr2+"   "
    if val2 in reg_sym08 and len(val1)>=6:                            # mov byte[mem] reg08
        val6=check_sym(val1,5)
        if val6 in line2:
            if val2=="al":
                addr=find_sym_add(val6,8)
                return "A2"+addr+"    "
            else:
                addr1=find_sym_opcode(val2)
                addr2=find_sym_add1(val6,8)
                return "88"+addr1+addr2+"  "
                                                                     # mov *****[mem] img** opcod and mod r/m
    if val2 in line4 and len(val1)>=6:                               # mov dword[mem] img32
        val6=check_sym(val1,6)
        if val6 in line2:
            addr1=find_sym_add1(val6,8)
            addr2=find_lit_add(val2,8)
            val="C705"+addr1+addr2
            return val
    if val2 in line4 and len(val1)>=6:                               # mov word[mem] img16
        val6=check_sym(val1,5)
        val5=list(val1)
        val4=val5[0]
        if val6 in line2 and val4=='w':
            addr1=find_sym_add1(val6,8)
            addr2=find_lit_add(val2,4)
            val="66C705"+addr1+addr2
            return val
    if val2 in line4 and len(val1)>=6:                               # mov byte[mem] reg08
        val6=check_sym(val1,5)
        val5=list(val1)
        val4=val5[0]
        if val6 in line2 and val4=='b':
            addr1=find_sym_add1(val6,8)
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
    op_txt.append(line_no+address+opcode+orignal+sym)
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
    if val1 in reg_sym08 and val2 in reg_sym08:                      # add reg08 reg08
        mod=check_reg(val1,val2)
        return "00"+mod+"             "
    if val1 in reg_sym16 and val2 in reg_sym16:                      # add reg16 reg16
        mod=check_reg(val1,val2)
        return "6601"+mod+"           "
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

    if val1 in reg_sym16 and len(val2)>=6:                            # add reg16 word[mem]
        val6=check_sym(val2,5)
        val5=list(val2)
        val4=val5[0]
        if val6 in line2 and val4=='w':
            if val1=="ax":
                addr=find_sym_add(val6,8)
                return "6605"+addr+"     "
            else:
                addr1=find_sym_opcode(val1)
                addr2=find_sym_add(val6,8)
                return "6603"+addr1+addr2+"    "
    if val1 in reg_sym08 and len(val2)>=6:                            # add reg08 byte[mem]
        val6=check_sym(val2,5)
        val5=list(val2)
        val4=val5[0]
        if val6 in line2 and val4=='b':
            if val1=="al":
                addr=find_sym_add(val6,8)
                return "04"+addr+"      "
            else:
                addr1=find_sym_opcode(val1)
                addr2=find_sym_add(val6,8)
                return "02"+addr1+addr2+"    "

                                                                       # add reg** img | mem opcod and mod r/m
    if val1 in reg_sym08 and (val2 in line4 or val2 in line2):         # add reg08 img | mem
        val11=find_sym_add_opcode(val1)
        v1=int(val2)
        val12='{0:0<2}'.format(hex(v1)[2:]).upper()
        return "80"+val11+val12+"                "

    if val1 in reg_sym16 and (val2 in line4 or val2 in line2):         # add reg16 img | mem
        val11=find_sym_add_opcode(val1)
        v1=int(val2)
        val12='{0:0<4}'.format(hex(v1)[2:]).upper()
        return "6683"+val11+val12+"        "

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
    if val2 in reg_sym08 and len(val1)>=6:                            # add byte[mem] reg08
        val6=check_sym(val1,5)
        if val6 in line2:
            addr1=find_sym_opcode(val2)
            addr2=find_sym_add(val6,8)
            return "00"+addr1+addr2+"  "
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
    op_txt.append(line_no+address+opcode+orignal+sym)
    op_val.append(line_no+address+opcode+orignal+sym)
    return addr3

def append_call(line1,list1):
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
    addr3+=5
    opcode.append("E8"+"(00000000)"+"   ")
    ol=line1.rstrip()
    orignal.append(ol)
    sym.append('no')
    op_txt.append(line_no+address+opcode+orignal+sym)
    op_val.append(line_no+address+opcode+orignal+sym)
    return addr3


def find_push_opcode(list1):
    if len(list1[1])<6:
        val1=list1[1]
        if ord(val1[0]) in range(48,57):
            val2=int(val1)
            val3=hex(val2)[2:]
            val4='{:0>2}'.format(val3)
            val5='{:0<{}}'.format(val4,8).upper()
            return "68"+str(val5)+"     "
        if ord(val1[0]) not in range(48,57):
            if val1 in reg_sym16:
                for i in range(len(reg_sym16)):
                    if reg_sym16[i]==val1:
                        val2=50+int(reg_sym16[i-1])
                        return "66"+str(val2)+"               "
            if val1 in reg_sym32:
                for i in range(len(reg_sym32)):
                    if reg_sym32[i]==val1:
                        val2=50+int(reg_sym32[i-1])
                        return str(val2)+"               "

    if len(list1[1])>6:
        val1=list1[1]
        if val1[0]=='d':
            sym=check_sym(val1,6)
            add=find_sym_add1(sym,8)
            return "FF35"+str(add)+"    "
        if val1[0]=='w':
            sym=check_sym(val1,5)
            add=find_sym_add1(sym,8)
            return "66FF35"+str(add)+"    "

def append_push(line1,list1):
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
    opcod=find_push_opcode(list1)
    val=find_len_op(opcod)
    addr3+=val
    opcode.append(opcod)
    ol=line1.rstrip()
    orignal.append(ol)
    sym.append('no')
    op_val.append(line_no+address+opcode+orignal+sym)
    op_txt.append(line_no+address+opcode+orignal+sym)
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
    if temp1=='call':
        append_call(line1,list1)
        return addr3
    if temp1=='push':
        append_push(line1,list1)
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



def obj_code(fname):
    l_no=1
    fp1=open(fname,"r")
    line1=fp1.readline()
    while(line1!=""):
        list1=line1.split()
        find_opcode(line1,list1,l_no)   #call find opcode function-find the all opcode
        l_no+=1
        line1=fp1.readline()

    val1=fname.split('.')
    val2=val1[0]+'.o'
    obj_write(val2)


def obj_disp():
    val1='{0:0>8}'.format(hex(184748807)[2:]).upper()
    print('\n','%s ' % (val1),"< symbol table > :",'\n')
    if (sym_val==[]):
        print('\t'"Symbol NOT Available")
    else:
        ln1=len(sym_val)
        for i in range(ln1):
            print('\t',sym_val[i][3],'\t',sym_val[i][1],'\t''\t',sym_val[i][2],'\t',sym_val[i][4],'\t',sym_val[i][5],'\t',sym_val[i][6])
        print('\n')

    val2='{0:0>8}'.format(hex(219611911)[2:]).upper()
    print('\n','%s ' %(val2),"< literal table > :",'\n')
    ln2=len(lit_val)
    if (lit_val==[]):
        print('\t'"Literal NOT Available")
    else:
        for i in range(ln2):
            print('\t',lit_val[i][0],'\t',lit_val[i][2],'\t''\t',lit_val[i][3],'\t',lit_val[i][4])
        print('\n')

    val3='{0:0>8}'.format(hex(add1)[2:]).upper()
    print('\n','%s ' % (val3),"< section .data > :",'\n')
    ln3=len(op_dat)
    for i in range(ln3):
        print('\t',op_dat[i][1],' ' ,op_dat[i][2],'\t',op_dat[i][3])
    print('\n')

    val4='{0:0>8}'.format(hex(add2)[2:]).upper()
    print('\n','%s ' % (val4),"< section .bss > :",'\n')
    ln4=len(op_bss)
    for i in range(ln4):
        print('\t',op_bss[i][1],' ' ,op_bss[i][2],'\t',op_bss[i][3])
    print('\n')

    val5='{0:0>8}'.format(hex(add3)[2:]).upper()
    print('\n','%s ' % (val5),"< _start > :",'\n')
    ln3=len(op_txt)
    for i in range(ln3):
        print('\t',op_txt[i][1],'    ' ,op_txt[i][2])
    print('\n')

def obj_write(fname):
    fo=open(fname,"w+")

    val1='{0:0>8}'.format(hex(184748807)[2:]).upper()
    fo.write('\n'+'%s ' % (val1)+"< symbol table > :"+'\n\n')
    if (sym_val==[]):
        fo.write('\t'"Symbol NOT Available")
    else:
        ln1=len(sym_val)
        for i in range(ln1):
            fo.write('\t'+str(sym_val[i][3])+'\t'+str(sym_val[i][1])+'\t''\t'+str(sym_val[i][2])+'\t'+str(sym_val[i][4])+'\t'+str(sym_val[i][5])+'\t'+str(sym_val[i][6])+'\n')

    val2='{0:0>8}'.format(hex(219611911)[2:]).upper()
    fo.write('\n'+'%s ' %(val2)+"< literal table > :"+'\n\n')
    ln2=len(lit_val)
    if (lit_val==[]):
        fo.write('\t'"Literal NOT Available")
    else:
        for i in range(ln2):
            fo.write('\t'+str(lit_val[i][0])+'\t'+str(lit_val[i][2])+'\t''\t'+str(lit_val[i][3])+'\t'+str(lit_val[i][4])+'\n')

    val3='{0:0>8}'.format(hex(add1)[2:]).upper()
    fo.write('\n'+'%s ' % (val3)+"< section .data > :"+'\n\n')
    ln3=len(op_dat)
    for i in range(ln3):
        fo.write('\t'+str(op_dat[i][1])+' ' +str(op_dat[i][2])+'\t'+str(op_dat[i][3])+'\n')

    val4='{0:0>8}'.format(hex(add2)[2:]).upper()
    fo.write('\n'+'%s ' % (val4)+"< section .bss > :"+'\n\n')
    ln4=len(op_bss)
    for i in range(ln4):
        fo.write('\t'+str(op_bss[i][1])+' ' +str(op_bss[i][2])+'\t'+str(op_bss[i][3])+'\n')

    val5='{0:0>8}'.format(hex(add3)[2:]).upper()
    fo.write('\n'+'%s ' % (val5)+"< _start > :"+'\n\n')
    ln3=len(op_txt)
    for i in range(ln3):
        fo.write('\t'+str(op_txt[i][1])+'    ' +str(op_txt[i][2])+'\n')



if __name__ == '__main__':

    script,filename=argv
    sym_table(filename)
    write_file()

    lit_table(filename)
    lit_write()

    obj_code(filename)
    obj_disp()                #call obj display function

