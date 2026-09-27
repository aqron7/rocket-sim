import matplotlib.pyplot as plt

# Constants
m_loaded = .080
g = 9.81
dt = 0.001
sim_time = 50

# Starting state
t = 0.0
v = 0.0
h = 0.0

# History
times = []
velocities = []
altitudes = []
launched = False



from pathlib import Path
motor_file = Path(__file__).parent / "Estes_D12.eng"
    
pairs = [(0.0, 0.0)]
header_done = False

with open(motor_file) as file:
    for line in file:
        line = line.strip()

        if line == "" or line.startswith(";"):
            continue

        parts = line.split()

        if header_done == False:
            m_prop = float(parts[4])
            header_done = True
        else:
            pairs.append((float(parts[0]), float(parts[1])))

print("Propellant mass:", m_prop)

dry_mass = m_loaded - m_prop

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


I_total = 0.0
t_int = 0.0
I_burned = 0.0
while t_int <= pairs[-1][0]:
    I_total = I_total + thrust_at(t_int) * dt
    t_int = t_int + dt

print("Total impulse:", I_total)

printed = False
while t < sim_time:

    # Calculate net force
    thrust = thrust_at(t)
    mass = dry_mass + m_prop * (1 - I_burned / I_total)

    F_net = thrust - mass * g

    I_burned = I_burned + thrust * dt
    
    if thrust > mass * g:
        launched = True

    if launched == False:
        a = 0
    else: a = F_net/mass

    if launched == True and h < 0:
        break

            
    v = v + a * dt
    h = h + v *dt
    t = t + dt
    if t >= pairs[-1][0] and printed == False:
            printed = True
            print("Burnout:", v, h)

    times.append(t)
    velocities.append(v)
    altitudes.append(h)

print("Maximum altitude:", max(altitudes))
print("Maximum velocity:", max(velocities))
print("mass at burnout:", mass)
print("Impulse burned:", I_burned)
plt.plot(times, altitudes)
plt.xlabel("Time (s)")
plt.ylabel("Altitude (m)")
plt.show()