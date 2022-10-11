from concurrent.futures import Executor
import covalent as ct

@ct.electron(executor="2132")
def hello(): return "Hello "

@ct.electron
def moniker(name): return name+" "

@ct.electron
def join(*a): return "".join(a)

@ct.lattice
def workflow(name):
	result=join(hello(),moniker(name))
	return result+" !!"

id=ct.dispatch(workflow)(name="shore")
ct.get_result(id,wait=True)
