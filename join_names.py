import covalent as ct

@ct.electron
def spacer(word): return word+" "

@ct.electron
def join(*a): return "".join(a)

@ct.lattice
def workflow(name):
	return join(spacer("hello"),spacer(name)) +" !!"

id=ct.dispatch(workflow)(name="Shore")
result_ct=ct.get_result(id,wait=True)
print(result_ct)

