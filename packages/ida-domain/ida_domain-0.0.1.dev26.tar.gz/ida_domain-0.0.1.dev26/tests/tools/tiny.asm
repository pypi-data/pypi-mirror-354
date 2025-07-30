BITS 64
section .text
    global _start

_start:
    ; Print "Hello, IDA!"
    mov rax, 1              ; syscall: sys_write
    mov rdi, 1              ; file descriptor (stdout)
    lea rsi, [rel hello]    ; Load string address
    mov rdx, hello_len      ; String length
    syscall

    ; Perform addition: add_numbers(5, 10)
    mov rdi, 5
    mov rsi, 10
    call add_numbers
    mov r12, rax            ; Store sum result

    ; Print "Sum: "
    mov rax, 1
    mov rdi, 1
    lea rsi, [sum_str]
    mov rdx, sum_len
    syscall

    ; Print sum result
    mov rdi, r12
    call print_number

    ; Print newline
    mov rax, 1
    mov rdi, 1
    lea rsi, [newline]
    mov rdx, newline_len
    syscall

    ; Perform multiplication: multiply_numbers(5, 10)
    mov rdi, 5
    mov rsi, 10
    call multiply_numbers
    mov r12, rax            ; Store product result

    ; Print "Product: "
    mov rax, 1
    mov rdi, 1
    lea rsi, [product_str]
    mov rdx, product_len
    syscall

    ; Print product result
    mov rdi, r12
    call print_number

    ; Print newline
    mov rax, 1
    mov rdi, 1
    lea rsi, [newline]
    mov rdx, newline_len
    syscall

    ; Exit
    mov rax, 60             ; syscall: exit
    xor rdi, rdi
    syscall

; ------------------------------------------------------------------
; Function: add_numbers(int a, int b) -> int
; Adds two numbers and returns the result in RAX.
; ------------------------------------------------------------------
add_numbers:
    push rbp
    mov rbp, rsp
    mov rax, rdi
    add rax, rsi
    pop rbp
    ret

; ------------------------------------------------------------------
; Function: multiply_numbers(int a, int b) -> int
; Multiplies two numbers and returns the result in RAX.
; ------------------------------------------------------------------
multiply_numbers:
    push rbp
    mov rbp, rsp
    mov rax, rdi
    imul rax, rsi
    pop rbp
    ret

; ------------------------------------------------------------------
; Function: print_number(int num)
; Converts a number to ASCII and prints it to stdout.
; ------------------------------------------------------------------
print_number:
    mov rbx, rsp
    sub rsp, 20             ; Reserve stack space
    mov rsi, rsp
    mov rcx, 10             ; Base 10
    mov rdx, 0              ; Clear remainder

.print_digit:
    div rcx                 ; RAX /= 10, remainder in RDX
    add dl, '0'             ; Convert remainder to ASCII
    dec rsi                 ; Move buffer pointer
    mov [rsi], dl           ; Store digit
    test rax, rax
    jnz .print_digit        ; Continue if RAX != 0

    mov rax, 1              ; syscall: sys_write
    mov rdi, 1
    mov rdx, rbx
    sub rdx, rsi            ; Calculate printed string length
    syscall

    add rsp, 20             ; Restore stack
    ret

section .rodata
    hello       db "Hello, IDA!", 10, 0  ; Ensure null termination
    hello_len   equ $ - hello

    sum_str     db "Sum: "
    sum_len     equ $ - sum_str

    product_str db "Product: "
    product_len equ $ - product_str

    newline     db 10
    newline_len equ 1

    float_val   dd 0x4048F5C3      ; 3.14 as 32-bit IEEE float
    double_val  dq 0x40191EB851EB851F ; 6.28 as 64-bit IEEE double
