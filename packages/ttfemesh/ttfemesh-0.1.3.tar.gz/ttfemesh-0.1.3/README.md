# TTFEMesh

[![PyPI](https://img.shields.io/pypi/v/ttfemesh.svg)](https://pypi.org/project/ttfemesh/)
[![Documentation Status](https://readthedocs.org/projects/tt-femesh/badge/?version=latest)](https://tt-femesh.readthedocs.io/en/latest/?badge=latest)
[![Tests](https://github.com/MazenAli/TT-FEMesh/actions/workflows/ci.yml/badge.svg)](https://github.com/MazenAli/TT-FEMesh/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/MazenAli/TT-FEMesh/branch/main/graph/badge.svg)](https://codecov.io/gh/MazenAli/TT-FEMesh)

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/downloads/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/downloads/)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/downloads/)

TTFEMesh is a Python library for generating tensor train representations of finite element meshes. It provides a comprehensive toolkit for creating domains, generating meshes, and computing tensorized Jacobians, Dirichlet masks, and concatenation maps, all of which are essential for solving partial differential equations using tensor train decompositions.

## Features

- Domain creation and manipulation
- Finite element mesh generation
- Tensor train representation of mesh components
- Computation of tensorized Jacobians
- Dirichlet boundary condition handling
- Concatenation map generation
- Integration with the `torchtt` package for TT decompositions
- Support for 2D domains and meshes
- Flexible and extensible architecture

## Installation

### Platform Support

TTFEMesh is currently only supported on Linux systems due to dependencies on the `torchtt` package. For other platforms (macOS, Windows), we recommend using Docker.

### Linux Installation

1. Install system dependencies:
```bash
sudo apt-get update
sudo apt-get install -y libblas-dev liblapack-dev
```

2. Install the package:
```bash
pip install ttfemesh
```

## Quick Start

Here's a simple example to get you started:

```python
from ttfemesh.domain import RectangleFactory, CurveConnection2D, DirichletBoundary2D, Domain2D
from ttfemesh.quadrature import GaussLegendre2D
from ttfemesh.mesh import DomainBilinearMesh2D

# Create a domain with two rectangles
rectangle1 = RectangleFactory.create((0, 0), (2, 1))
rectangle2 = RectangleFactory.create((2, 0), (3, 1))

# Connect the rectangles
edge = CurveConnection2D([0, 1], [1, 3])

# Set boundary conditions
bc = DirichletBoundary2D([(0, 3), (1, 1)])

# Create the domain
domain = Domain2D([rectangle1, rectangle2], [edge], bc)

# Generate a mesh
order = 1
qrule = GaussLegendre2D(order)
mesh_size_exponent = 3
mesh = DomainBilinearMesh2D(domain, qrule, mesh_size_exponent)

# Get tensorized components
subdmesh = mesh.get_subdomain_mesh(0)
jac_tts = subdmesh.get_jacobian_tensor_trains()
jac_dets = subdmesh.get_jacobian_det_tensor_trains()
jac_invdets = subdmesh.get_jacobian_invdet_tensor_trains()

# Get element to global index map
element2global_map = mesh.get_element2global_index_map()

# Get Dirichlet masks and concatenation maps
masks = mesh.get_dirichlet_masks()
concat_maps = mesh.get_concatenation_maps()
```

## Documentation

For detailed documentation, including API reference and examples, visit our [documentation](https://tt-femesh.readthedocs.io/en/latest/).

## Requirements

- Python >= 3.10, < 3.13
- Linux operating system (or Docker)
- BLAS and LAPACK libraries (system dependencies)
- torchtt (for tensor train operations)
- Other dependencies listed in [`requirements.txt`](requirements.txt)

## Contributing

We welcome contributions! Please read our [Contributing Guide](https://github.com/MazenAli/TT-FEMesh/blob/main/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

TTFEMesh is licensed under the MIT License - see the [LICENSE](https://github.com/MazenAli/TT-FEMesh/blob/main/LICENSE) file for details.
