import warnings
from abc import ABC, abstractmethod
from typing import Callable, Union

import numpy as np

from ttfemesh.utils.array import ensure_1d


class Curve(ABC):
    """
    Abstract base class for a curve in the domain.
    Defines the interface for all curve implementations.
    """

    def get_start(self) -> np.ndarray:
        """Get the start point of the curve."""
        return self.evaluate(-1.0)[0]

    def get_end(self) -> np.ndarray:
        """Get the end point of the curve."""
        return self.evaluate(1.0)[0]

    def __call__(self, *args, **kwargs) -> np.ndarray:
        return self.evaluate(*args, **kwargs)

    def _validate(self, t: Union[np.ndarray, float], tol: float = 1e-6):
        """
        Ensure that parameter values are in the interval [-1, 1] within a specified tolerance.

        Args:
            t (np.ndarray): Array of parameter values to validate.
            tol (float): Tolerance for boundary checks.

        Raises:
            ValueError: If any parameter values are outside the interval [-1, 1] (with tolerance).
        """

        t_ = ensure_1d(t)

        if not np.all(-1 - tol <= t_) or not np.all(t_ <= 1 + tol):
            warnings.warn(
                f"Parameter values are not in the interval [-1, 1]"
                f" within tolerance {tol}."
                f" May lead to unexpected behavior."
            )

    @abstractmethod
    def evaluate(self, t: Union[np.ndarray, float]) -> np.ndarray:  # pragma: no cover
        """
        Evaluate the curve at parameter values t.

        Args:
            t (Union[np.ndarray, float]): Array of or scalar parameter values in [-1, 1].

        Returns:
            np.ndarray: Array of shape (len(t), 2) with (x, y) coordinates.
        """
        pass

    @abstractmethod
    def tangent(self, t: Union[np.ndarray, float]) -> np.ndarray:  # pragma: no cover
        """
        Compute the tangent vector (not normalized) to the curve at parameter values t.

        Args:
            t (Union[np.ndarray, float]): Array of or scalar parameter values in [-1, 1].

        Returns:
            np.ndarray: Array of shape (len(t), 2) with tangent vectors.
        """
        pass

    def equals(self, other: "Curve", num_points: int = 100, tol: float = 1e-6) -> bool:
        """
        Check if two curves are approximately equal by sampling.

        Args:
            other (Curve): Another curve to compare.
            num_points (int): Number of points to sample along the curve.
            tol (float): Tolerance for point-wise comparison.

        Returns:
            bool: True if the curves are approximately equal, False otherwise.
        """
        reverse = False
        start = self.get_start()
        start_other = other.get_start()

        if not np.allclose(start, start_other, atol=tol):
            start_other = other.get_end()
            if not np.allclose(start, start_other, atol=tol):
                return False
            reverse = True

        ts = np.linspace(-1, 1, num_points)
        for t in ts:
            t_other = t if not reverse else -t
            if not np.allclose(self.evaluate(t), other.evaluate(t_other), atol=tol):
                return False
        return True


class Line2D(Curve):
    """
    A line segment in 2D space.

    Example:
        >>> from ttfemesh.domain import Line2D
        >>> from ttfemesh.utils import plot_curve_with_tangents
        >>> line = Line2D((0, 0), (1, 1))
        >>> print(line)
        >>> plot_curve_with_tangents(line, "Line")
    """

    def __init__(self, start: tuple[float, float], end: tuple[float, float]):
        """
        Initialize a line segment from `start` to `end`.

        Args:
            start (tuple): Coordinates of the start point (x, y).
            end (tuple): Coordinates of the end point (x, y).
        """
        self.start = np.array(start)
        self.end = np.array(end)

    def evaluate(self, t: Union[np.ndarray, float]) -> np.ndarray:
        t_ = ensure_1d(t)
        self._validate(t_)

        return np.outer((1 - t_) * 0.5, self.start) + np.outer((1 + t_) * 0.5, self.end)

    def tangent(self, t: Union[np.ndarray, float]) -> np.ndarray:
        t_ = ensure_1d(t)
        self._validate(t_)

        return np.tile(0.5 * (self.end - self.start), (len(t_), 1))

    def __repr__(self):
        return f"Line2D(start={tuple(self.start)}, end={tuple(self.end)})"


