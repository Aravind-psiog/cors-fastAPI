import covalent as ct
# !pip install ase
# !pip install ase-notebook
from ase import Atoms
from ase.calculators.emt import EMT
from ase.constraints import FixAtoms
from ase.optimize import QuasiNewton
from ase.build import fcc111, add_adsorbate
from ase.io import read
from ase.io.trajectory import Trajectory
from ase_notebook import AseView, ViewConfig
from matplotlib import pyplot as plt

@ct.electron
def construct_cu_slab(
    unit_cell=(4, 4, 2),
    vacuum=10.0,
):
    slab = fcc111("Cu", size=unit_cell, vacuum=vacuum)
    return slab


@ct.electron
def compute_system_energy(system):
    system.calc = EMT()
    return system.get_potential_energy()


@ct.electron
def construct_n_molecule(d=0):
    return Atoms("2N", positions=[(0.0, 0.0, 0.0), (0.0, 0.0, d)])


@ct.electron
def get_relaxed_slab(slab, molecule, height=1.85):
    slab.calc = EMT()
    add_adsorbate(slab, molecule, height, "ontop")
    constraint = FixAtoms(mask=[a.symbol != "N" for a in slab])
    slab.set_constraint(constraint)
    dyn = QuasiNewton(slab, trajectory="/tmp/N2Cu.traj", logfile="/tmp/temp")
    dyn.run(fmax=0.01)
    return slab

@ct.lattice
def compute_energy(initial_height=3, distance=1.10):
    N2 = construct_n_molecule(d=distance)
    e_N2 = compute_system_energy(system=N2)

    slab = construct_cu_slab(unit_cell=(4, 4, 2), vacuum=10.0)
    e_slab = compute_system_energy(system=slab)

    relaxed_slab = get_relaxed_slab(slab=slab, molecule=N2, height=initial_height)
    e_relaxed_slab = compute_system_energy(system=relaxed_slab)
    final_result = e_slab + e_N2 - e_relaxed_slab

    return final_result

@ct.lattice
def compute_energy(initial_height=3, distance=1.10):
    N2 = construct_n_molecule(d=distance)
    e_N2 = compute_system_energy(system=N2)

    slab = construct_cu_slab(unit_cell=(4, 4, 2), vacuum=10.0)
    e_slab = compute_system_energy(system=slab)

    relaxed_slab = get_relaxed_slab(slab=slab, molecule=N2, height=initial_height)
    e_relaxed_slab = compute_system_energy(system=relaxed_slab)
    final_result = e_slab + e_N2 - e_relaxed_slab

    return final_result

# ------------------- single lattice workflow ---------------------------------------------------------
# dispatch_id = ct.dispatch(compute_energy)(initial_height=3, distance=1.10)

# result = ct.get_result(dispatch_id=dispatch_id, wait=True)

# print(
#     f"Computation status = {result.status}\nEnergy of slab + nitrogen system = {result.result:.4f}"
# )

# ----------------------------------------------------------------------------------------------------


# ----------------------- sub lattices workflow -------------------------------------------------------
import numpy as np

optimize_height = ct.electron(compute_energy)


@ct.lattice
def vary_distance(distance):
    result = []
    for i in distance:
        result.append(optimize_height(initial_height=3, distance=i))
    return result

import numpy as np

distance = np.linspace(1, 1.5, 3)

vary_distance.draw(distance=np.round(distance, 2))

seps = 7
distance = np.linspace(1, 1.5, seps)
dispatch_id = ct.dispatch(vary_distance)(distance=distance)

# ------------------------------------------------------------------------------------------------------
