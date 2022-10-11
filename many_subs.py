import covalent as ct

@ct.electron
def add(a,b):
    return a+b

@ct.electron
def sub(a,b):
    return a-b

@ct.electron
@ct.lattice
def mul(a,b):
    res1 = add(a,b)
    res2 = sub(a,b)
    return res1,res2

@ct.electron
@ct.lattice
def div(a,b):
    a = add(a,b)
    b = sub(a,b)
    return a/b

@ct.electron
@ct.lattice
def sub(a,b):
    res1 = add(a,b)
    res2 = sub(a,b)
    return res1,res2

@ct.lattice
def solution(a,b):
    res1,res2 = mul(a,b)
    sol = div(res1,res2)
    sub(5,3)
    sub(5,3)
    sub(5,3)
    sub(5,3)
    sub(5,3)
    sub(5,3)
    sub(5,3)
    sub(5,3)
    sub(5,3)
    sub(5,3)
    sub(5,3)
    sub(5,3)
    sub(5,3)
    return sol

print(ct.dispatch(solution)(3,2) )