import covalent as ct
import time
@ct.electron
def identity(x):return x
@ct.electron
def combine(x):return sum(x1)
@ct.lattice
def workflow(n,parallel=False,serial=False):
    vals=[]
    result=1
    time.sleep(5)
    nodes=range(n)
    if parallel and not serial:
        for _ in nodes:
            time.sleep(5)
            vals.append(identity(1))
        vals=combine(vals)
    elif serial and not parallel:
        for _ in nodes:
            result=identity(result)
    elif serial and parallel:
        time.sleep(5)
        for i in nodes:
            for _ in nodes:
                if i==0:
                    vals.append(identity(1))
                else:
                    vals.append(identity(result))
            result=combine(vals)
    return result,vals
dispatcher=ct.dispatch(workflow)
n=7
#parallel_id=dispatcher(n=n,parallel=True) # for horizontal large graph
#serial_id=dispatcher(n=n,serial=True) # for vertical large graph
both_id=dispatcher(n=n,serial=True,parallel=True) # Hagrid level graph
