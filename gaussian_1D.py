"""
A simple animation for the 1D case
with potential well.

Created on: 24-04-2017.
@author: eduardo
"""
import quantum_plots as qplots

import numpy as np
import simulation as sm
import matplotlib.pyplot as plt


# Define the system parameters and domain
dim = 1
numberPoints = 256
dt = .001
dirichletBC = False
startPoint = 0
domainLength = 15


def gaussian(x):
    '''A 1D Gaussian potential function'''
    mag = 200
    center = 4
    std = 1
    V = mag * np.exp(-(x-center)**2/(2*std**2))
    return V


# Create the simulation for the system
sim = sm.Simulation(dim=dim, potentialFunc=gaussian,
                    dirichletBC=dirichletBC, numberPoints=numberPoints,
                    startPoint=startPoint, domainLength=domainLength,
                    dt=dt)

# Create the initial wave function
sim.setPsiPulse(pulse="plane", energy=500, center=2)

# System evolution and Animation
ani = qplots.animation1D(sim, psi='real', V=gaussian)
plt.show()