class CircularArc2D(Curve):
    """
    A circular arc in 2D space.

    Example:
        >>> import numpy as np
        >>> from ttfemesh.domain import CircularArc2D
        >>> from ttfemesh.utils import plot_curve_with_tangents
        >>> circular_arc = CircularArc2D((0, 0), 1, np.pi/2., 0.5*np.pi)
        >>> print(circular_arc)
        >>> plot_curve_with_tangents(circular_arc, "Circular Arc")
    """

    def __init__(
        self,
        center: tuple[float, float],
        radius: float,
        start_angle: float = 0.0,
        angle_sweep: float = np.pi,
    ):
        """
        Initialize a circular arc defined by a center, radius, and angle sweep.

        Args:
            center (tuple): Coordinates of the center (x, y).
            radius (float): Radius of the half-circle.
            start_angle (float): Starting angle in radians. Default is 0.
            angle_sweep (float): Angle sweep in radians. Default is π.
        """
        self.center = np.array(center)
        self.radius = radius
        self.start_angle = start_angle
        self.angle_sweep = angle_sweep

    def evaluate(self, t: Union[np.ndarray, float]) -> np.ndarray:
        t_ = ensure_1d(t)
        self._validate(t_)

        angle = self.start_angle + 0.5 * (t_ + 1) * self.angle_sweep
        x = self.center[0] + self.radius * np.cos(angle)
        y = self.center[1] + self.radius * np.sin(angle)
        return np.stack((x, y), axis=-1)

    def tangent(self, t: Union[np.ndarray, float]) -> np.ndarray:
        t_ = ensure_1d(t)
        self._validate(t_)

        angle = self.start_angle + 0.5 * (t_ + 1) * self.angle_sweep
        mul_factor = 0.5 * self.angle_sweep * self.radius
        dx = -np.sin(angle) * mul_factor
        dy = np.cos(angle) * mul_factor
        tangent = np.stack((dx, dy), axis=-1)
        return tangent

    def __repr__(self):
        return (
            f"CircularArc2D(center={tuple(self.center)}, "
            f"radius={self.radius}, start_angle={self.start_angle}, "
            f"angle_sweep={self.angle_sweep})"
        )


class ParametricCurve2D(Curve):
    """
    A parametric curve in 2D space.

    Example:
        >>> from ttfemesh.domain import ParametricCurve2D
        >>> from ttfemesh.utils import plot_curve_with_tangents
        >>> parametric_curve = ParametricCurve2D(
        ...     lambda t: np.sin(t * np.pi),
        ...     lambda t: np.cos(t * np.pi)
        ... )
        >>> print(parametric_curve)
        >>> plot_curve_with_tangents(parametric_curve, "Parametric Curve")
    """

    def __init__(
        self, x_func: Callable[[np.ndarray], np.ndarray], y_func: Callable[[np.ndarray], np.ndarray]
    ):
        """
        Initialize a parametric curve defined by functions x(t) and y(t).
        Uses a finite difference approximation to compute the tangent.

        Args:
            x_func (Callable[[np.ndarray], np.ndarray]): Function x(t) where t is in [-1, 1].
            y_func (Callable[[np.ndarray], np.ndarray]): Function y(t) where t is in [-1, 1].
        """
        self.x_func = x_func
        self.y_func = y_func

    def evaluate(self, t: Union[np.ndarray, float]) -> np.ndarray:
        t_ = ensure_1d(t)
        self._validate(t_)

        x = self.x_func(t_)
        y = self.y_func(t_)
        return np.stack((x, y), axis=-1)

    def tangent(self, t: Union[np.ndarray, float]) -> np.ndarray:
        """
        Compute the tangent vector using a finite difference approximation.

        Args:
            t (Union[np.ndarray, float]): Array of or scalar parameter values in [-1, 1].

        Returns:
            np.ndarray: Array of shape (len(t), 2) with tangent.
        """
        t_ = ensure_1d(t)
        self._validate(t_)

        dt = 1e-5
        dx = (self.x_func(t_ + dt) - self.x_func(t_)) / dt
        dy = (self.y_func(t_ + dt) - self.y_func(t_)) / dt
        tangent = np.stack((dx, dy), axis=-1)
        return tangent

    def __repr__(self):
        return f"ParametricCurve2D(x_func={self.x_func}, y_func={self.y_func})"
