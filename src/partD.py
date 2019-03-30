import lib2 as lib

file = input("file dfa: ")
dfa = lib.importJFF(file)
chars = lib.getChars(dfa)
dfa2 = lib.minimizeDFA(dfa, chars)
lib.export(dfa2,"dfa1.jff")
