"""
matrix.py
Definition of the matrices that discretize the Hamiltonians in 1 and
2 dimensions.

Created on: 19-04-2017.
@author: eduardo
"""

import numpy as np
import scipy.sparse as sp


def A1D(numberPoints, potentialFunc, domainStart, domainLength):
    """
    Hamiltonian discretization in 1d without boundaries.

    Uses Explicit method.
    Input:
        Number of points to evaluate on (float)
        Potential function (vectorised function)
        Location where domain starts (float)
        Length of domain (float)
    Output:
        Matrix A (scipy sparse matrix)
    """
    h = domainLength/numberPoints   # dx

    x = np.linspace(domainStart, domainStart + domainLength, numberPoints-1)
    v = potentialFunc(x)

    a = np.ones(numberPoints-1)*(2+(h**2 * v))
    b = np.ones(numberPoints-2)*-1
    A = sp.diags(a, 0) + sp.diags(b, 1) + sp.diags(b, -1)

    # Periodic boundaries
    # A[0,-1] = -1
    # A[-1,0] = -1

    return (1./h**2) * A


def A1Dfull(numberPoints, potentialFunc, domainStart, domainLength):
    """
    Hamiltonian discretization in 1d with Dirichlet boundary conditions.

    Uses Explicit method to compute RHS of (A.68) in jos' book.
    Here we take hbar = 2m = 1.
    Input:
        Number of points to evaluate on (float)
        Potential function (vectorised function)
        Location where domain starts (float)
        Length of domain (float)
    Output:
        Matrix A, the discretised Hamiltonian (scipy sparse matrix)
    """
    h = domainLength/numberPoints  # dx

    x = np.linspace(domainStart, domainStart + domainLength, numberPoints+1)
    v = potentialFunc(x)

    a = np.ones(numberPoints+1)*(2+(h**2 * v))
    b = np.ones(numberPoints)*-1

    a[0] = h**2
    a[numberPoints] = h**2

    b[0] = 0
    b[numberPoints-1] = 0

    A = sp.diags(a, 0) + sp.diags(b, 1) + sp.diags(b, -1)
    return (1./h**2) * A


def A2D(numberPoints, potentialFunc, domainStart, domainLength):
    """
    Hamiltonian discretization in 2d without boundaries.

    Here we take hbar = 2m = 1.
    Input:
        Number of points to evaluate in each axis direction (float)
        Potential function (vectorised function)
        Location where domain starts (tuple)
        Length of domain (float)
    Output:
        Matrix A, the discretised Hamiltonian (scipy sparse matrix)
    """
    h = domainLength/numberPoints  # dx

    o = np.ones(numberPoints-1)
    x = np.linspace(domainStart[0], domainStart[0] + domainLength,
                    numberPoints-1)
    y = np.linspace(domainStart[1], domainStart[1] + domainLength,
                    numberPoints-1)
    x = np.kron(x, o)
    y = np.kron(o, y)
    v = potentialFunc(x, y)

    a = np.ones(numberPoints-1)*(2)
    b = np.ones(numberPoints-2)*(-1)

    Id = np.identity(numberPoints-1)

    A1d = sp.diags(a, 0) + sp.diags(b, 1) + sp.diags(b, -1)
    A = sp.kron(Id, A1d) + sp.kron(A1d, Id) + h**2 * sp.diags(v, 0)
    return (1./h**2) * A


def _Ih(numberPoints):
    """Return Identity matrix of given length with zeros on the extremes."""
    Id = np.ones(numberPoints+1)
    Id[0] = 0
    Id[numberPoints] = 0
    return sp.diags(Id)


def _Th(numberPoints, domainLength):
    """Create a section of the matrix A."""
    h = domainLength/numberPoints

    a = np.ones(numberPoints+1)*4.
    b = np.ones(numberPoints)*(-1)

    a[0] = h**2
    a[numberPoints] = h**2

    b[0] = 0
    b[numberPoints-1] = 0

    T = sp.diags(a, 0) + sp.diags(b, -1) + sp.diags(b, 1)
    return T


def A2Dfull(numberPoints, potentialFunc, domainStart, domainLength):
    """Hamiltonian discretization in 2D with dirichlet boundary conditions."""
    h = domainLength/numberPoints
    a = np.ones(numberPoints+1)
    b = np.ones(numberPoints)*(-1)
    b2 = np.zeros(numberPoints+1)
    a[0] = 0
    a[numberPoints] = 0
    b[0] = 0
    b[numberPoints-1] = 0
    b2[0] = 1
    b2[numberPoints] = 1

    Center1 = sp.diags(a, 0)
    Center2 = sp.diags(b, 1)
    Center3 = sp.diags(b, -1)
    Bounds = sp.diags(b2, 0)

    T = _Th(numberPoints, domainLength)
    Id = _Ih(numberPoints)
    I_N = (h**2)*sp.identity(numberPoints+1)

    o = np.ones(numberPoints+1)
    x = np.linspace(domainStart[0], domainStart[0] + domainLength,
                    numberPoints+1)
    y = np.linspace(domainStart[1], domainStart[1] + domainLength,
                    numberPoints+1)
    x = np.kron(x, o)
    y = np.kron(o, y)
    v = potentialFunc(x, y)

    A = sp.kron(Center1, T) + sp.kron(Center2, Id) + sp.kron(Center3, Id) \
      + sp.kron(Bounds, I_N) + (h**2 * sp.diags(v, 0))
    return (1./h**2)*A
