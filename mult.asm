section .data
	msg2 db "sum is = %d",0,10
	num1 dd 18
	num2 dd 20

section .bss

	res resd 1

section .text 
	global main
	extern printf

main:
	mov eax,50
	mov ebx,10
	mul ebx
	
	push eax
	push msg2
	call printf
	add esp,8

