from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple

import numpy as np

from ttfemesh.basis import BilinearBasis, TensorProductBasis
from ttfemesh.domain import Domain, Quad
from ttfemesh.domain.subdomain_connection import CurveConnection2D, VertexConnection2D
from ttfemesh.mesh.mesh_utils import side_concatenation_tt, vertex_concatenation_tt
from ttfemesh.mesh.subdomain_mesh import QuadMesh, SubdomainMesh, SubdomainMesh2D
from ttfemesh.quadrature.quadrature import QuadratureRule
from ttfemesh.tt_tools.tensor_cross import TTCrossConfig
from ttfemesh.types import BoundarySide2D, BoundaryVertex2D, TensorTrain


class DomainMesh(ABC):
    """
    DomainMesh base class that ties together the domain, subdomain meshes, and basis functions.
    It provides an interface for the element jacobians of the subdomains,
    the element to global index maps, the boundary masks and the concatenation maps.
    """

    def __init__(
        self,
        domain: Domain,
        quadrature_rule: QuadratureRule,
        mesh_size_exponent: int,
        basis: TensorProductBasis,
        tt_cross_config: Optional[TTCrossConfig] = None,
    ):
        """
        Initialize a DomainMesh.

        Args:
            domain (Domain): The domain containing subdomains and their connections.
            quadrature_rule (QuadratureRule): Quadrature rule for integration.
            mesh_size_exponent (int): Discretization size exponent.
            basis (TensorProductBasis): The basis functions for the domain.
            cross_config (Optional[TTCrossConfig]):
                Optional configuration for tensor cross approximation.
                If None, the default configuration is used.
        """

        self.quadrature_rule = quadrature_rule
        self.mesh_size_exponent = mesh_size_exponent
        self.domain = domain
        self.basis = basis
        self._tt_cross_config = tt_cross_config
        self.subdomain_meshes = self._create_subdomain_meshes()

    @abstractmethod
    def _create_subdomain_meshes(self):  # pragma: no cover
        num_subdomains = self.domain.num_subdomains
        subdomain_meshes = []
        for i in range(num_subdomains):
            subdomain = self.domain.get_subdomain(i)
            mesh_size_exponent = self.mesh_size_exponent
            quadrature_rule = self.quadrature_rule
            tt_cross_config = self._tt_cross_config
            subdomain_mesh = SubdomainMesh(
                subdomain, quadrature_rule, mesh_size_exponent, tt_cross_config
            )
            subdomain_meshes.append(subdomain_mesh)

        return subdomain_meshes

    def get_subdomain_mesh(self, subdomain_index: int) -> SubdomainMesh:  # noqa
        """
        Get the SubdomainMesh for a subdomain.

        Args:
            subdomain_index (int): The index of the subdomain.

        Returns:
            SubdomainMesh: The SubdomainMesh for the subdomain.

        Raises:
            ValueError: If the subdomain index is invalid.
        """
        self._validate_subdomain_index(subdomain_index)
        return self.subdomain_meshes[subdomain_index]

    def get_element2global_index_map(self) -> np.ndarray:  # noqa
        """
        Get the TT-representation of transformations mapping from element index to global basis
        function index for all reference basis functions on a reference element in a subdomain.
        This map depends on the type of basis functions used and
        the discretization size of the subdomain.

        Args:
            subdomain_index (int): The index of the subdomain.

        Returns:
            np.ndarray: A matrix of TT-representations, i.e.,
                each element of the matrix is a TT-vector.
                Indexing of the matrix corresponds to the
                reference basis function indexing.
                For example, for a bilinear basis in 2D, the indexing is:
                (i, j) where i and j are the indices of the basis functions in x and y direction
                Specifically, (0, 0), (1, 0), (0, 1) and (1, 1),
                representing the four basis functions
                corresponding to the four vertices of the reference element:
                lower left, lower right, upper right and upper left, respectively.
                See also the documentation for the chosen Basis class.
        """
        mesh_size_exponent = self.mesh_size_exponent
        ttmaps = self.basis.get_all_element2global_ttmaps(mesh_size_exponent)

        return ttmaps

    def get_dirichlet_masks(self) -> Dict[int, TensorTrain]:  # noqa
        """
        Get the dirichlet boundary masks.

        Returns:
            Dict[TensorTrain]: A dictionary where the keys are subdomain indices,
                and the values are TT-representations of the boundary masks.
        """

        boundary_condition = self.domain.boundary_condition
        if boundary_condition is None:
            print("No boundary condition specified.")
            return None

        grouped = boundary_condition.group_by_subdomain()
        boundary_masks = {}
        for subdomain_index, curve_indices in grouped.items():
            sides = [BoundarySide2D(i) for i in curve_indices]
            boundary_mask = self.basis.get_dirichlet_mask(self.mesh_size_exponent, *sides)
            boundary_masks[subdomain_index] = boundary_mask

        return boundary_masks

    @abstractmethod  # noqa # pragma: no cover
    def get_concatenation_maps(self) -> Dict[Tuple[int, int], TensorTrain]:
        """
        Get the TT-representations of the concatenation maps for all pairs of connected subdomains.

        Returns:
            Dict[Tuple[int, int], TensorTrain]:
                A dictionary where the keys are pairs of subdomain indices,
                and the values are TT-representations of the concatenation maps.
        """
        pass

    def _validate_subdomain_index(self, subdomain_index: int):
        if subdomain_index < 0 or subdomain_index >= self.domain.num_subdomains:
            raise ValueError(
                f"Invalid subdomain index: {subdomain_index}. "
                f"Valid indices are in the range [0, {self.domain.num_subdomains})."
            )

    def __repr__(self) -> str:
        return (
            f"DomainMesh(domain={self.domain}, "
            f"mesh_size_exponent={self.mesh_size_exponent}, "
            f"quadrature_rule={self.quadrature_rule}, "
            f"basis={self.basis})"
        )


