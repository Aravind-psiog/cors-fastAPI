import covalent as ct
from covalent.executor import DaskExecutor
from covalent._workflow.lattice import Lattice
# from dask.distributed import LocalCluster

# lc = LocalCluster()
# dask_exec = DaskExecutor(lc.scheduler_address)

@ct.electron(executor="local")
def square(x):
    return x**2

@ct.electron(executor="local")
def cube(x):
    return x**3


@ct.lattice
def workflow(x):
    res1 = square(x)
    res2 = cube(x)

id=ct.dispatch(workflow)(x=1)

workflow.build_graph(2)
received_lattice = Lattice.deserialize_from_json(workflow.serialize_to_json())

tg = received_lattice.transport_graph._graph
