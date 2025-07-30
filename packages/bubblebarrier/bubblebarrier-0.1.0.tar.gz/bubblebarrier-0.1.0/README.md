# BubbleBarrier

[![PyPI version](https://badge.fury.io/py/bubblebarrier.svg)](https://badge.fury.io/py/bubblebarrier)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A Python package for calculating bubble barriers in cosmic reionization models. This package provides tools for modeling ionized bubbles and barrier functions used in studies of the epoch of reionization.

## Features

- **Bubble Model Calculations**: Compute bubble volume fractions and mass functions
- **Barrier Functions**: Calculate δ_v barriers for reionization modeling
- **Mass Function Integration**: Efficient numerical integration for halo mass functions
- **Parallel Processing**: Built-in support for parallel computation using joblib
- **Astrophysical Parameters**: Configurable escape fraction, ionizing photon production, and other physical parameters

## Installation

### From PyPI (recommended)

```bash
pip install bubblebarrier
```

### From Source

```bash
git clone https://github.com/SOYONAOC/BubbleBarrier.git
cd BubbleBarrier
pip install -e .
```

## Quick Start

```python
import numpy as np
from bubblebarrier import Bubble, Barrier

# Initialize bubble model
bubble = Bubble(zeta=30, b0=1.0, b1=1.0)

# Initialize barrier model
barrier = Barrier(
    fesc=0.2,      # Escape fraction
    qion=20000.0,  # Ionizing photons per baryon
    z_v=12.0,      # Redshift
    nrec=3,        # Recombination parameter
    xi=100.0       # X-ray heating efficiency
)

# Calculate bubble volume fraction
z = 10.0
mass = 1e16  # Solar masses
Q_bubble = bubble.Q_bubble(mass, z)

# Calculate ionizing photon number
Mv = 1e15
delta_R = 0.1
N_ion = barrier.Nion(Mv, delta_R)

print(f"Bubble volume fraction: {Q_bubble:.3e}")
print(f"Ionizing photon number: {N_ion:.3e}")
```

## Core Classes

### Bubble Class

The `Bubble` class handles bubble model calculations for reionization studies.

**Parameters:**
- `zeta` (float): Efficiency parameter (default: 40)
- `b0` (float): Bias parameter b₀ (default: 1.0)
- `b1` (float): Bias parameter b₁ (default: 1.0)

**Key Methods:**
- `Q_bubble(m, z)`: Calculate cumulative bubble volume fraction
- `MassFunc_Liner(m, z)`: Linear mass function with bias
- `B(m, z)`: Barrier function calculation

### Barrier Class

The `Barrier` class computes barrier heights for ionization balance.

**Parameters:**
- `fesc` (float): Escape fraction of ionizing photons (default: 0.2)
- `qion` (float): Ionizing photons per stellar baryon (default: 20000.0)
- `z_v` (float): Redshift of interest (default: 12.0)
- `nrec` (int): Recombination clumping factor (default: 3)
- `xi` (float): X-ray heating efficiency (default: 100.0)

**Key Methods:**
- `Nion(Mv, delta_R)`: Calculate ionizing photon production
- `Calcul_deltaVM(Mv)`: Compute barrier height δ_v
- `Calcul_deltaVM_Minihalo(Mv)`: Barrier calculation including minihalos

## Advanced Usage

### Parallel Computation

```python
# Calculate barriers for multiple halo masses in parallel
Mv_array = np.logspace(14, 17, 50)  # Range of halo masses
delta_v_results = barrier.Calcul_deltaVM_Parallel(Mv_array)
```

### Including Minihalo Effects

```python
# Calculate barriers including X-ray heating from minihalos
delta_v_minihalos = barrier.Calcul_deltaVM_Minihalo_Parallel(Mv_array)
```

### Custom Bubble Parameters

```python
# Create bubble model with custom parameters
custom_bubble = Bubble(zeta=50, b0=1.5, b1=0.8)

# Calculate mass function with linear bias
z = 8.0
masses = np.logspace(12, 18, 100)
mass_func = [custom_bubble.MassFunc_Liner(m, z) for m in masses]
```

## Physical Background

This package implements models for:

1. **Bubble Model**: Describes the topology of ionized regions during reionization
2. **Barrier Method**: Calculates the density threshold required for halo formation in ionized regions
3. **Mass Functions**: Modified halo mass functions accounting for ionization feedback
4. **Recombination**: Self-consistent treatment of recombination in ionized bubbles

The models are particularly useful for:
- 21cm signal predictions
- Reionization simulations
- Studying the connection between galaxies and ionized bubbles
- Modeling the impact of X-ray sources on reionization

## Dependencies

- `numpy >= 1.18.0`
- `scipy >= 1.5.0`
- `astropy >= 4.0`
- `matplotlib >= 3.0.0`
- `joblib >= 1.0.0`
- `massfunc` (custom cosmology package)

## Examples

See the `examples/` directory for Jupyter notebooks demonstrating:
- Basic barrier calculations
- Bubble volume evolution
- Comparison with analytical models
- Parameter sensitivity studies

## Citation

If you use this package in your research, please cite:

```bibtex
@misc{bubblebarrier2025,
  author = {Hajime Hinata},
  title = {BubbleBarrier: A Python package for reionization bubble modeling},
  year = {2025},
  url = {https://github.com/SOYONAOC/BubbleBarrier}
}
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- **Author**: Hajime Hinata
- **Email**: onmyojiflow@gmail.com
- **GitHub**: [SOYONAOC](https://github.com/SOYONAOC)

## Acknowledgments

- Based on the barrier method for reionization modeling
- Implements algorithms from modern reionization literature
- Thanks to the astrophysics community for theoretical foundations
