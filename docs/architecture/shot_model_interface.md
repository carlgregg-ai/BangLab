# Shot-model boundary

Conceptual boundary only for v0.1:

`FireEvent -> ShotModel -> evaluable ShotState / encounter field -> consumers`

Track E implements an Eulerian encounter field. Consumers depend on documented outputs, not internal equations. Do not create a framework/plugin system yet.

A future model may use empirical longitudinal data, stochastic pellets, DEM, CFD-derived coefficients or another validated representation without forcing clay/visualisation/trainer code to adopt Track E internals.
