j L43
  


L1: 
sw ra,(sp)
L2: 
lw t1,-0(sp)
li t2,1
ble t1,t2,L4
L3: 
b L6
L4: 
lw t1,-0(sp)
lw t0,-8(sp)
sw t1,(t0)
L5: 
b L16
L6: 
lw t1,-0(sp)
li t2,1
sub t1,t1,t2
sw t1,-16(sp)
L7: 
addi fp,sp,36
lw t0,-16(sp)
sw t0,-12(fp)
L8: 
addi t0,sp,-20
sw t0,-8(fp)
L9: 
addi sp,sp,36
jal L1
addi sp,sp,-36
L10: 
lw t1,-0(sp)
li t2,2
sub t1,t1,t2
sw t1,-24(sp)
L11: 
addi fp,sp,36
lw t0,-24(sp)
sw t0,-12(fp)
L12: 
addi t0,sp,-28
sw t0,-8(fp)
L13: 
addi sp,sp,36
jal L1
addi sp,sp,-36
L14: 
lw t1,-20(sp)
lw t2,-28(sp)
add t1,t1,t2
sw t1,-32(sp)
L15: 
lw t1,-32(sp)
lw t0,-8(sp)
sw t1,(t0)
L16: 
lw ra,(sp)
jr ra
L17: 
sw ra,(sp)
L18: 
lw t1,-0(sp)
lw t2,-0(sp)
div t1,t1,t2
sw t1,-24(sp)
L19: 
lw t1,-24(sp)
lw t2,-0(sp)
mul t1,t1,t2
sw t1,-28(sp)
L20: 
lw t1,-0(sp)
lw t2,-28(sp)
beq t1,t2,L22
L21: 
b L24
L22: 
li t1,1
lw t0,-0(sp)
sw t1,(t0)
L23: 
b L25
L24: 
li t1,0
lw t0,-0(sp)
sw t1,(t0)
L25: 
lw ra,(sp)
jr ra
L26: 
sw ra,(sp)
L27: 
li t1,1
lw t0,-8(sp)
sw t1,(t0)
L28: 
li t1,2
sw t1,-16(sp)
L29: 
lw t1,-16(sp)
lw t2,-0(sp)
blt t1,t2,L31
L30: 
b L42
L31: 
addi fp,sp,32
lw t0,-16(sp)
sw t0,-12(fp)
L32: 
lw t0,-0(sp)
sw t0,-16(fp)
L33: 
addi t0,sp,-20
sw t0,-20(fp)
L34: 
lw t0,-4(sp)
sw t0,-4(fp)
addi sp,sp,32
jal L1
addi sp,sp,-32
L35: 
lw t1,-20(sp)
li t2,1
beq t1,t2,L37
L36: 
b L39
L37: 
li t1,0
lw t0,-8(sp)
sw t1,(t0)
L38: 
b L39
L39: 
lw t1,-16(sp)
li t2,1
add t1,t1,t2
sw t1,-24(sp)
L40: 
lw t1,-24(sp)
sw t1,-16(sp)
L41: 
b L29
L42: 
lw ra,(sp)
jr ra
L43: 
addi sp,sp,32
mv gp,sp
L44: 
li a7,5
ecall
mv t1,a0
L45: 
addi fp,sp,36
lw t0,-12(gp)
sw t0,-12(fp)
L46: 
addi t0,sp,-20
sw t0,-8(fp)
L47: 
lw t0,-4(sp)
sw t0,-4(fp)
addi sp,sp,36
jal L1
addi sp,sp,-36
L48: 
lw t1,-20(sp)
mv a0,t1
li a7,1
ecall
L49: 
li t1,2
sw t1,-16(gp)
L50: 
lw t1,-16(gp)
li t2,30
ble t1,t2,L52
L51: 
b L62
L52: 
addi fp,sp,28
lw t0,-16(gp)
sw t0,-12(fp)
L53: 
addi t0,sp,-24
sw t0,-8(fp)
L54: 
lw t0,-4(sp)
sw t0,-4(fp)
addi sp,sp,28
jal L1
addi sp,sp,-28
L55: 
lw t1,-24(sp)
li t2,1
beq t1,t2,L57
L56: 
b L59
L57: 
lw t1,-16(gp)
mv a0,t1
li a7,1
ecall
L58: 
b L59
L59: 
lw t1,-16(gp)
li t2,1
add t1,t1,t2
sw t1,-28(sp)
L60: 
lw t1,-28(sp)
sw t1,-16(gp)
L61: 
b L50
L62: 
li a0,0
li a7,93
ecall
L63: 
