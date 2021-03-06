"""
Simulation of Rutherford scattering.

Created on: 28-04-2017.
@author: eduardo

"""
import numpy as np
import simulation as sm
import quantum_plots as qplots
import matplotlib.pyplot as plt


# Define the system parameters and domain
dim = 2
numberPoints = 100
dt = .001
dirichletBC = False
startPoint = [0, 0]
domainLength = 2

sign = -1
if dirichletBC:
    sign = 1
allPoints = numberPoints + sign


def scattering(x, y):
    '''1/r^2 Dispersive force around a defined center '''
    center = [0.5, 1.]
    alpha = 10
    r = np.linalg.norm([x - center[0], y - center[1]])
    return alpha/r


def scatteringVis(x, y):
    '''An exaggereted potential function to make it more visisble'''
    center = [0.5, 1.]
    r = np.linalg.norm([x - center[0], y - center[1]])
    if r < .05:
        return 1
    else:
        return 0


# Create the simulation for the system
sim = sm.Simulation(dim=dim, potentialFunc=scattering,
                    dirichletBC=dirichletBC, numberPoints=numberPoints,
                    startPoint=startPoint, domainLength=domainLength,
                    dt=dt)

# Create the initial wave function
sim.setPsiPulse(pulse="circular", energy=1000, vel=[1, 0], center=[.1, 1], width=.1)

# System evolution and Animation
ani = qplots.animation2D(sim, psi="norm",
                         potentialFunc=scatteringVis, save=False)
plt.show()
