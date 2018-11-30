from finalObj import *
from sys import argv
import sys

final=['0','al','0','bl','0','cl','0','dl','0','ah','0','bh','0','ch','0','dh','0','ax','0','bx','0','cx','0','dx','0','sp','0','bp','0','si','0','di','0','eax','0','ebx','0','ecx','0','edx','0','esp','0','ebp','0','esi','0','edi']
stack=[]
if not os.path.exists("SymbolTable.txt"):
    open("SymbolTable.txt","w").close()

if not os.path.exists(".literal_table.txt"):
    open(".literal_table.txt","w").close()

def move_decode(reg,val):
        for i in range(len(final)):
            if final[i]=='eax' and reg==184:
                final.pop(i-1)
                final.insert(i-1,val)
                break
            if final[i]=='ebx' and reg==185:
                final.pop(i-1)
                final.insert(i-1,val)
                break
            if final[i]=='ecx' and reg==186:
                final.pop(i-1)
                final.insert(i-1,val)
                break
            if final[i]=='edx' and reg==187:
                final.pop(i-1)
                final.insert(i-1,val)
                break
            if final[i]=='esp' and reg==188:
                final.pop(i-1)
                final.insert(i-1,val)
                break
            if final[i]=='ebp' and reg==189:
                final.pop(i-1)
                final.insert(i-1,val)
                break
            if final[i]=='esi' and reg==190:
                final.pop(i-1)
                final.insert(i-1,val)
                break
            if final[i]=='edi' and reg==191:
                final.pop(i-1)
                final.insert(i-1,val)
                break

def decode_mov2(reg,add):
    temp=None
    val1=None
    for i in range(len(op_dat)):
        if op_dat[i][1]==add:
            temp=(op_dat[i][4])

    if temp!=None:
        for i in range(len(sym_val)):
            if sym_val[i][1]==temp:
                val1=int((sym_val[i][6]),10)

    for i in range(len(final)):
        if reg in ['05','0D','15','1D'] and final[i] in ['eax','ebx','ecx','edx']:
            final.pop(i-1)
            final.insert(i-1,val1)
            break
