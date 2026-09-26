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

pairs = [(0,0),(.03,2.5),(.10,9),(.18,17.5),(.28,29.7),(.32,18),(.38,12),(.45,10.5),(.72,9.2),(1.25,8.7),(1.6,8.2),(1.64,0)];

def thrust_at(t):
    # Step 1: outside the burn?
    if t < pairs[0][0] or t > pairs[-1][0]:
        return 0

    # Step 2: find the pair t sits between
    for i in range(len(pairs) - 1):
        t_left, f_left = pairs[i]
        t_right, f_right = pairs[i + 1]

        if t_left <= t <= t_right:
            # Step 3: interpolate
            fraction = (t - t_left) / (t_right - t_left)
            change = f_right - f_left
            return f_left + fraction * change
for test_t in [-0.1, 0.0, 0.28, 0.30, 1.00, 1.64, 2.0]:
    print(test_t, thrust_at(test_t))


plt.plot(times, altitudes)
plt.xlabel("Time (s)")
plt.ylabel("Altitude (m)")
plt.show()