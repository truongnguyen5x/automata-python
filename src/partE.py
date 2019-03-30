import lib2 as lib

file = input("file dfa: ")
dfa = lib.importJFF(file)
chars = lib.getChars(dfa)
lib.removeUnreachable(dfa)
dfa2 = lib.minimizeDFA2(dfa, chars)
lib.export(dfa2,"dfa2.jff")
