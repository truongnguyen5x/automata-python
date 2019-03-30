import lib2 as lib
file=input("file: ")
auto=lib.importJFF(file)
while True:
    w = input("Input string: [or enter q to quit]: ")
    if w == "q":
        exit()
    result = lib.checkString(auto["init"], w)
    print("Yes" if result else 'No')