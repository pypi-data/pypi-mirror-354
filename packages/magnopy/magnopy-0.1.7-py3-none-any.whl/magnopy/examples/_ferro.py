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

from magnopy._parameters._p22 import from_iso
from magnopy._spinham._convention import Convention
from magnopy._spinham._hamiltonian import SpinHamiltonian

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def cubic_ferro_nn(
    a: float = 1,
    J_iso: float = 1,
    J_21=(0, 0, 0),
    S: float = 0.5,
    dimensions: int = 3,
) -> SpinHamiltonian:
    r"""
    Hamiltonian on the cubic lattice with non-zero exchange
    parameters between nearest-neighbors. One atom per unit cell.

    .. math::

        \mathcal{H}
        =
        \dfrac{1}{2}
        \sum_{\mu, \nu}
        J_{iso}
        \boldsymbol{S}_{\mu}
        \cdot
        \boldsymbol{S}_{\mu+\nu}
        +
        \sum_{\mu}
        \boldsymbol{S}_{\mu}
        \boldsymbol{J}_{21}
        \boldsymbol{S}_{\mu}

    where

    * :math:`\nu \in {(1,0,0), (-1,0,0)}` if ``dimensions == 1``.
    * :math:`\nu \in {(1,0,0), (-1,0,0), (0,1,0), (0,-1,0)}` if ``dimensions == 2``.
    * :math:`\nu \in {(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)}` if
      ``dimensions == 3``.

    Parameters
    ----------
    a : float, default 1.0
        Lattice parameter of the cubic lattice.
        The unit cell of the Hamiltonian is defined as

        .. code-block:: python

            [[a, 0, 0],
             [0, a, 0],
             [0, 0, a]]
    J_iso : float, default 1.0
        Isotropic exchange parameter for the pairs of the nearest-neighbor magnetic
        sites, given in energy units. Only magnitude is important.
    J_21 : (3, 3) or (3, ) |array-like|_, default (0, 0, 0)
        On-site quadratic anisotropy.
    S : float, default 0.5
        Spin value of the magnetic site.
    dimensions : int, default 3
        Either 1, 2 or 3. Dimensionality of the spin Hamiltonian.

    Returns
    -------
    spinham : :py:class:`.SpinHamiltonian`
        Spin Hamiltonian.
    """

    cell = a * np.eye(3, dtype=float)
    atoms = dict(
        names=["X"],
        species=["X"],
        spins=[S],
        g_factors=[2],
        positions=[[0, 0, 0]],
    )
    convention = Convention(
        spin_normalized=False,
        multiple_counting=True,
        c21=1,
        c22=0.5,
    )

    spinham = SpinHamiltonian(cell=cell, atoms=atoms, convention=convention)

    J_21 = np.array(J_21, dtype=float)
    if J_21.shape == (3,):
        J_21 = np.diag(J_21)

    spinham.add_21(alpha=0, parameter=J_21)

    J_iso = -from_iso(iso=abs(J_iso))

    spinham.add_22(alpha=0, beta=0, nu=(1, 0, 0), parameter=J_iso)

    if dimensions >= 2:
        spinham.add_22(alpha=0, beta=0, nu=(0, 1, 0), parameter=J_iso)

    if dimensions >= 3:
        spinham.add_22(alpha=0, beta=0, nu=(0, 0, 1), parameter=J_iso)

    return spinham


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
