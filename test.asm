;Rollno: 17161
;Name  : Yewale Pavan Vitthal

section .data
	str: db "******",10,0
	str2: db "++++++",0
	str3: db "||||||",0
	str4: db "------",10,10,0
	msg: db "****",0
	msg3: db "",10,0
	mem: db "m",0
	clr: db "clear",0
section .bss
	n resd 4
	c resd 1
section .text
	extern printf,system
	global main
main:
	mov dword[n],6
lebel:
	call print
	call swap
	call waitt
	push clr
	call system
	add esp,4
	jmp lebel
swap:
	mov al,byte[str]
	mov byte[mem],al
	mov esi,1
	mov ecx,str
	call repeat
	dec esi
	mov bl,byte[str3]
	mov byte[ecx+esi],bl
	mov ecx,str3
	mov esi,1
	call repeat
	dec esi
	mov eax,dword[n]
	mov bl,byte[str4+eax-1]
	mov byte[ecx+esi],bl
	mov esi,dword[n]
	dec esi
	dec esi
	mov ecx,str4
	call repeat1
	mov esi,dword[n]
	mov bl,byte[str2+esi-1]
	mov byte[str4],bl
	mov ecx,str2
	sub esi,2
	call repeat1
	mov al,byte[mem]
	mov byte[str2],al
	ret
repeat:
	mov bl,byte[ecx+esi]
	dec esi
	mov byte[ecx+esi],bl
	inc esi
	inc esi
	cmp esi,dword[n]
	jnz repeat
	ret
repeat1:
	mov bl,byte[ecx+esi]
	inc esi
	mov byte[ecx+esi],bl
	dec esi
	dec esi
	cmp esi,-1
	jnz repeat1
	ret
print:	
	push str
	call printf
	add esp,4
	mov edi,str2
	mov ebp,str3
	mov esi,0
dooo:	
	;push msg
	;call printf
	;add esp,4
	mov eax,4
	mov ebx,1
	mov ecx,edi
	mov edx,1
	int 0x80
	;push msg
	;call printf
	;add esp,4
	mov eax,4
	mov ebx,1
	mov ecx,ebp
	mov edx,1
	int 0x80
	push msg3
	call printf
	add esp,4
	inc esi
	inc edi
	inc ebp
	cmp esi,dword[n]
	jnz dooo
	push str4
	call printf
	add esp,4
	ret
waitt:
	mov eax,0
do:	
	inc eax
	cmp eax,100000000
	jnz do
	ret
end:

