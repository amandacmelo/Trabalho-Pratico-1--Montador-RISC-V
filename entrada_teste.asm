lw x10, 48(x23)
sw x11, 200(x12)
add x2, x0, x1
xor x4, x2, x3
addi x3, x2, -243
sll x1, x2, x2
bne x10, x25, 8
srl x0, x2, x2
or x2, x2, x1
andi x2, x1, 16


