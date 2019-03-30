import lib2 as lib

file = input("file dfa: ")
dfa = lib.importJFF(file)
chars = lib.getChars(dfa)
lib.removeUnreachable(dfa)
lib.export(dfa,'z'+file)