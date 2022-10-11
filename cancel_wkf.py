import covalent as ct
import time

@ct.electron
def task_1():
    time.sleep(10)
    print("Task 1")
    return 5

@ct.electron
def task_2(b, c):
    time.sleep(b + c)
    print("Task 2")

@ct.lattice
def workflow(x):
    task_2(task_1(), x)
    return x ** 2

dispatch_id = ct.dispatch(workflow)(10)
print(dispatch_id)

time.sleep(3)
result = ct.get_result(dispatch_id)
print(result)
ct.cancel_workflow(dispatch_id)
result = ct.get_result(dispatch_id, wait=True)
print(result)

print(result.get_all_node_outputs())