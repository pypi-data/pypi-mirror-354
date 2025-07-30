# Dark from Light 🌌

*"Unveiling the invisible universe, one galaxy at a time"*
A Python package that classifies galaxies into groups and estimates dark matter halo masses using Random Forest regressors trained on large volume cosmological simulations: [EAGLE](https://icc.dur.ac.uk/Eagle/) and [IllustrisTNG](https://www.tng-project.org/).

## Features

- **Galaxy Group Classification**: Automatically allocate galaxies into groups
- **Dark Matter Mass Estimation**: Predict halo masses from observable properties (photometric/spectroscopic stellar mass estimates, sky coordinates and redhsift)
- **Pre-trained Models**: Ready-to-use Random Forest regressors trained on simulation data (mapping between electromagnetic observables and halo properties)
- **Multiple Halo Mass - Stellar Mass Relations**: Choice among models trained on EAGLE, IllustrisTNG and hybrid approach (mean prediction between the two simulations)

## Quick Start

```python
from dark_from_light import allocate_galaxy_groups, HybridRegressionModel

# Classify galaxies into groups
allocate_galaxy_groups(galaxy_data)

# Estimate dark matter halo masses
model = HybridRegressionModel()
halo_mass = model.predict_group(group_total_stellar_mass)
```

*Turn stellar observations into cosmic insights.*