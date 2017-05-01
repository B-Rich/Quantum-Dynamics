"""
Simulation of the double slit experiment.

Created on: 28-04-2017.
@author: eduardo

"""
import numpy as np
import simulation as sm
import quantum_plots as qplots


# Define the system parameters
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

x = np.linspace(startPoint[0], startPoint[0] + domainLength, allPoints)
y = np.linspace(startPoint[1], startPoint[1] + domainLength,
                allPoints).reshape(-1, 1)


def doubleSlit(x, y):
    sS = .3   # Slit separation
    sW = .1   # Half slit width
    spX = .5  # X coordinate start
    spY = 1   # Y coordinate of center of slits
    if x > spX and x < spX+.05 and (y < spY-sS/2. or y > spY+sS/2.):
        return 50000
    if x > spX and x < spX+.05 and (y > spY-sS/2.+sW and y < spY+sS/2.-sW):
        return 50000
    else:
        return 0


# Create the simulation for the system
sim = sm.Simulation(dim=dim, potentialFunc=doubleSlit,
                    dirichletBC=dirichletBC, numberPoints=numberPoints,
                    startPoint=startPoint, domainLength=domainLength,
                    dt=dt)

# Create the initial wave function
sim.setPsiPulse(pulse="plane", energy=500, center=.1, width=.1)

ani = qplots.animation2D(sim, [x, y], allPoints, psi="norm",
                     potentialFunc=doubleSlit, save=False)
