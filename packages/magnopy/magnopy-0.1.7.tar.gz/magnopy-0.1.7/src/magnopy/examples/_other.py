# MAGNOPY - Python package for magnons.
# Copyright (C) 2023-2025 Magnopy Team
#
# e-mail: anry@uv.es, web: magnopy.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import numpy as np

from magnopy._parameters._p22 import from_dmi, from_iso
from magnopy._spinham._convention import Convention
from magnopy._spinham._hamiltonian import SpinHamiltonian

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def ivuzjo(N=10, J=10):
    r"""
    Prepare a Hamiltonian as in the example of [1]_.

    .. math::

        \mathcal{H}
        =
        -\dfrac{1}{2}
        \sum_{\mu, \nu}
        J
        \boldsymbol{S}_{\mu}
        \cdot
        \boldsymbol{S}_{\mu+\nu}
        -
        \dfrac{1}{2}
        \sum_{\mu, \nu}
        \dfrac{J}{2}
        \boldsymbol{r}_{\nu}
        \left(
        \boldsymbol{S}_{\mu}
        \times
        \boldsymbol{S}_{\mu+\nu}
        \right)
        +
        \sum_{\mu}
        J
        \boldsymbol{\hat{z}}
        \boldsymbol{S}_{\mu}

    Parameters
    ----------
    N : int, default 10
        Size of the supercell (N x N).
    J : float, default 10
        Value of the isotropic exchange in energy units (meV).

    Returns
    -------
    spinham : :py:class:`.SpinHamiltonian`
        Spin Hamiltonian (with magnetic field)

    References
    ----------
    .. [1] Ivanov, A.V., Uzdin, V.M. and Jónsson, H., 2021.
        Fast and robust algorithm for energy minimization of spin systems applied
        in an analysis of high temperature spin configurations in terms of skyrmion
        density.
        Computer Physics Communications, 260, p.107749.

    """

    J = 10

    D = J / 2

    BOHR_MAGNETON = 0.057883818060  # meV / Tesla

    cell = np.eye(3, dtype=float) * N

    atoms = dict(names=[], positions=[], g_factors=[], spins=[])
    names_to_index = {}
    atom_index = 0
    for i in range(0, N):
        for j in range(0, N):
            atoms["names"].append(f"Fe_{i+1}_{j+1}")
            atoms["positions"].append([i + 0.5, j + 0.5, 0])
            atoms["spins"].append(1)
            atoms["g_factors"].append(2)
            names_to_index[f"Fe_{i+1}_{j+1}"] = atom_index
            atom_index += 1

    convention = Convention(
        multiple_counting=True, spin_normalized=False, c21=-1, c22=-0.5
    )

    spinham = SpinHamiltonian(cell=cell, atoms=atoms, convention=convention)

    # For each atom add bonds
    for i in range(0, N):
        for j in range(0, N):
            alpha = names_to_index[f"Fe_{i+1}_{j+1}"]

            # 1 0 0
            if i == N - 1:
                nu = (1, 0, 0)
                beta = names_to_index[f"Fe_1_{j+1}"]
            else:
                nu = (0, 0, 0)
                beta = names_to_index[f"Fe_{i+2}_{j+1}"]

            parameter = from_iso(iso=J) + from_dmi(dmi=[D, 0, 0])
            spinham.add_22(alpha=alpha, beta=beta, nu=nu, parameter=parameter)

            # 0 1 0
            if j == N - 1:
                nu = (0, 1, 0)
                beta = names_to_index[f"Fe_{i+1}_1"]
            else:
                nu = (0, 0, 0)
                beta = names_to_index[f"Fe_{i+1}_{j+2}"]
            parameter = from_iso(iso=J) + from_dmi(dmi=[0, D, 0])
            spinham.add_22(alpha=alpha, beta=beta, nu=nu, parameter=parameter)

    spinham.add_magnetic_field(h=[0, 0, J / 5 / BOHR_MAGNETON / 2])

    return spinham


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
