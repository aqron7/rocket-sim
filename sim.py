import matplotlib.pyplot as plt

# Constants
mass = 1.0
thrust = 20.0
burn_time = 3.0
g = 9.81
dt = 0.1
sim_time = 30.0

# Starting state
t = 0.0
v = 0.0
h = 0.0

# History
times = []
velocities = []
altitudes = []

printed = False
while t < sim_time:

    # Calculate net force
    if t < burn_time:
        F_net = thrust-mass * g
    else:
        F_net = -mass * g
   

    a=F_net/mass
    v = v + a * dt
    h = h + v *dt
    t = t + dt
    if t >= burn_time and printed == False:
            printed = True
            print("Burnout:", v, h)

    times.append(t)
    velocities.append(v)
    altitudes.append(h)

plt.plot(times, altitudes)
plt.xlabel("Time (s)")
plt.ylabel("Altitude (m)")
plt.show()