import lib2 as lib
file = input("file: ")
nfa = lib.importJFF(file)
chars = lib.getChars(nfa)
auto = lib.toDFA(nfa, chars)
lib.export(auto, "dfa.jff")



