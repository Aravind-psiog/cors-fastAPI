import covalent as ct
from covalent._data_store import DataStore

@ct.electron
def spacer(word): return word+" "

@ct.electron
def join(*a): return "".join(a)

@ct.electron
@ct.lattice
def wrap_upper(data: str): return data.upper()

@ct.electron
@ct.lattice
def wrap_lower(data: str): return data.lower()

@ct.electron
@ct.lattice
def wrap_lower_sublattice2(data:str): 
    return data.join(" I'm sub 2 lattice ")



@ct.lattice
def workflow(name):
    a = wrap_upper(join(spacer("hello"),spacer(name)) +" !!")
    b = wrap_lower(join(spacer("hello"),spacer(name)) +" !!")
    c = wrap_lower_sublattice2(wrap_lower(join(spacer("hello"),spacer(name)) +" !!"))
    return a + b + c



workflows= [
    (workflow,("sam"))
]

db = DataStore("sqlite+pysqlite:///results.db", initialize_db=True)
electron_id = 0
edge_id = 0
lattice_id = 0
electrons = []
edges = []
lattices = []

for workflow in workflows:
    lattice_id = lattice_id + 1
    lattice, args = workflow
    dispatch_id = ct.dispatch(lattice)(*args)
    print("***DISPATCH***")
    print(dispatch_id)
