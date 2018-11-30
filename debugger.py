#!/usr/bin/env python3
from symboltable import *
from literaltable import *
from finalLst import *
from finalObj import *
from smaco import *
from sys import argv
import sys
ko = ['n','q','quit','list','help','h','info reg','run','display $eax','display $ebx','display $ecx',      'display $edx','display $esp','display $ebp','display $esi','display $edi','print/d $eax','print/d $ebx','print/d $ecx',   'print/d $edx','print/d $esp','print/d $ebp','print/d $esi','print/d $edi','print/h $eax','print/h $ebx','print/h $ecx',   'print/h $edx','print/h $esp','print/h $ebp','print/h $esi','print/h $edi','print/b $eax','print/b $ebx','print/b $ecx',   'print/b $edx','print/b $esp','print/b $ebp','print/b $esi','print/b $edi']
display=[]
pcnt=1

if not os.path.exists("SymbolTable.txt"):
    open("SymbolTable.txt","w").close()

if not os.path.exists(".literal_table.txt"):
    open(".literal_table.txt","w").close()

def list_call():
    for i in range(len(op_val)):
        print(op_val[i][0],'\t',op_val[i][3])

    return

def display_call(reg):
    rval=0
    val=reg.replace('$','')
    display.append(str(val))
    for j in range(len(final)):
        if final[j]==val:
            rval=(final[j-1])
    for i in range(len(display)):
        if display[i]==val:
            print(i+1,": ",reg,"=",rval)
    return

def display_reg():
    if display!=[]:
        for i in range(len(display)):
            reg=display[i]
            for j in range(len(final)):
                if final[j]==reg:
                    print(i+1,":",reg,"=",final[j-1])


def info_reg_call():
    cnt=1
    for i in range(33,len(final),2):
        print(cnt,":",final[i],"= ",final[i-1])
        cnt+=1
    return


def start_deb():
    cnt=0
    n=len(op_txt)
    print("Breakpoint 1, 0x08048400 in main ()")
    while cnt<n:

        sp=input("(gdb)")
        sk=sp.split()

        if sp=='ni' or sp=='next' or sp=='n':
            decode_opcode(op_txt[cnt][2])
            print(op_txt[cnt][0],":",op_txt[cnt][3])
            display_reg()
            cnt+=1

        if sp=='run':
            e=input("Start it from the beginning? (y or n)")
            if e=='y':
                start_deb()
            if e=='n':
                return
        if sp=='list':
            list_call()

        if sk[0]=='display':
            display_call(sk[1])

        if sp=='info reg':
            info_reg_call()


        if sk[0]=='display':
            display_call(sk[1])

        if sp not in ['n','ni','next','q','quit','list','help','h','info reg','run','display $eax','display $ebx','display $ecx','display $edx','display $esp','display $ebp','display $esi','display $edi','print/d $eax','print/d $ebx','print/d $ecx','print/d $edx','print/d $esp','print/d $ebp','print/d $esi','print/d $edi','print/h $eax','print/h $ebx','print/h $ecx','print/h $edx','print/h $esp','print/h $ebp','print/h $esi','print/h $edi','print/b $eax','print/b $ebx','print/b $ecx','print/b $edx','print/b $esp','print/b $ebp','print/b $esi','print/b $edi']:
            print("Undefined command: %r.  Try 'help' or 'h'." % (sp))


    else:
        print("which has no line number information, end program")



if __name__ == '__main__':

    script,filename=argv
    f1=filename.split('.')
    if f1[1]!='asm':
        print("nasm: fatal: unable to open input file",filename)
        sys.exit()

    sym_table(filename)
    write_file()

    lit_table(filename)
    lit_write()

    obj_code(filename)
    print("run")
    print("ni")
    print("list")
    print("info reg")


    while True:
        sp=input("(gdb)")
        sk=sp.split()

        if sp=='list':
            list_call()

        if sp=='info reg':
            print("The program is not being run.")

        if sp=='run':
            start_deb()

        if sk[0]=='display':
            display_call(sk[1])

        if sp=='n' or sp=='ni' or sp=='next':
            print("The program is not being run.")

        if sp not in ko:
            print("command not found")


