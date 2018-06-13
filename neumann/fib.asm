funcb 1
mov r1 *sp
add r1 1
mov r2 **r1
mov r3 *r2
sub r3 1
rjgz *r3 5
mov rv *r2
mov r1 **sp
pop
jump *r1
push *r3
call 1
mov r3 **sp
pop
sub r3 1
push *rv
push *r3
call 1
pop
add rv **sp
pop
mov r1 **sp
pop
jump *r1
funce
putstr Hello! This programm will calclulate the n-th member of the fib-sequence [0, 1, 1, 2, 3, 5, 8, ... ]
putstr Enter number n:
read r1
push *r1
call 1
pop
putstr Your answer is:
print *rv
term