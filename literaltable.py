#!/usr/bin/env python3
from sys import argv
from symboltable import *
import sys
import os

lit_val=[]
reg_sym=['eax','ebx','ecx','edx','edi','esi','esp','ebp','al','bl','cl','dl','ax','bx','cx','dx','sp','bp']
inst_sym=['mov','add']
cnt=1
symbol=[]

if not os.path.exists("SymbolTable.txt"):
    open("SymbolTable.txt","w").close()

fp=open("SymbolTable.txt","r")
line=fp.read()
list_sym=line.split()


def find_hex(val):
    list1=list(val)
    if ord(list1[0]) in range(48,58):
        val1=hex(int(val))
        return '{0:0>2}'.format(val1[2:].upper())

def find_sym(val1):
    val2=val1.replace("'","")
    return val2

def find_shex(val1):
    val=[]
    for i in range(len(val1)):
        val2=ord(val1[i])
        val3=hex(val2)[2:]
        val.append(val3)
    val4=''.join(val)
    return val4.upper()

def find_lit(list1,n):
    lit_no=[]
    line_no=[]
    lit_sym=[]
    lit_hex=[]
    lit_typ=[]
    global cnt

    for i in range(len(list1)):
        if list1[i] in inst_sym:
            val1=list1[i+1]
            val2=val1.split(',')
            if val2[0] in reg_sym:
                if val2[1] not in reg_sym:
                    val3=ord(list(list(val2)[1])[0])
                    if val3 in range(48,58):
                        lit_no.append(cnt)
                        cnt+=1
                        line_no.append(n)
                        lit_sym.append(val2[1])
                        temp=find_hex(val2[1])
                        lit_hex.append(temp)
                        lit_typ.append('reg,img')
                        lit_val.append(lit_no+line_no+lit_sym+lit_hex+lit_typ)

                    if val3 not in range(48,58) and '[' not in val2[1]:
                        lit_no.append(cnt)
                        cnt+=1
                        line_no.append(n)
                        val=find_sym(val2[1])
                        lit_sym.append(val)
                        temp=find_shex(val)
                        lit_hex.append(temp)
                        lit_typ.append('reg,img')
                        lit_val.append(lit_no+line_no+lit_sym+lit_hex+lit_typ)


            if val2[0] in list_sym or val2[0] not in reg_sym:
                if val2[0] not in list_sym:
                    val3=ord(list(list(val2)[1])[0])
                    if val3 in range(48,58):
                        lit_no.append(cnt)
                        cnt+=1
                        line_no.append(n)
                        lit_sym.append(val2[1])
                        temp=find_hex(val2[1])
                        lit_hex.append(temp)
                        lit_typ.append('mem,img')
                        lit_val.append(lit_no+line_no+lit_sym+lit_hex+lit_typ)



def lit_table(f_name):
    fo=open(f_name,"r")
    cnt=1

    line1=fo.readline()
    while (line1 !=""):
        line2=line1.split()
        find_lit(line2,cnt)
        cnt+=1
        line1=fo.readline()

    for k in range(len(sym_val)):
        symbol.append(sym_val[k][1])




def lit_disp():
    ln=len(lit_val)
    if (lit_val==[]):
        print('\t'"Literal NOT Available")
    else:
        print('\n'"       Line No" '\t' "     Literal NO" '\t' "     Literal Symbol" '\t' "literal Hex" '\t' "Type" '\n')
        for i in range(ln):
            print('\t',lit_val[i][1] ,'\t''\t',  lit_val[i][0],'\t''\t',lit_val[i][2],'\t''\t',lit_val[i][3],'\t''\t',lit_val[i][4])
        print('\n')

def lit_write():
    fo=open(".literal_table.txt","w+")
    for i in range(len(lit_val)):
        fo.write(str(lit_val[i][0])+'\t'+str(lit_val[i][2])+'\t'+str(lit_val[i][3])+'\t'+str(lit_val[i][4])+'\n')

if __name__ == '__main__':
    script,filename=argv
    sym_table(filename)
    write_file()

    lit_table(filename)
    lit_disp()
    lit_write()

