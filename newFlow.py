import covalent as ct
@ct.electron
def identity(x):
    return x


@ct.electron
def square(x):
    return x * x


@ct.electron
def multiply(x, y):
    return x * y


@ct.lattice
def check(main_input):
    ret = multiply(x=2, y=3)
    for _ in range(20):
        val1 = identity(x=main_input)
        val2 = square(x=ret)
        ret = multiply(x=val2, y=3)
        
    return ret
        
        
dispatcher=ct.dispatch(check)        
dispatcher(main_input=1)
