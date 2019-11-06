init $1, 0xE
init $1, 0x3	#$8 = B
init $0, 0
init $0, 4
init $2, 0
init $2, 0xF
init $2, 0xF
init $3, 0
add $7, $2
loop_255:
add $5, $2
init $2, 5
add $6, $2
init $2,0
loop_mult:
multxor $5, $1
bnzdec $6, loop_mult
foldmtch $5, $3
store $7($0)
bnzdec $7, loop_255