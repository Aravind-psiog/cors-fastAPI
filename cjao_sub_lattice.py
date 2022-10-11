import covalent as ct

@ct.electron
def sub_sub_task(x):
    return x**2

@ct.electron
@ct.lattice
def sub_sub_workflow(x):
    # 1 -> 0
    return sub_sub_task(x)

@ct.electron
@ct.lattice
def sub_workflow(x):
    # 1 -> 0
    return sub_sub_workflow(x)

@ct.lattice
def workflow(x):
    # 1 -> 0
    return sub_workflow(x)

dispatch_id = ct.dispatch(workflow)(3)
print(dispatch_id)
print(ct.get_result(dispatch_id, wait=True))