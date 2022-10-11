import covalent as ct

@ct.lattice
@ct.electron
def task():
    return True

ct.dispatch(task)()
