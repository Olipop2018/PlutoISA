memory = [0] *4096 #Remember when ever you get an address in hex subtract 8192 from it then write to it
				#Dynamic Instruction Count
registers = {"$0": 0, "$1":0,"$2": 0, "$3":0,"$4": 0, 
                  "$5":0,"$6": 0, "$7":0,"a0": 0, "a1":0,"a2": 0, 
                  "a3":0, "lo":0,"hi":0, "loop0":9,"loop1":13,"loop2":0,"loop3":0}
labelIndex = []
labelName = []
pcAssign= []
 
def multXor(A,B):
        tmp = A * B
        tmp= format(tmp,'016b')
        hi2=  int(tmp[:8],2)
        lo2=  int(tmp[8:],2)   
        A = hi2 ^ lo2
        return A


def foldmatch(C, dest):
     C= format(C,'08b')
     C= int(C[4:8],2) ^ int(C[:4],2)
     C= format(C,'04b')
     C=  int(C[2:4],2) ^ int(C[:2],2)
   # now does pattern matachin of C
     registers[dest]= C
     C= format(C,'02b')
     if ('11' in C):
         n3 = registers["a3"] 
         n3+=1
         registers["a3"] = n3
     elif('10' in C):
        n2 = registers["a2"] 
        n2+=1
        registers["a2"] = n2
     elif('01' in C):
         n1 = registers["a1"] 
         n1+=1
         registers["a1"] = n1
     elif('00' in C):
         n0 = registers["a0"]  
         n0+=1
         registers["a0"] = n0

def init(D, dest):
    if(D==0):
        registers["hi"] = D
    elif(D<0):
        registers[dest]= D
        return
    ihi =  registers["hi"]
    registers["hi"] = D
    ihi= format(ihi,'04b')
    D = format(D,'04b')
    D = ihi + D
    D = int(D,2)
    registers[dest]= D # writes the value to the register specified
    print ("result:" ,dest ,"=",  hex(D))

def store(acc):
    memory[acc] = registers["$3"]
    memory[0] = registers["a0"]
    memory[1] = registers["a1"]
    memory[2] = registers["a2"]
    memory[3] = registers["a3"]
    #print(memory)
    


   # registers["$hi"] = n		#Shift high right 32
   # registers["$lo"] = int(C,2)
    #print ("result:" ,"$hi" ,"=", hex(n))
    #print ("result:" ,"$lo" ,"=", hex(int(C,2)))
    


