from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict, List, Tuple

from ttfemesh.domain.subdomain import Subdomain2D


class BoundaryCondition(ABC):
    """
    Abstract base class for boundary conditions.
    """

    @abstractmethod
    def validate(self, *args, **kwargs):  # pragma: no cover
        """
        Validate the boundary condition with respect to the subdomains.
        """
        pass

    @abstractmethod
    def group_by_subdomain(self) -> Dict[int, List[int]]:  # pragma: no cover
        """
        Group the boundary conditions by subdomain.

        Returns:
            Dict[int, List[int]]: A dictionary where the keys are subdomain indices,
                                  and the values are lists of curve or face indices
                                  with the boundary condition.
        """
        pass


class DirichletBoundary2D(BoundaryCondition):
    """
    Implements a Dirichlet boundary condition for a 2D curve.
    Boundary values are implicitly assumed to be zero.

    Example:
    >>> from ttfemesh.domain import RectangleFactory, CurveConnection2D, VertexConnection2D
    >>> from ttfemesh.domain import DirichletBoundary2D, Domain2D
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
    >>> domain.plot()
    """

    def __init__(self, boundary: List[Tuple[int, int]]):
        """
        Initialize the Dirichlet boundary condition.

        Args:
            boundary (List[Tuple[int, int]]):
                List of subdomain and curve indices for the Dirichlet boundary.
        """
        self.boundary = boundary

    def validate(self, subdomains: List[Subdomain2D]):
        """
        Validate the boundary condition. Ensure that the specified curve exists.

        Args:
            subdomains (List[Subdomain]): List of subdomains in the domain.
        """
        for subdomain_idx, curve_idx in self.boundary:
            if subdomain_idx >= len(subdomains):
                raise ValueError(f"Subdomain index {subdomain_idx} out of range.")
            if curve_idx >= len(subdomains[subdomain_idx].curves):
                raise ValueError(
                    f"Curve index {curve_idx} out of range" f" for subdomain {subdomain_idx}."
                )

    def num_bcs(self) -> int:
        """
        Get the number of curves with imposed boundary conditions.

        Returns:
            int: Number of curves with boundary conditions.
        """
        return len(self.boundary)

    def group_by_subdomain(self) -> Dict[int, List[int]]:
        """
        Group the boundary conditions by subdomain.

        Returns:
            Dict[int, List[int]]: A dictionary where the keys are subdomain indices,
                                  and the values are lists of curve indices with
                                  the boundary condition.
        """
        grouped = defaultdict(list)
        for subdomain, curve in self.boundary:
            grouped[subdomain].append(curve)

        return dict(grouped)

    def __repr__(self):
        return f"DirichletBoundary2D(num_bcs={self.num_bcs()})"
