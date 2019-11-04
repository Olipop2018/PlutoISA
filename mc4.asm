init $1, 0x6
init $1 0x6	#$8 = B
init $0, 0
#Code begins
init $2, 0xF 
init $2, xF
init $0,0
add $7, $2 #255
add $5, $7# A
init $0, 0
init $2, -1
add $4, $2
init $2, 0
init $0, 4
loop_255:
init $2, 5
add $6, $2# has 5
init $2,0
add $5, $7# A
loop_mult:	#Loop mult/fold
multxor $5, $1
bnzerodec $6, loop_mult	#If $11 /0 0 loop
foldmtch $5, $3
store $7, $0
add $7, $4
bnzerodec $7, loop_255	