class DomainMesh2D(DomainMesh):
    """Mesh for 2D domains. This is essentially a factory for SubdomainMesh2D objects."""

    def _create_subdomain_meshes(self):
        num_subdomains = self.domain.num_subdomains
        subdomain_meshes = []
        for i in range(num_subdomains):
            subdomain = self.domain.get_subdomain(i)
            mesh_size_exponent = self.mesh_size_exponent
            quadrature_rule = self.quadrature_rule
            tt_cross_config = self._tt_cross_config
            if isinstance(subdomain, Quad):
                subdomain_mesh = QuadMesh(
                    quad=subdomain,
                    quadrature_rule=quadrature_rule,
                    mesh_size_exponent=mesh_size_exponent,
                    tt_cross_config=tt_cross_config,
                )
            else:
                subdomain_mesh = SubdomainMesh2D(
                    subdomain=subdomain,
                    quadrature_rule=quadrature_rule,
                    mesh_size_exponent=mesh_size_exponent,
                    tt_cross_config=tt_cross_config,
                )
            subdomain_meshes.append(subdomain_mesh)

        return subdomain_meshes

    def __repr__(self) -> str:
        return (
            f"DomainMesh2D(domain={self.domain}, "
            f"mesh_size_exponent={self.mesh_size_exponent}, "
            f"quadrature_rule={self.quadrature_rule}, "
            f"basis={self.basis})"
        )


