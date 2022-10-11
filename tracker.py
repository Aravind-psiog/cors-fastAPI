import numpy as np
import covalent as ct
from covalent.executor import DaskExecutor
from covalent._workflow.lattice import Lattice
from dask.distributed import LocalCluster
from covalent.executor.executor_plugins.local import LocalExecutor
if __name__ == "__main__":
    lc = LocalCluster()
    le=LocalExecutor()
    dask_exec = DaskExecutor(lc.scheduler_address)
    N = 5
    STALL = 1e5
    X = 20
    @ct.electron(executor=le)
    def matrix_workload(mat_1, mat_2, stall=STALL, x=X):
        i = 0
        while i < stall:
            x * x
            i += 1
        return mat_1
    @ct.electron(executor=dask_exec)
    def matrix_flatten(mat_1):
        return np.ravel(mat_1)
    @ct.electron(executor=le)
    def split_in_half(mat_1):
        return np.array_split(mat_1, 2)
    @ct.lattice(executor=le)
    def inflate(mat_1, dim=3):
        mat_2 = np.random.default_rng().integers(3, size=(dim, dim))
        mat_3 = matrix_workload(mat_1, mat_2)
        mat_4 = matrix_flatten(mat_3)
        mat_5 = matrix_workload(mat_1, mat_3)
        return matrix_workload(mat_4, mat_5)
    @ct.lattice(executor=dask_exec)
    def deflate(mat_1, dim=3):
        mat_2 = np.random.default_rng().integers(3, size=(dim, dim))
        mat_3, mat_4 = split_in_half(mat_1)
        mat_5 = matrix_workload(mat_1, mat_3)
        mat_6 = matrix_workload(mat_2, mat_4)
        mat_7 = matrix_flatten(mat_5)
        mat_8, mat_9 = split_in_half(mat_6)
        return mat_8, matrix_workload(mat_7, mat_9)
    @ct.electron
    @ct.lattice(executor=le)
    def idi(mat_1):
        mat_2 = inflate(mat_1)
        mat_3, mat_4 = deflate(mat_2)
        mat_5 = inflate(mat_3)
        return matrix_workload(mat_4, mat_5)
    @ct.lattice(executor=dask_exec)
    def workflow(dim=3):
        mat_1 = np.random.default_rng().integers(10, size=(dim, dim))
        mat_2, mat_3 = split_in_half(mat_1)
        mat_4 = matrix_workload(mat_2, mat_3)
        mat_5 = inflate(mat_4, dim)
        mat_6 = matrix_flatten(mat_5)
        mat_7 = inflate(mat_5)
        mat_8, mat_9 = deflate(mat_6)
        mat_10 = idi(mat_9)
        return matrix_workload(matrix_workload(mat_7, mat_10), mat_8)
    iterations = list(range(N))
    execution_time_taken = []
    dispatch_ids = [ct.dispatch(workflow)() for _ in iterations]
