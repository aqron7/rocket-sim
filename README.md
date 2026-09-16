# Rocket Trajectory Simulator

A flight simulator for high-powered rockets, built from scratch to learn
the physics rather than to use an existing tool.

## Goal

Predict a rocket's trajectory from first principles, then validate the
predictions against real flight data from the Rutgers Rocket Propulsion
Laboratory. The long-term aim is to extend this into a 6-DOF simulation
with thrust vector control and state estimation.

## Status

**Stage 1 — 1D point mass, constant thrust, no drag.**

Roadmap:
- [x] Stage 0: environment and repo setup
- [ ] Stage 1: 1D point mass, constant thrust, no drag
- [ ] Stage 2: real motor thrust curves and mass depletion
- [ ] Stage 3: aerodynamic drag
- [ ] Stage 4: validation against RPL flight data
- [ ] Stage 5+: 2D dynamics, gimbaled thrust, control, estimation

## Approach

Each stage adds one piece of physics at a time and is verified against
something independently checkable before moving on. Assumptions are
documented as they are made, since the accuracy of the model depends on
them more than on the code.

## Stack

Python, NumPy, Matplotlib. No simulation libraries.

## Notes

Development log, including what broke and why, is in `notes.md`.