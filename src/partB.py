import lib2 as lib
file1=input("file1: ")
file2=input("file2: ")
auto1=lib.importJFF(file1)
auto2=lib.importJFF(file2)
auto3=lib.unionIntersectionDFA(auto1,auto2,True)
auto4=lib.unionIntersectionDFA(auto1,auto2,False)
lib.export(auto3,"hop.jff")
lib.export(auto4,"giao.jff")