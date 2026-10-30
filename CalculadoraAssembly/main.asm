default rel

section .bss

    num1 resb 2
    num2 resb 2
    respsum resb 8
    respsub resb 8
section .data
    msg db "Digite Um numero : "
    tmsg equ $ - msg

    msg2 db 10,"Digite Outro Numero : "
    tmsg2 equ $ - msg2

    sum db 10,"A soma é : "
    tsum equ $ - sum

    subt db 10,"A subtracao e : "
    tsub equ $ - subt


section .text
    global _start


_start:
    mov rax,1
    mov rdi,1
    mov rsi,msg ; IMPRIME A MENSAGEM DO 1 NUMERO 
    mov rdx,tmsg
    syscall

    mov rax,0
    mov rdi,0
    mov rsi,num1 ;SALVA 1 NUMERO 
    mov rdx, 2
    syscall
    
    mov r9, [num1] ; R9 RECEBE ASCII (NUM + 48)
    
    mov rax,1
    mov rdi,1
    mov rsi,msg2 ; MENSAGEM 2 NUMERO
    mov rdx,tmsg2
    syscall

    mov rax,0
    mov rdi,0
    mov rsi,num2  ; SALVA 2 NUMERO + ascii
    mov rdx,2
    syscall

    mov r10,[num2]

    mov r12,r10
    add r12,r9 

    mov r13,r9
    sub r13,r10
    add r13, '0'
    

    mov rax,1
    mov rdi,1
    mov rsi,sum ; IMPRIME A MENSAGEM DE SOMA DOS NEGOCIO
    mov rdx,tsum
    syscall

    mov [respsub],r13b
    mov byte [respsub + 1], 10
    mov [respsum],r12
    sub [respsum], 48
    mov byte [respsum + 1], 10

    mov rax,1
    mov rdi,1
    mov rsi,respsum ; IMPRIME A RESPOSTA (SO VAI ATE 10 PQ EU TO COM PREGUICA DE FAZER O BAGUI DE QUOCIENTE PQ E MT LONGO SAPORCARIA)
    mov rdx,2
    syscall

    mov rax,1
    mov rdi,1
    mov rsi,subt
    mov rdx,tsub
    syscall

    mov rax,1
    mov rdi,1
    mov rsi,respsub
    mov rdx,2
    syscall
    
    fim: 
    mov rax,60
    mov rdi,0
    syscall
