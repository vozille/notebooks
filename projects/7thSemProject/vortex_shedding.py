#!/usr/bin/python

# 2D flow around a cylinder


import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import cm
from numpy import *
from numpy.linalg import *

# Flow definition

maxIter = 150  # Total number of time iterations.
Re = 600.0  # Reynolds number.
nx = 520
ny = 180
ly = ny - 1.0
q = 9  # Lattice dimensions and populations.
cx = nx / 4
cy = ny / 2
r = ny / 9  # Coordinates of the cylinder.
vLat = 0.000000005  # Velocity in lattice units.
nulb = vLat * r / Re
omega = 1.0 / (3. * nulb + 0.5)  # Relaxation parameter.

# Lattice Constants
c = array([(x, y) for x in [0, -1, 1] for y in [0, -1, 1]])  # Lattice velocities.
t = 1. / 36. * ones(q)  # Lattice weights.
t[asarray([norm(ci) < 1.1 for ci in c])] = 1.0 / 9.0
t[0] = 4. / 9.
noslip = [c.tolist().index((-c[points]).tolist()) for points in range(q)]
i1 = arange(q)[asarray([ci[0] < 0 for ci in c])]  # Unknown on right wall.
i2 = arange(q)[asarray([ci[0] == 0 for ci in c])]  # Vertical middle.
i3 = arange(q)[asarray([ci[0] > 0 for ci in c])]  # Unknown on left wall.

dhleper = lambda finput: sum(finput, axis=0)  # Helper function for density computation.


def equilibrium(rho, u0):  # Equilibrium distribution function.
    cu = 3.0 * dot(c, u0.transpose(1, 0, 2))
    usqr = 3. / 2. * (u0[0] ** 2 + u0[1] ** 2)
    feq = zeros((q, nx, ny))
    for points in range(q):
        feq[points, :, :] = rho * t[points] * (1. + cu[points] + 0.5 * cu[points] ** 2 - usqr)
    return feq


# Setup: cylindrical obstacle and velocity inlet with perturbation
obstacle = fromfunction(lambda x, y: (x - cx) ** 2 + (y - cy) ** 2 < r ** 2, (nx, ny))
vel = fromfunction(lambda d, x, y: (1 - d) * vLat * (1.0 + 1e-4 * sin(y / ly * 2 * pi)), (2, nx, ny))
feq = equilibrium(1.0, vel)
finput = feq.copy()

fig = plt.figure()
vid = []

# Main time loop
for time in range(maxIter):
    finput[i1, -1, :] = finput[i1, -2, :]  # Right wall: outflow condition.
    rho = dhleper(finput)  # Calculate macroscopic density and velocity.
    u0 = dot(c.transpose(), finput.transpose((1, 0, 2))) / rho

    u0[:, 0, :] = vel[:, 0, :]  # Left wall: compute density from known populations.
    rho[0, :] = 1. / (1. - u0[0, 0, :]) * (dhleper(finput[i2, 0, :]) + 2. * dhleper(finput[i1, 0, :]))

    feq = equilibrium(rho, u0)  # Left wall: Zou/He boundary condition.
    finput[i3, 0, :] = finput[i1, 0, :] + feq[i3, 0, :] - finput[i1, 0, :]
    fout = finput - omega * (finput - feq)  # Collision step.
    for points in range(q):
        fout[points, obstacle] = finput[noslip[points], obstacle]
    for points in range(q):  # Streaming step.
        finput[points, :, :] = roll(roll(fout[points, :, :], c[points, 0], axis=0), c[points, 1], axis=1)

    if time % 10 == 0:  # Visualization
        # plt.clf()
        vid.append([plt.imshow(sqrt(u0[0] ** 2 + u0[1] ** 2).transpose(), cmap=cm.seismic)])
        plt.savefig("./images/vel." + str(time / 10).zfill(4) + ".png")
    if (time - 1) % 10 == 0:
        print("done " + str(time + 1))
im_ani = animation.ArtistAnimation(fig, vid, interval=40, repeat_delay=3000,
                                   blit=True)
plt.show()
