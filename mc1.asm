#Required commands
	init $1, 0xF
	init $1 0xA	#$8 = B
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
	
#XOR C into Byte 			#Reset multply counter
	#addi $15, $0, 0x2000	#Part B register start
	foldmtch $5, $3
	store $7, $0
	add $7, $4
	bnzerodec $7, loop_255	
	#srl $18, $14, 16
	#andi $14, $14, 0xFFFF # bitmask(zeroing out) most significant bits(leftost numbers)
	#xor $14, $18, $14
	#srl $18, $14, 8
	#andi $14, $14, 0xFF
	#xor $14, $18, $14
	
#Store
	#sw $14, 0($9)		#Store
	#addi $9, $9, -4		#Decrement address
	#addi $10, $10, -1	#Decrement counter/value
	#addi $14, $10, 0	#Reset A
	#bne $10, $0, loop_mult	#If $10 /= 0 loop
	
#Part B begins

#	addi $9, $9, 4		#Reset start address 0x2020
#	addi $18, $0, 4		#Multiplication factor + Counter
#	addi $19, $0, 0 	#To be SLL
#	addi $20, $0, 0 	#Part B(ii) number
#	addi $10, $0, 100	#Counter for 1-100 
#	addi $21, $0, 0		#Set counter
#	addi $23, $0, 1		#BNE useful logic

#Part B(ii) anaylsis
	
#loop_pm:	#Loop pattern matching
#	sltiu $21, $19, 0xf8	#Check if less than since I know f8 = 11111000
#	addi $18, $18, -1	#Decrement count
#	sll $19, $19, 1		#Shift left 1
#	sw $19, 0x201c($0)	
#	lbu $19, 0x201c($0)
#	bne $21, $23, skip_s	#If f8 or higher skip_s
#	bne $18, $0, loop_pm 	#If counter not 0 
#	bne $18, $23, skip_fr	#If counter 0 and no skip_s
	
#skip_s: 	#Skip match success
#	addi $20, $20, 1	#Increment part B(ii)
	
#skip_fr: 	#Skip Fold
#	lw $19, 0($9)		#Load
#	addi $18, $0, 4		#Reset multiplication factor + Counter
#	addi $10, $10, -1	#Decrement amount of times needed to loop
#	addi $9, $9, 4		#Next number
#	bne $10, $0, loop_pm	#Loop remaining numbers
#	sw $20, 0x2000($0)	#Store pattern matching