def instrSimulation(instrs, DIC, pc):
   #pc = int(0)
   bcount=0
   #DIC = int(0)
   j= int(0)
   while True:
        bcount+=1
       # num= len(instrs)
        if (int(pc) >= len(instrs)):
           
            print("Dynamic Instruction Count: ",DIC)
            return DIC, pc;
        line = instrs[int(pc)]
        print("Current instruction PC =",pc)
        DIC+=1
        if(line[0:4] == "init"): # INIT
            line = line.replace("init","")
            line = line.split(",")
            if(line[1][0:2]== "0x"):
                n=16
            else:
                n=10
            imm = int(line[1],n) # will get the negative or positive inter value. if unsigned and negative will get the unsigned value of th negative integer.
            rs = imm # reads the value from specified register
            rt = "$" + str(line[0]) # locate the register in which to write to
            instruction = "init" 
            print (instruction , rt, imm if(n== 10) else hex(imm))
            init(rs, rt)
            #result = rs + imm # does the addition operation
            #registers[rt]
            #= result # writes the value to the register specified
            #print ("result:" ,rt ,"=",  hex(result))
            pc += 1# increments pc by 4 
           # pcprint = hex(pc)
            

           # print(registers)# print all the registers and their values (testing purposes to see what is happening)
            #print(pc)
            #print(pcprint)

           
        elif(line[0:5] == "store"): # store
            line = line.replace("store","")
            line = line.replace(")","")
            line = line.replace("(",",")
            line = line.split(",")
            rs = int(registers[("$" + str(line[0]))])
            rt = int(registers[("$" + str(line[1]))])
            instruction = "store"
            print (instruction , ("$" + str(line[0])) + "("+("$" + str(line[1]))+")" )
            mem = rt+ rs
            store(mem)
            memo= mem
            print ("result memory:", hex(memo) ,"=", hex(registers["$3"]))
            pc+= 1# increments pc by 4 
          
           
            
            # pcprint=  hex(pc)
            #print(registers)# print all the registers and their values (testing purposes to see what is happening)
            #print(pc)
            #print(pcprint)  
       
      
        elif(line[0:6] == "bnzdec"): # bne
            line = line.replace("bnzdec","")
            line = line.split(",")
           # for i in range(len(labelName)):
            #        if(labelName[i] == line[1]):
             #          lpos = int(labelIndex[i])
              #         label= labelName[i] 
            #temp2= pcAssign[lpos]
            temp2= registers["loop"+ str(line[1])]
            rs = 0
            rt = registers[("$" + str(line[0]))]
            instruction = "bne" 
            print (instruction , ("$" + str(line[0])) , str(line[1]))
            rt= rt-1
            if(rs != rt):
                #temp2= temp2-pc
                pc=temp2
                #rt= rt-1
                registers[("$" + str(line[0]))]= rt
                registers["$2"]= rt
                #print ("branch to" ,label)
            else:
                pc+= 1
                print ("does not branch, go to next instructions" )
           # pcprint=  hex(pc)
            #print(registers)# print all the registers and their values (testing purposes to see what is happening)
            #print(pc)
            #print(pcprint)

       
            
        elif(line[0:8] == "foldmtch"): # FOLDMATCH
            line = line.replace("foldmtch","")
            line = line.split(",")
            rs = registers[("$" + str(line[0]))]	#First register
            rt = "$" + str(line[1])	#Second register
            instruction = "cfold" 
            print (instruction , ("$" + str(line[0])) ,("$" + str(line[1])))
            foldmatch(rs, rt)
            
            pc += 1# increments pc by 4 
           # pcprint =  hex(pc)
           # print(registers)# print all the registers and their values (testing purposes to see what is happening)
           # print(pc)
            #print(pcprint)

        elif(line[0:7] == "multxor"): # MULT/U
            line = line.replace("multxor","")
            line = line.split(",")
            rs = registers[("$" + str(line[0]))]	#First register
            rt = registers[("$" + str(line[1]))]	#Second register
            rs= int(rs) if int(rs) > 0  else (65536 + int(rs))
            rt= int(rt) if int(rt) > 0  else (65536 + int(rt))
            instruction = "mult"
            print (instruction , ("$" + str(line[0])) ,("$" + str(line[1])))
            rslt =multXor(rs,rt)
            registers[("$" + str(line[0]))] = rslt	
            print ("result:" ,"$" + str(line[0]) ,"=", hex(rslt))
            pc += 1# increments pc by 4 
             
            #pcprint =  hex(pc)
            #print(registers)# print all the registers and their values (testing purposes to see what is happening)
            #print(pc)
            #print(pcprint) 
           
#        elif(line[0:3] == "xor"): # XOR
 #           line = line.replace("xor","")
  #          line = line.split(",")
   #         rd = "$" + str(line[0])
    #        rs = registers[("$" + str(line[1]))]
     #       rt = registers[("$" + str(line[2]))]
      #      instruction = "xor"
       #     print (instruction , rd ,("$" + str(line[1])), ("$" + str(line[2])))
        #    result = rs ^ rt # does the addition operation
         #   registers[rd]= result
          #  print ("result:" ,rd ,"=", hex(result))
            
           # pc+= 1 # increments pc by 4 
             
           # pcprint =  hex(pc)
           # print(registers)# print all the registers and their values (testing purposes to see what is happening)
           # print(pc)
           # print(pcprint)
       
        elif(line[0:3] == "add"): # ADD
            line = line.replace("add","")
            line = line.split(",")
            rd =  registers[("$" + str(line[0]))]
            rs = registers[("$" + str(line[1]))]
          # rt = registers[("$" + str(line[2]))]
            instruction = "add"
            print (instruction , ("$" + str(line[0])),("$" + str(line[1])))
            result = rs # does the addition operation
            registers[("$" + str(line[0]))]= result
            print ("result:" ,("$" + str(line[0])),"=", hex(result))
            pc+= 1 # increments pc by 1
           # pcprint =  hex(pc)
           # print(registers)# print all the registers and their values (testing purposes to see what is happening)
           # print(pc)
           # print(pcprint)
        
      

        elif(line[0:1] == "j"): # JUMP
            line = line.replace("j","")
            line = line.split(",")
            instruction = "j" 
            print (instruction , ("$" + str(line[0])))
           
            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location

            if(line[0].isdigit()): # First,test to see if it's a label or a integer
                pc= int(line[0])
               # hexstr= hex(int(hexstr[0], 2))
               # f.write(hexstr + '\n')#str('000010') + str(format(int(line[0]),'026b')) + '\n'+ hexstr+ '\n')

            else: # Jumping to label
                for i in range(len(labelName)):
                    if(labelName[i] == line[0]):
                        lpos = int(labelIndex[i]-1)
                        
                pc= (pcAssign[lpos])+4
                print ("branch to" ,label)
        print("Next instruction PC =",pc)
                        #pc= format(int(labelIndex[i]),'026b')
                        #pc = int(pc,2)
                        #hexstr= hex(int(hexstr[0], 2))
                       # f.write(hexstr+ '\n')#str('000010') + str(format(int(labelIndex[i]),'026b')) + '\n'+ hexstr+ '\n')
  

