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


R"""
Convention of spin Hamiltonian
"""

import warnings

from magnopy._spinham._hamiltonian import SpinHamiltonian

# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def make_supercell(spinham: SpinHamiltonian, supercell):
    r"""
    Creates a Hamiltonian on the supercell of the given one.

    Parameters
    ----------
    spinham : :py:class:`.SpinHamiltonian`
        Original spin Hamiltonian. ``spinham.cell`` is interpreted as the original
        unit cell.
    supercell : (3, ) tuple or list of int
        Repetitions of the unit cell (``spinham.cell``) along each lattice
        vector that defined the unit cell. If :math:`(i, j, k)` is given, then the
        supercell is formally defined as
        :math:`(i\cdot\boldsymbol{a}_1, j\cdot\boldsymbol{a}_2, k\cdot\boldsymbol{a}_3)`,
        where :math:`(\boldsymbol{a}_1, \boldsymbol{a}_2, \boldsymbol{a}_3)` is the
        original cell (``spinham.cell``).

    Returns
    -------
    spinham : :py:class:`.SpinHamiltonian`
        Spin Hamiltonian that is defined on a ``supercell`` and has the same parameters
        as the given ``spinham``.
    """

    warnings.warn(
        "Creation of supercell is untested, use at your own risk.", UserWarning
    )

    if supercell[0] < 1 or supercell[1] < 1 or supercell[2] < 1:
        raise ValueError(
            f"Supercell repetitions should be larger or equal to 1, got {supercell}"
        )

    new_cell = [supercell[i] * spinham.cell[i] for i in range(3)]

    new_atoms = {}

    for key in spinham.atoms:
        new_atoms[key] = []

    for k in range(supercell[2]):
        for j in range(supercell[1]):
            for i in range(supercell[0]):
                for atom_index in range(len(spinham.atoms.names)):
                    for key in spinham.atoms:
                        if key == "positions":
                            position = spinham.atoms.positions[atom_index]
                            new_position = [
                                (position[0] + i) / supercell[0],
                                (position[1] + j) / supercell[1],
                                (position[2] + k) / supercell[2],
                            ]
                            new_atoms["positions"].append(new_position)
                        elif key == "names":
                            new_atoms["names"].append(
                                f"{spinham.atoms.names[atom_index]}_{i}_{j}_{k}"
                            )
                        else:
                            new_atoms[key].append(spinham.atoms[key][atom_index])

    new_spinham = SpinHamiltonian(
        cell=new_cell, atoms=new_atoms, convention=spinham.convention
    )

    def get_new_indices(alpha, nu, ijk):
        nu = [nu[index] + ijk[index] for index in range(3)]

        i, j, k = [nu[index] % supercell[index] for index in range(3)]

        nu = [nu[index] // supercell[index] for index in range(3)]

        alpha = alpha + (i + j * supercell[0] + k * supercell[1] * supercell[0]) * len(
            spinham.atoms.names
        )

        return alpha, tuple(nu)

    for k in range(supercell[2]):
        for j in range(supercell[1]):
            for i in range(supercell[0]):
                # One spin
                for alpha, parameter in spinham._1:
                    alpha, _ = get_new_indices(alpha=alpha, nu=(0, 0, 0), ijk=(i, j, k))

                    new_spinham.add_1(alpha=alpha, parameter=parameter)

                # Two spins
                for alpha, parameter in spinham._21:
                    alpha, _ = get_new_indices(alpha=alpha, nu=(0, 0, 0), ijk=(i, j, k))

                    new_spinham.add_21(alpha=alpha, parameter=parameter)

                for alpha, beta, nu, parameter in spinham._22:
                    alpha, _ = get_new_indices(alpha=alpha, nu=(0, 0, 0), ijk=(i, j, k))
                    beta, nu = get_new_indices(alpha=beta, nu=nu, ijk=(i, j, k))

                    new_spinham.add_22(
                        alpha=alpha, beta=beta, nu=nu, parameter=parameter, replace=True
                    )

                # Three spins
                for alpha, parameter in spinham._31:
                    alpha, _ = get_new_indices(alpha=alpha, nu=(0, 0, 0), ijk=(i, j, k))

                    new_spinham.add_31(alpha=alpha, parameter=parameter)

                for alpha, beta, nu, parameter in spinham._32:
                    alpha, _ = get_new_indices(alpha=alpha, nu=(0, 0, 0), ijk=(i, j, k))
                    beta, nu = get_new_indices(alpha=beta, nu=nu, ijk=(i, j, k))

                    new_spinham.add_32(
                        alpha=alpha, beta=beta, nu=nu, parameter=parameter, replace=True
                    )

                for alpha, beta, gamma, nu, _lambda, parameter in spinham._33:
                    alpha, _ = get_new_indices(alpha=alpha, nu=(0, 0, 0), ijk=(i, j, k))
                    beta, nu = get_new_indices(alpha=beta, nu=nu, ijk=(i, j, k))
                    gamma, _lambda = get_new_indices(
                        alpha=gamma, nu=_lambda, ijk=(i, j, k)
                    )

                    new_spinham.add_33(
                        alpha=alpha,
                        beta=beta,
                        gamma=gamma,
                        nu=nu,
                        _lambda=_lambda,
                        parameter=parameter,
                        replace=True,
                    )

                # Four spins
                for alpha, parameter in spinham._41:
                    alpha, _ = get_new_indices(alpha=alpha, nu=(0, 0, 0), ijk=(i, j, k))

                    new_spinham.add_41(alpha=alpha, parameter=parameter)

                for alpha, beta, nu, parameter in spinham._421:
                    alpha, _ = get_new_indices(alpha=alpha, nu=(0, 0, 0), ijk=(i, j, k))
                    beta, nu = get_new_indices(alpha=beta, nu=nu, ijk=(i, j, k))

                    new_spinham.add_421(
                        alpha=alpha, beta=beta, nu=nu, parameter=parameter, replace=True
                    )

                for alpha, beta, nu, parameter in spinham._422:
                    alpha, _ = get_new_indices(alpha=alpha, nu=(0, 0, 0), ijk=(i, j, k))
                    beta, nu = get_new_indices(alpha=beta, nu=nu, ijk=(i, j, k))

                    new_spinham.add_422(
                        alpha=alpha, beta=beta, nu=nu, parameter=parameter, replace=True
                    )

                for alpha, beta, gamma, nu, _lambda, parameter in spinham._43:
                    alpha, _ = get_new_indices(alpha=alpha, nu=(0, 0, 0), ijk=(i, j, k))
                    beta, nu = get_new_indices(alpha=beta, nu=nu, ijk=(i, j, k))
                    gamma, _lambda = get_new_indices(
                        alpha=gamma, nu=_lambda, ijk=(i, j, k)
                    )

                    new_spinham.add_43(
                        alpha=alpha,
                        beta=beta,
                        gamma=gamma,
                        nu=nu,
                        _lambda=_lambda,
                        parameter=parameter,
                        replace=True,
                    )

                for (
                    alpha,
                    beta,
                    gamma,
                    epsilon,
                    nu,
                    _lambda,
                    rho,
                    parameter,
                ) in spinham._44:
                    alpha, _ = get_new_indices(alpha=alpha, nu=(0, 0, 0), ijk=(i, j, k))
                    beta, nu = get_new_indices(alpha=beta, nu=nu, ijk=(i, j, k))
                    gamma, _lambda = get_new_indices(
                        alpha=gamma, nu=_lambda, ijk=(i, j, k)
                    )
                    epsilon, rho = get_new_indices(alpha=epsilon, nu=rho, ijk=(i, j, k))
                    new_spinham.add_44(
                        alpha=alpha,
                        beta=beta,
                        gamma=gamma,
                        epsilon=epsilon,
                        nu=nu,
                        _lambda=_lambda,
                        rho=rho,
                        parameter=parameter,
                        replace=True,
                    )

    return new_spinham


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
