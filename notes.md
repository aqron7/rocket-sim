# Development Notes

## Stage 1 — 1D point mass, constant thrust, no drag

**Setup:** 1 kg rocket, 20 N thrust, 3 s burn, g = 9.81 m/s^2, no drag.
Euler integration, sim runs to t = 30 s.

**Hand calculation (target):**
- F_net = T - mg = 20 - 9.81 = 10.19 N
- a = F_net / m = 10.19 m/s^2 (constant during burn)
- At burnout: v = a*t = 30.57 m/s, h = 0.5*a*t^2 = 45.86 m

**dt sweep:**

| dt | v (m/s) | v error | h (m) | h error |
|---|---|---|---|---|
| 0.1 | 30.5700 | +0.0003% | 47.383 | +3.3% |
| 0.01 | 30.6719 | +0.33% | 46.315 | +0.98% |
| 0.001 | 30.5802 | +0.033% | 45.901 | +0.089% |

**Altitude error behaves as expected.** Shrinking dt by 10x reduces the
error by roughly 10x, which is first-order convergence and is the
expected behavior for Euler's method. The error is always positive
because the loop updates velocity before altitude, then uses the new
(higher) velocity to advance altitude across the entire timestep. The
rocket was actually slower than that for most of the step, so distance
is overestimated on every iteration and the bias accumulates.

**Velocity error does not follow that pattern, and the reason matters.**
Velocity integration has no approximation error in this problem at all.
Acceleration is genuinely constant during the burn, so v = v + a*dt is
exact regardless of step size. The only velocity error comes from a
bookkeeping issue: the while condition is checked before t is
incremented, so the sim takes one extra step past burn_time and applies
thrust slightly too long.

At dt = 0.1, 3.0 divides evenly into 30 steps, so t lands exactly on
burn_time and the overshoot does not occur. At dt = 0.01 and 0.001,
floating point accumulation means t never lands exactly on 3.0, so the
extra step happens.

This is worth recording because the dt = 0.1 result looks like the most
accurate run in the sweep. It is not. It is right for a reason that has
nothing to do with integration quality, and running only that case would
have led to the wrong conclusion about the integrator.

**Takeaway:** an accurate number is not evidence of a correct model. The
two error sources here are independent and scale differently, so they
have to be diagnosed separately rather than read off a single result.

**Assumptions in this model:**
- Constant mass (no propellant depletion)
- Constant thrust (no real thrust curve)
- No aerodynamic drag
- Constant g (no variation with altitude)
- 1D translation only, no rotation or angle of attack
- Flat, non-rotating Earth
- No ground: altitude continues negative past impact

**Known issues to fix in a later stage:**
- Loop takes one step past burn_time
- No termination condition at h = 0

**Next:** Stage 2 adds a real motor thrust curve and mass depletion.