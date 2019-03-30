import lib2 as lib
auto1=lib.importJFF("m1.jff")
auto2=lib.importJFF("m2.jff")
auto3=lib.unionIntersectionDFA(auto1,auto2,True)
auto4=lib.unionIntersectionDFA(auto1,auto2,False)
lib.export(auto3,"hop.jff")
lib.export(auto4,"giao.jff")