def saveJumpLabel(asm,labelIndex, labelName):
    lineCount = 0
    ppc= 0
    w = 0
    for line in asm:
        line = line.replace(" ","")
        if":" in line:
            pcAssign.append(w)
            registers["loop"+ str(w)] = ppc
            w+=1
        else:
            pcAssign.append(ppc)  
            ppc+=1
        if(line.count(":")):
            labelName.append(line[0:line.index(":")]) # append the label name
            labelIndex.append(lineCount) # append the label's index
            asm[lineCount] = line[line.index(":")+1:]
        lineCount += 1
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

def main():
   # f = open("mc.txt","w+")
    h = open("mc4.txt","r")
    asm = h.readlines()
    instrs = []
    FinalDIC= 0
    FinalPC= 0
    
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')
       
    saveJumpLabel(asm,labelIndex,labelName) # Save all jump's destinations
    
    for line in asm:
        #line = line.replace("\t","")
        #line = line.replace('"','')
        if(line[0:2]== '01'):
            line = "init"+ str(int(line[2:4],2))+","+ str(int(line[4:],2))
        elif(line[0:3]== '100'):
            line = "add"+ str(int(line[3:6],2))+","+ str(int(line[6:],2))
        elif(line[0:3]== '001'):
            line = "multxor"+ str(int(line[3:6],2))+","+ str(int(line[6:],2))
        elif(line[0:3]== '110'):
            line = "bnzdec"+ str(int(line[3:6],2))+","+ str(int(line[6:],2))
        elif(line[0:3]== '111'):
            line = "foldmtch"+ str(int(line[3:6],2))+","+ str(int(line[6:],2))
        elif(line[0:3]== '101'):
            line = "store"+ str(int(line[3:6],2))+"("+ str(int(line[6:],2))+ ")"
        line = line.replace("\n","") # Removes extra chars
        line = line.replace("$","")
        line = line.replace(" ","")
        line = line.replace("zero","0") # assembly can also use both $zero and $0
        instrs.append(line)
    print(instrs)
    print(pcAssign)
    FinalDIC, FinalPC = instrSimulation(instrs, FinalDIC, FinalPC)
    print("memory contents from 0 - 264:")
    for k in range(0,265):
        mem= 8192+ k
        memlo= mem- 8192
        first = format(memory[memlo])
        print("memory","{}: {}".format(memlo,first), end='| ')
        if(k%12 == 0 and k > 0):
            print("\n")
    
    print("all register values:")
    proregister= str(registers)
    proregister= proregister.replace("'","")
    proregister= proregister.replace("{","")
    proregister= proregister.replace("}","")
    proregister= proregister.replace(",","\n")
    #print(registers)
    print(" "+ proregister)
    print("Final PC =",FinalPC)
   # print("memory contents from 0x2000 - 0x2050:")
    #for l in range(0,260):
     #   mem= 8192+ l
      #  memlo= mem- 8192
       # first = format(memory[memlo])
        #print("memory"," {} : {}".format(memlo,first))
    print("Dynamic Instruction Count: ",FinalDIC)

if __name__ == "__main__":
    main()