class DomainBilinearMesh2D(DomainMesh2D):
    """
    Mesh for 2D domains with bilinear basis functions.
    This implementation of the concatenation maps works only for bilinear basis functions.

    Example:
    >>> from ttfemesh.domain import RectangleFactory, CurveConnection2D, VertexConnection2D
    >>> from ttfemesh.domain import DirichletBoundary2D, Domain2D
    >>> from ttfemesh.quadrature import GaussLegendre2D
    >>> from ttfemesh.mesh import DomainBilinearMesh2D

    >>> lower_left = (0, 0)
    >>> upper_right = (2, 1)
    >>> rectangle1 = RectangleFactory.create(lower_left, upper_right)

    >>> lower_left = (2, 0)
    >>> upper_right = (3, 1)
    >>> rectangle2 = RectangleFactory.create(lower_left, upper_right)

    >>> lower_left = (-2, 1)
    >>> upper_right = (0, 2)
    >>> rectangle3 = RectangleFactory.create(lower_left, upper_right)

    >>> domain_idxs = [0, 1]
    >>> curve_idxs = [1, 3]
    >>> edge = CurveConnection2D(domain_idxs, curve_idxs)

    >>> vertex_idxs = [(0, 3, "start"), (2, 0, "end")]
    >>> vertex = VertexConnection2D(vertex_idxs)

    >>> bc = DirichletBoundary2D([(1, 1), (2, 3)])

    >>> domain = Domain2D([rectangle1, rectangle2, rectangle3], [edge, vertex], bc)

    >>> quadrature_rule = GaussLegendre2D()
    >>> mesh_size_exponent = 3
    >>> domain_mesh = DomainBilinearMesh2D(domain, quadrature_rule, mesh_size_exponent)
    >>> print(domain_mesh)
    """

    def __init__(
        self,
        domain: Domain,
        quadrature_rule: QuadratureRule,
        mesh_size_exponent: int,
        tt_cross_config: Optional[TTCrossConfig] = None,
    ):
        basis = BilinearBasis()
        super().__init__(domain, quadrature_rule, mesh_size_exponent, basis, tt_cross_config)

    def get_concatenation_maps(  # noqa
        self,
    ) -> Dict[Tuple[int, int], Tuple[TensorTrain, TensorTrain, TensorTrain]]:
        """
        Get the TT-representations of the concatenation maps for all pairs of connected subdomains.
        See Section 5 of arXiv:1802.02839 for details.
        Pmp describes which nodes in the left domain are connected
        to which nodes in the right domain,
        Pmm describes which nodes in the left domain are to be connected,
        Ppp describes which nodes in the right domain are to be connected.

        Returns:
            Dict[Tuple[int, int], Tuple[TensorTrain, TensorTrain, TensorTrain]]:
                A dictionary where the keys are pairs of subdomain indices,
                and the values are tuples TT-representations of the connectivity maps.

        Raises:
            ValueError: If the connection type is not supported.
        """

        connections = self.domain.get_connections()
        concatenation_maps = {}
        for connection in connections:
            if isinstance(connection, VertexConnection2D):
                for (
                    (subdidx1, subdidx2),
                    (curveidx1, curveidx2),
                    (pos1, pos2),
                ) in connection.get_connection_pairs():

                    offset1 = 0 if pos1 == "start" else 1
                    vertex_idx1 = (curveidx1 + offset1) % 4

                    offset2 = 0 if pos2 == "start" else 1
                    vertex_idx2 = (curveidx2 + offset2) % 4

                    vertex1 = BoundaryVertex2D(vertex_idx1)
                    vertex2 = BoundaryVertex2D(vertex_idx2)

                    tt_connectivity = vertex_concatenation_tt(
                        vertex1, vertex2, self.mesh_size_exponent
                    )
                    concatenation_maps[(subdidx1, subdidx2)] = tt_connectivity

            elif isinstance(connection, CurveConnection2D):
                subdidx1, subdidx2 = connection.subdomains_indices
                curveidx1, curveidx2 = connection.curve_indices
                side1 = BoundarySide2D(curveidx1)
                side2 = BoundarySide2D(curveidx2)
                tt_connectivity = side_concatenation_tt(side1, side2, self.mesh_size_exponent)
                concatenation_maps[(subdidx1, subdidx2)] = tt_connectivity

            else:
                raise ValueError(f"Unsupported connection type: {type(connection)}.")

        return concatenation_maps

    def __repr__(self):
        return (
            f"DomainBilinearMesh2D(domain={self.domain}, "
            f"mesh_size_exponent={self.mesh_size_exponent}, "
            f"quadrature_rule={self.quadrature_rule}, "
            f"basis={self.basis})"
        )
