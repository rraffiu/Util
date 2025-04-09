def beautify(func):
    def inner(a):
        print("-"*50)
        func(a)
        print("-"*50)
    return inner
@beautify
def output(a):
    print(f"{a}")
output("This is the total energy = " + str(34)+ " eV")
