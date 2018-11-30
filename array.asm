section .data
	po dd "hi im in",10,0
	ol dd "my name is batman",10,0
	arr dd 10,20,30,40,-1
section .bss
	n resd 1,20,30
	num resd 100
section .text
	global main
	extern printf,scanf
main:
	push n
	push msg
	call scanf
pq:
	add esp,8	
	im here
	jnz pqr
	jmp ok
	jmp pq

