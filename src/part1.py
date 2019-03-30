import lib2 as lib
auto = lib.importJFF("dfa.jff")
w = input("Enter string w: ")
result = lib.checkString(auto["init"], w)
print("Yes" if result else 'No')