def decode_add(reg):
    for i in range(len(final)):
        if reg=='C0' and final[i]=='eax':                         # add eax,eax
            for j in range(len(final)):
                if reg=='C0' and final[j]=='eax':
                    temp=final[j-1]+final[i-1]
                    final.pop(j-1)
                    final.insert(j-1,temp)
            break

        if reg=='C1' and final[i]=='eax':                        # add ebx,eax
            for j in range(len(final)):
                if reg=='C1' and final[j]=='ebx':
                    temp=final[j-1]+final[i-1]
                    final.pop(j-1)
                    final.insert(j-1,temp)
            break

        if reg=='C2' and final[i]=='eax':                        # add ecx,eax
            for j in range(len(final)):
                if reg=='C2' and final[j]=='ecx':
                    temp=final[j-1]+final[i-1]
                    final.pop(j-1)
                    final.insert(j-1,temp)
            break

        if reg=='C3' and final[i]=='eax':                        # add edx,eax
            for j in range(len(final)):
                if reg=='C3' and final[j]=='edx':
                    temp=final[j-1]+final[i-1]
                    final.pop(j-1)
                    final.insert(j-1,temp)
            break

        if reg=='C8' and final[i]=='ebx':                        # add eax,ebx
            for j in range(len(final)):
                if reg=='C8' and final[j]=='eax':
                    temp=final[j-1]+final[i-1]
                    final.pop(j-1)
                    final.insert(j-1,temp)
            break

        if reg=='C9' and final[i]=='ebx':                        # add ebx,ebx
            for j in range(len(final)):
                if reg=='C9' and final[j]=='ebx':
                    temp=final[j-1]+final[i-1]
                    final.pop(j-1)
                    final.insert(j-1,temp)
            break

        if reg=='CA' and final[i]=='ebx':                        # add ecx,ebx
            for j in range(len(final)):
                if reg=='CA' and final[j]=='ecx':
                    temp=final[j-1]+final[i-1]
                    final.pop(j-1)
                    final.insert(j-1,temp)
            break

        if reg=='CB' and final[i]=='ebx':                        # add edx,ebx
            for j in range(len(final)):
                if reg=='CB' and final[j]=='edx':
                    temp=final[j-1]+final[i-1]
                    final.pop(j-1)
                    final.insert(j-1,temp)
            break

        if reg=='D0' and final[i]=='ecx':                        # add eax,ecx
            for j in range(len(final)):
                if reg=='D0' and final[j]=='eax':
                    temp=final[j-1]+final[i-1]
                    final.pop(j-1)
                    final.insert(j-1,temp)
            break

        if reg=='D1' and final[i]=='ecx':                        # add ebx,ecx
            for j in range(len(final)):
                if reg=='D1' and final[j]=='ebx':
                    temp=final[j-1]+final[i-1]
                    final.pop(j-1)
                    final.insert(j-1,temp)
            break

        if reg=='D2' and final[i]=='ecx':                        # add ecx,ecx
            for j in range(len(final)):
                if reg=='D2' and final[j]=='ecx':
                    temp=final[j-1]+final[i-1]
                    final.pop(j-1)
                    final.insert(j-1,temp)
            break

        if reg=='D3' and final[i]=='ecx':                        # add edx,ecx
            for j in range(len(final)):
                if reg=='D3' and final[j]=='edx':
                    temp=final[j-1]+final[i-1]
                    final.pop(j-1)
                    final.insert(j-1,temp)
            break

        if reg=='D8' and final[i]=='edx':                        # add eax,edx
            for j in range(len(final)):
                if reg=='D8' and final[j]=='eax':
                    temp=final[j-1]+final[i-1]
                    final.pop(j-1)
                    final.insert(j-1,temp)
            break

        if reg=='D9' and final[i]=='edx':                        # add ebx,edx
            for j in range(len(final)):
                if reg=='D9' and final[j]=='ebx':
                    temp=final[j-1]+final[i-1]
                    final.pop(j-1)
                    final.insert(j-1,temp)
            break

        if reg=='DA' and final[i]=='edx':                        # add ecx,edx
            for j in range(len(final)):
                if reg=='DA' and final[j]=='ecx':
                    temp=final[j-1]+final[i-1]
                    final.pop(j-1)
                    final.insert(j-1,temp)
            break

        if reg=='DB' and final[i]=='edx':                        # add edx,edx
            for j in range(len(final)):
                if reg=='DB' and final[j]=='edx':
                    temp=final[j-1]+final[i-1]
                    final.pop(j-1)
                    final.insert(j-1,temp)
            break

def decode_push(sp,ad):
    temp=None
    for i in range(len(final)):
        if sp>=80 and sp<= 87 and final[i] in ['eax','ebx','ecx','edx','esp','ebp','esi','edi']:
            stack.insert(0,final[i-1])


    for i in range(len(op_dat)):
        if op_dat[i][1]==ad:
            temp=(op_dat[i][4])

    if temp!=None:
        for i in range(len(sym_val)):
            if sym_val[i][1]==temp:
                val=(sym_val[i][6])
                stack.insert(0,val)

def decode_call():
    for i in range(len(stack)):
        print(stack[i])
    print("\n")


def decode_opcode(code):
    v1=code[0:2]
    v2=int(v1,16)
                                                             # check mov instraction
    if v2 in range(184,192):
        v3=code[2:]
        v4=v3.replace('0',"")
        v5=v4.rstrip()
        v6=int(v5,16)
        move_decode(v2,v6)                                     # decode mov
    if v2==139:
        v3=code[2:4]
        v4=code[5:13]
        decode_mov2(v3,v4)

                                                              # check add instraction
    if v2==1:
        v3=code[2:]
        v4=v3.replace('0','')
        v5=v4.rstrip()
        v6='{:0<2}'.format(v5)
        decode_add(v6)
                                                             # check push
    if v2 in range(80,88) or v2==255:
        v3=code[4:]
        v4=v3.replace('[','')
        v5=v4.replace(']','')
        v6=v5.rstrip()
        decode_push(v2,v6)                                  # decode push

    if v2==232:
        decode_call()


def scode():
    print(op_txt)
    for i in range(len(op_txt)):
        val=op_txt[i][2]
        decode_opcode(val)                                   #decode opcode



if __name__ == '__main__':

    script,filename=argv
    f1=filename.split('.')
    if f1[1]!='asm':
        print("file opening error",filename)
        sys.exit()

    sym_table(filename)
    write_file()

    lit_table(filename)
    lit_write()

    obj_code(filename)
    print("stack")
    print(stack)
    print(final)
    scode()
    print(final)
