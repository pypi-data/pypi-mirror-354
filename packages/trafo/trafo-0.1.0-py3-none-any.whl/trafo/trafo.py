"""
MIT License

Copyright 2024-2025 Mirko Kunze

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the “Software”), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from math import atan2, copysign, cos, pi, sin, sqrt
import random
from itertools import repeat
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import (
    cast,
    Iterable,
    List,
    Literal,
    NamedTuple,
    Optional,
    overload,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
)

# epsilon is chosen such that with floating point precision, the following holds:
# cos(EPS) == 1.0
# sin(EPS) == EPS
# sqrt(1.0 + EPS**2) == 1.0
# sqrt(1.0 - EPS**2) == 1.0
EPS = 7.4e-9
DEG = pi / 180.0
_inf = float("inf")


def norm(*sides: float) -> float:
    """Calculate the Euclidean norm of an n-dimensional vector."""
    m = max(abs(s) for s in sides)
    if m == 0:
        return 0.0
    return m * sqrt(sum((s / m) ** 2.0 for s in sides))


class Vector(NamedTuple):
    """An immutable 3D vector representing a point or a direction"""

    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    @staticmethod
    def zero() -> "Vector":
        """Create a zero vector while being extra explicit about it."""
        return Vector(0.0, 0.0, 0.0)

    @staticmethod
    def ex() -> "Vector":
        """Create a unit vector in x-direction."""
        return Vector(1.0, 0.0, 0.0)

    @staticmethod
    def ey() -> "Vector":
        """Create a unit vector in y-direction."""
        return Vector(0.0, 1.0, 0.0)

    @staticmethod
    def ez() -> "Vector":
        """Create a unit vector in z-direction."""
        return Vector(0.0, 0.0, 1.0)

    @staticmethod
    def rand_box(
        min: Sequence[float] = (0.0, 0.0, 0.0),
        max: Sequence[float] = (1.0, 1.0, 1.0),
        generator: random.Random = cast(random.Random, random),
    ) -> "Vector":
        """Create a random vector with uniform distribution within a cuboid."""
        return Vector(
            generator.uniform(min[0], max[0]),
            generator.uniform(min[1], max[1]),
            generator.uniform(min[2], max[2]),
        )

    @staticmethod
    def rand_sphere(
        radius: float = 1.0,
        center: Optional["Vector"] = None,
        fill: bool = False,
        generator: random.Random = cast(random.Random, random),
    ) -> "Vector":
        """Create a random vector with uniform distribution on or in a sphere."""
        v = Vector(generator.gauss(), generator.gauss(), generator.gauss()).normalized()
        if center is None:
            center = Vector.zero()
        if fill:
            v = v * generator.random() ** (1 / 3)
        return Vector(
            center[0] + radius * v[0],
            center[1] + radius * v[1],
            center[2] + radius * v[2],
        )

    def __eq__(self, other: object) -> bool:
        """Check equality with another vector; true if all elements are equal."""
        if isinstance(other, Vector):
            return self[:] == other[:]
        else:
            return NotImplemented

    def __ne__(self, other: object) -> bool:
        """Check inequality with another vector; true if any element is unequal."""
        return not self == other

    def __add__(self, other: "Vector") -> "Vector":  # type: ignore[override]
        """Add another vector element-wise (returns a new Vector).
        Note that this violates LSP for tuples which are expected to concatenate instead.
        """
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            return NotImplemented

    def __neg__(self) -> "Vector":
        """Return the negated vector (as a new Vector)."""
        return Vector(-self.x, -self.y, -self.z)

    def __sub__(self, other: "Vector") -> "Vector":
        """Subtract another vector (returns a new Vector)."""
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            return NotImplemented

    def __mul__(self, scalar: float) -> "Vector":  # type: ignore[override]
        """Multiply by a scalar element-wise (returns a new Vector).
        Note that this violates LSP for tuples which are expected to repeat instead."""
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
        else:
            return NotImplemented

    def __rmul__(self, scalar: float) -> "Vector":  # type: ignore[override]
        """Multiply by a scalar element-wise (returns a new Vector).
        Note that this violates LSP for tuples which are expected to repeat instead."""
        return self * scalar

    def __truediv__(self, scalar: float) -> "Vector":
        """Divide by a scalar element-wise (returns a new Vector)."""
        if isinstance(scalar, (int, float)):
            return Vector(self.x / scalar, self.y / scalar, self.z / scalar)
        else:
            return NotImplemented

    def dot(self, other: "Vector") -> float:
        """Calculate the dot product with another vector."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: "Vector") -> "Vector":
        """Calculate the cross product with another vector (returns a new Vector)."""
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def norm(self) -> float:
        """Calculate the Euclidean norm (length) of the vector."""
        return norm(*self)

    def length(self) -> float:
        """Calculate the length (Euclidean norm) of the vector."""
        return norm(*self)

    def normalized(self) -> "Vector":
        """Return a (new) normalized vector with the same direction.
        Raises when called on a zero vector."""
        x, y, z = self.x, self.y, self.z
        m = max(abs(x), abs(y), abs(z))
        if m == 0:
            raise ValueError("cannot normalize a zero vector")
        x, y, z = x / m, y / m, z / m
        norm = sqrt(x * x + y * y + z * z)
        return Vector(x / norm, y / norm, z / norm)

    def perp(self, other: Optional["Vector"] = None) -> "Vector":
        """Calculate a vector perpendicular to this vector.
        If other is given, the result is perpendicular to both.
        Raises when called on a zero vector or when the vectors are parallel."""
        if other is None:
            if abs(self.x) < abs(self.y) and abs(self.x) <= abs(self.z):
                other = Vector(1.0, 0.0, 0.0)
            elif abs(self.y) < abs(self.z):
                other = Vector(0.0, 1.0, 0.0)
            else:
                other = Vector(0.0, 0.0, 1.0)
        return self.cross(other).normalized()

    @staticmethod
    def make_basis(v1: "Vector", v2: "Vector") -> Tuple["Vector", "Vector", "Vector"]:
        """Create an orthonormal basis from two vectors.
        The direction of the first vector is preserved,
        the second is made perpendicular to the first,
        the third is perpendicular to the first two.
        Raises when called on a zero vector or when the vectors are parallel."""
        v1 = v1.normalized()
        v3 = v1.perp(v2)
        v2 = v3.perp(v1)
        return v1, v2, v3

    def distance_to(self, other: "Vector") -> float:
        """Calculate the Euclidean distance to another vector."""
        return (self - other).norm()

    def angle_to(self, other: "Vector") -> float:
        """Calculate the angle to another vector (in rad)."""
        v1 = self.normalized()
        v2 = other.normalized()
        cos_angle = v1.dot(v2)
        sin_angle = v1.cross(v2).norm()
        return atan2(sin_angle, cos_angle)

    def lerp(self, other: "Vector", f: float) -> "Vector":
        """Linearly interpolate between two vectors (returns a new Vector)."""
        return Vector(
            self.x + f * (other.x - self.x),
            self.y + f * (other.y - self.y),
            self.z + f * (other.z - self.z),
        )

    @staticmethod
    def mean(
        vectors: Iterable["Vector"], weights: Optional[Iterable[float]] = None
    ) -> "Vector":
        """Calculate the weighted mean of a sequence of vectors.
        Raises when called with an empty sequence or when the sum of weights is zero."""

        weights = weights or repeat(1.0)

        if (
            hasattr(vectors, "__len__")
            and hasattr(weights, "__len__")
            and vectors.__len__() != weights.__len__()
        ):
            raise ValueError("vectors and weights must have the same length")

        x, y, z = 0.0, 0.0, 0.0
        w_sum = 0.0

        for v, weight in zip(vectors, weights):
            x += v.x * weight
            y += v.y * weight
            z += v.z * weight
            w_sum += weight

        if w_sum == 0.0:
            raise ValueError(
                "cannot compute mean if sequence is empty or sum of weights is 0"
            )

        return Vector(x / w_sum, y / w_sum, z / w_sum)

    def __str__(self) -> str:
        """Return a string representation of the vector."""
        return f"(x={self.x}, y={self.y}, z={self.z})"

    def __format__(self, format_spec: str) -> str:
        """Return a formatted string representation of the vector.
        The format_spec is applied to each element."""
        fx = self.x.__format__(format_spec)
        fy = self.y.__format__(format_spec)
        fz = self.z.__format__(format_spec)
        return f"(x={fx}, y={fy}, z={fz})"

    def __repr__(self) -> str:
        """Return an eval-able string representation of the vector."""
        return f"Vector({self.x}, {self.y}, {self.z})"


_T = TypeVar("_T", bound="Rotation")


class Rotation:
    """An immutable 3D orientation or rotation"""

    # uses quaternion under the hood which is an implementation detail
    # that is not part of the public interface and might change in the future
    __slots__ = ("_x", "_y", "_z", "_w")
    _x: float
    _y: float
    _z: float
    _w: float

    def __setattr__(self, name: str, value: float) -> None:
        """Deleted, always raises."""
        raise AttributeError("Rotation is immutable")

    def __delattr__(self, name: str) -> None:
        """Deleted, always raises."""
        raise AttributeError("Rotation is immutable")

    def __new__(
        cls: Type[_T], *, x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 1.0
    ) -> _T:
        """Construct a rotation from quaternion components without normalization.
        Intended only for use in classmethods. Use from_quat instead."""
        instance = super().__new__(cls)
        object.__setattr__(instance, "_x", x)
        object.__setattr__(instance, "_y", y)
        object.__setattr__(instance, "_z", z)
        object.__setattr__(instance, "_w", w)
        return instance

    def __init__(self) -> None:
        """Create the identity rotation."""
        # we only allow creation of the identity rotation via standard constructor
        # x, y, z, w are implementation details and should only be set via from_quat from the outside
        pass

    @staticmethod
    def identity() -> "Rotation":
        """Create the identity rotation while being extra explicit about it."""
        return Rotation()

    @staticmethod
    def x(angle: float) -> "Rotation":
        """Create a rotation about the x-axis."""
        return Rotation.__new__(Rotation, x=sin(angle / 2.0), w=cos(angle / 2.0))

    @staticmethod
    def y(angle: float) -> "Rotation":
        """Create a rotation about the y-axis."""
        return Rotation.__new__(Rotation, y=sin(angle / 2.0), w=cos(angle / 2.0))

    @staticmethod
    def z(angle: float) -> "Rotation":
        """Create a rotation about the z-axis."""
        return Rotation.__new__(Rotation, z=sin(angle / 2.0), w=cos(angle / 2.0))

    @staticmethod
    def from_quat(
        *, x: float, y: float, z: float, w: float, tolerance: float = EPS
    ) -> "Rotation":
        """Create a rotation from quaternion components.
        Raises if the norm deviates from 1 beyond the specified tolerance
        or if all components are 0."""

        m = max(abs(x), abs(y), abs(z), abs(w))
        if m == 0:
            raise ValueError("cannot normalize a zero quaternion")
        x_, y_, z_, w_ = x / m, y / m, z / m, w / m
        norm_ = sqrt(x_ * x_ + y_ * y_ + z_ * z_ + w_ * w_)

        if abs(m * norm_ - 1.0) > tolerance:
            raise ValueError(
                f"quaternion is not normalized: (x={x}, y={y}, z={z}, w={w})"
            )

        return Rotation.__new__(
            Rotation, x=x_ / norm_, y=y_ / norm_, z=z_ / norm_, w=w_ / norm_
        )

    def as_quat(
        self, order: Literal["xyzw", "wxyz"]
    ) -> Tuple[float, float, float, float]:
        """Return the quaternion components in the specified order."""
        if order == "xyzw":
            return self._x, self._y, self._z, self._w
        elif order == "wxyz":
            return self._w, self._x, self._y, self._z
        else:
            raise ValueError("order must be either 'xyzw' or 'wxyz'")

    @staticmethod
    def from_axis_angle(axis: Vector, angle: float) -> "Rotation":
        """Create a rotation from an axis and an angle (in rad)."""
        axis = axis.normalized()
        half_angle = angle / 2.0
        sin_half_angle = sin(half_angle)
        return Rotation.__new__(
            Rotation,
            x=sin_half_angle * axis.x,
            y=sin_half_angle * axis.y,
            z=sin_half_angle * axis.z,
            w=cos(half_angle),
        )

    def as_axis_angle(self) -> Tuple[Vector, float]:
        """Return the axis and angle (in rad) of the rotation.
        The angle is in the range [0, pi).
        If the angle is 0, the axis is (1, 0, 0)."""
        x, y, z, w = self._x, self._y, self._z, self._w
        cos_half_angle = w
        sin_half_angle = norm(x, y, z)
        if sin_half_angle == 0.0:
            return Vector(1.0, 0.0, 0.0), 0.0
        angle = 2.0 * atan2(sin_half_angle, cos_half_angle)
        angle = angle % (2.0 * pi)
        if angle <= pi:
            return Vector(x, y, z).normalized(), angle
        else:
            return Vector(-x, -y, -z).normalized(), 2.0 * pi - angle

    @staticmethod
    def from_rotvec(rotvec: Vector) -> "Rotation":
        """Create a rotation from a rotation vector.
        A rotation vector is the axis of rotation
        scaled by the angle of rotation."""
        angle = rotvec.norm()
        if angle == 0.0:
            return Rotation()
        elif angle < EPS:
            return Rotation.from_quat(
                x=rotvec.x, y=rotvec.y, z=rotvec.z, w=1.0, tolerance=0.1
            )
        else:
            return Rotation.from_axis_angle(rotvec.normalized(), angle)

    def as_rotvec(self) -> Vector:
        """Return the rotation vector of the rotation.
        A rotation vector is the axis of rotation
        scaled by the angle of rotation."""
        axis, angle = self.as_axis_angle()
        return axis * angle

    @staticmethod
    def from_matrix(
        matrix: Sequence[Sequence[float]],
        row_major: bool = True,
        check_matrix: bool = True,
    ) -> "Rotation":
        """Create a rotation from a 3x3 rotation matrix."""
        # https://www.euclideanspace.com/maths/geometry/rotations/conversions/matrixToQuaternion/index.htm

        if check_matrix:
            # row major or column major does not matter for these checks
            if (
                len(matrix) != 3
                or len(matrix[0]) != 3
                or len(matrix[1]) != 3
                or len(matrix[2]) != 3
            ):
                raise ValueError("matrix must be 3x3")
            vx = Vector(matrix[0][0], matrix[1][0], matrix[2][0])
            vy = Vector(matrix[0][1], matrix[1][1], matrix[2][1])
            vz = Vector(matrix[0][2], matrix[1][2], matrix[2][2])
            if (
                abs(vx.norm() - 1.0) > EPS
                or abs(vy.norm() - 1.0) > EPS
                or abs(vz.norm() - 1.0) > EPS
                or abs(vx.dot(vy)) > EPS
                or abs(vy.dot(vz)) > EPS
                or abs(vz.dot(vx)) > EPS
            ):
                raise ValueError("matrix must be orthonormal")
            if vx.cross(vy).dot(vz) < 0:
                raise ValueError("matrix must not flip handedness")

        if row_major:
            m00, m01, m02 = matrix[0]
            m10, m11, m12 = matrix[1]
            m20, m21, m22 = matrix[2]
        else:
            m00, m10, m20 = matrix[0]
            m01, m11, m21 = matrix[1]
            m02, m12, m22 = matrix[2]

        trace = m00 + m11 + m22

        if trace > 0.0:
            s = sqrt(trace + 1.0) * 2.0  # s = 4 * qw
            return Rotation.from_quat(
                x=(m21 - m12) / s, y=(m02 - m20) / s, z=(m10 - m01) / s, w=0.25 * s
            )
        elif (m00 > m11) and (m00 > m22):
            s = sqrt(1.0 + m00 - m11 - m22) * 2.0  # s = 4 * qx
            return Rotation.from_quat(
                x=0.25 * s, y=(m01 + m10) / s, z=(m02 + m20) / s, w=(m21 - m12) / s
            )
        elif m11 > m22:
            s = sqrt(1.0 + m11 - m00 - m22) * 2.0  # s = 4 * qy
            return Rotation.from_quat(
                x=(m01 + m10) / s, y=0.25 * s, z=(m12 + m21) / s, w=(m02 - m20) / s
            )
        else:
            s = sqrt(1.0 + m22 - m00 - m11) * 2.0  # s = 4 * qz
            return Rotation.from_quat(
                x=(m02 + m20) / s, y=(m12 + m21) / s, z=0.25 * s, w=(m10 - m01) / s
            )

    def as_matrix(self, row_major: bool = True) -> List[List[float]]:
        """Return the rotation as a 3x3 rotation matrix."""
        # https://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToMatrix/index.htm
        x, y, z, w = self._x, self._y, self._z, self._w
        xx, xy, xz, xw = x * x, x * y, x * z, x * w
        yy, yz, yw = y * y, y * z, y * w
        zz, zw = z * z, z * w

        if row_major:
            return [
                [1.0 - 2.0 * (yy + zz), 2.0 * (xy - zw), 2.0 * (xz + yw)],
                [2.0 * (xy + zw), 1.0 - 2.0 * (xx + zz), 2.0 * (yz - xw)],
                [2.0 * (xz - yw), 2.0 * (yz + xw), 1.0 - 2.0 * (xx + yy)],
            ]
        else:
            return [
                [1.0 - 2.0 * (yy + zz), 2.0 * (xy + zw), 2.0 * (xz - yw)],
                [2.0 * (xy - zw), 1.0 - 2.0 * (xx + zz), 2.0 * (yz + xw)],
                [2.0 * (xz + yw), 2.0 * (yz - xw), 1.0 - 2.0 * (xx + yy)],
            ]

    def basis(self) -> Tuple[Vector, Vector, Vector]:
        """Return the basis vectors of the rotation."""
        x, y, z = self.as_matrix(row_major=False)
        return Vector(*x), Vector(*y), Vector(*z)

    @staticmethod
    def compose(sequence: str, angles: Sequence[float]) -> "Rotation":
        """Compose a rotation from a sequence of rotations about x, y and z.
        The sequence is an arbitrarily long string of axis identifiers, e.g. 'XY' or 'zyxZ'.
        Use Capital letters for intrinsic rotations (rotate about the new, rotated axes),
        use lowercase letters for extrinsic rotations (rotate about the world axes).
        Intrinsic and extrinsic rotations can be mixed."""
        if len(sequence) != len(angles):
            raise ValueError("sequence and angles must have the same length")
        x, y, z, w = 0.0, 0.0, 0.0, 1.0
        for axis, angle in zip(sequence, angles):
            temp = Rotation.__new__(Rotation, x=x, y=y, z=z, w=w)
            # intrinsic rotation
            if axis == "X":
                x, y, z, w = temp._rotate_quat(Rotation.x(angle))
            elif axis == "Y":
                x, y, z, w = temp._rotate_quat(Rotation.y(angle))
            elif axis == "Z":
                x, y, z, w = temp._rotate_quat(Rotation.z(angle))
            # extrinsic rotation
            elif axis == "x":
                x, y, z, w = Rotation.x(angle)._rotate_quat(temp)
            elif axis == "y":
                x, y, z, w = Rotation.y(angle)._rotate_quat(temp)
            elif axis == "z":
                x, y, z, w = Rotation.z(angle)._rotate_quat(temp)
            else:
                raise ValueError(
                    f"unknown axis: {axis}; only X, Y, Z, x, y, z are allowed"
                )
        return Rotation.from_quat(x=x, y=y, z=z, w=w)

    _euler_orders = set(
        ["ZXZ", "XYX", "YZY", "ZYZ", "XZX", "YXY"]
        + ["XYZ", "YZX", "ZXY", "XZY", "ZYX", "YXZ"]
        + ["zxz", "xyx", "yzy", "zyz", "xzx", "yxy"]
        + ["xyz", "yzx", "zxy", "xzy", "zyx", "yxz"]
    )

    @staticmethod
    def from_euler(order: str, angles: Sequence[float]) -> "Rotation":
        """Create a rotation from Euler angles.
        The following orders are allowed:
        ZXZ, XYX, YZY, ZYZ, XZX, YXY (proper Euler, intrinsic)
        XYZ, YZX, ZXY, XZY, ZYX, YXZ (Tait-Bryan, intrinsic)
        zxz, xyx, yzy, zyz, xzx, yxy (proper Euler, extrinsic)
        xyz, yzx, zxy, xzy, zyx, yxz (Tait-Bryan, extrinsic)
        intrinsic: rotate about the new, rotated axes
        extrinsic: rotate about the original axes"""
        if order not in Rotation._euler_orders:
            raise ValueError(
                f"Euler order {order} unknown, must be one of {Rotation._euler_orders}"
            )
        return Rotation.compose(order, [angles[0], angles[1], angles[2]])

    def as_euler(self, order: str) -> Tuple[float, float, float]:
        """Return the Euler angles of the rotation.
        The order is one of:
        ZXZ, XYX, YZY, ZYZ, XZX, YXY (proper Euler, intrinsic)
        XYZ, YZX, ZXY, XZY, ZYX, YXZ (Tait-Bryan, intrinsic)
        zxz, xyx, yzy, zyz, xzx, yxy (proper Euler, extrinsic)
        xyz, yzx, zxy, xzy, zyx, yxz (Tait-Bryan, extrinsic)
        intrinsic: rotate about the new, rotated axes
        extrinsic: rotate about the original axes
        In case of a singularity, the first angle is set to 0 for extrinsic rotations,
        the third angle is set to 0 for intrinsic rotations."""
        if order not in self._euler_orders:
            raise ValueError(
                f"Euler order {order} unknown, must be one of {self._euler_orders}"
            )
        is_extrinsic = order.islower()
        order = order.lower()
        is_tait_bryan = order[0] != order[2]

        m = self.as_matrix()
        ax_index = {"x": 0, "y": 1, "z": 2}
        a1, a2 = ax_index[order[0]], ax_index[order[1]]
        a3 = 3 - a1 - a2  # Tait-Bryan: 3rd axis, proper Euler: unused axis
        parity = 1.0 if a2 == (a1 + 1) % 3 else -1.0

        if is_tait_bryan:  # e.g. xyz
            if is_extrinsic:
                a1, a3 = a3, a1
                parity = -parity
            beta = atan2(parity * m[a1][a3], norm(m[a1][a2], m[a1][a1]))
            if abs(abs(beta) - pi / 2.0) > EPS:
                alpha = atan2(-parity * m[a2][a3], m[a3][a3])
                gamma = atan2(-parity * m[a1][a2], m[a1][a1])
            else:  # singularity
                alpha = atan2(parity * m[a3][a2], m[a2][a2])
                gamma = 0.0
        else:  # proper Euler, e.g. zxz
            beta = atan2(norm(m[a2][a1], m[a3][a1]), m[a1][a1])
            if abs(beta) > EPS and abs(beta) < pi - EPS:
                alpha = atan2(m[a2][a1], -parity * m[a3][a1])
                gamma = atan2(m[a1][a2], parity * m[a1][a3])
            else:  # singularity
                alpha = atan2(parity * m[a3][a2], m[a2][a2])
                gamma = 0.0

        if is_extrinsic:
            return gamma, beta, alpha
        return alpha, beta, gamma

    @staticmethod
    def from_ypr(yaw: float, pitch: float, roll: float) -> "Rotation":
        """Create a rotation from yaw, pitch and roll angles."""
        return Rotation.compose("ZYX", [yaw, pitch, roll])

    def as_ypr(self) -> Tuple[float, float, float]:
        """Return the yaw, pitch and roll angles of the rotation.
        In case of a singularity (gimbal lock), roll is set to 0."""
        return self.as_euler("ZYX")

    @staticmethod
    def from_rpy(roll: float, pitch: float, yaw: float) -> "Rotation":
        """Create a rotation from roll, pitch and yaw angles."""
        return Rotation.compose("xyz", [roll, pitch, yaw])

    def as_rpy(self) -> Tuple[float, float, float]:
        """Return the roll, pitch and yaw angles of the rotation.
        In case of a singularity (gimbal lock), roll is set to 0."""
        return self.as_euler("xyz")

    @staticmethod
    def rand(generator: random.Random = cast(random.Random, random)) -> "Rotation":
        """Create a random rotation with uniform distribution."""
        x = generator.gauss()
        y = generator.gauss()
        z = generator.gauss()
        w = generator.gauss()
        # should be impossible for Mersenne twister to generate a zero quaternion
        return Rotation.from_quat(x=x, y=y, z=z, w=w, tolerance=_inf)

    def _rotate_vector(self, other: Vector) -> Vector:
        """Rotate a vector by the rotation (returns a new Vector)."""
        qx, qy, qz, qw = self._x, self._y, self._z, self._w
        px, py, pz = other  # pw = 0

        qpx = qw * px + qy * pz - qz * py
        qpy = qw * py - qx * pz + qz * px
        qpz = qw * pz + qx * py - qy * px
        qpw = -qx * px - qy * py - qz * pz

        qpq_x = -qpw * qx + qpx * qw - qpy * qz + qpz * qy
        qpq_y = -qpw * qy + qpx * qz + qpy * qw - qpz * qx
        qpq_z = -qpw * qz - qpx * qy + qpy * qx + qpz * qw

        return Vector(qpq_x, qpq_y, qpq_z)

    def _rotate_quat(self, other: "Rotation") -> Tuple[float, float, float, float]:
        """Combine two rotations (quaternion multiplication)."""
        x1, y1, z1, w1 = self._x, self._y, self._z, self._w
        x2, y2, z2, w2 = other._x, other._y, other._z, other._w
        x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
        y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
        z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
        w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
        # does not return Rotation to let the caller decide whether to normalize
        return x, y, z, w

    @overload
    def __matmul__(self, other: "Rotation") -> "Rotation":
        """Combine two rotations."""
        ...

    @overload
    def __matmul__(self, other: Vector) -> Vector:
        """Rotate a vector."""
        ...

    @overload
    def __matmul__(self, other: Iterable[Vector]) -> Iterable[Vector]:
        """Rotate a sequence of vectors."""
        ...

    def __matmul__(
        self, other: Union["Rotation", Vector, Iterable[Vector]]
    ) -> Union["Rotation", Vector, Iterable[Vector]]:
        """Combine two rotations or rotate a vector or a sequence of vectors."""
        if isinstance(other, Rotation):
            x, y, z, w = self._rotate_quat(other)
            return Rotation.from_quat(x=x, y=y, z=z, w=w)
        elif isinstance(other, Vector):
            return self._rotate_vector(other)
        elif isinstance(other, Iterable):
            other = cast(Iterable[Vector], other)
            # Conversion to matrix costs some compute but is worth it for many multiplications
            # since mtx @ v is faster than quat @ v.
            rx, ry, rz = self.as_matrix(row_major=True)
            return [
                Vector(
                    rx[0] * v[0] + rx[1] * v[1] + rx[2] * v[2],
                    ry[0] * v[0] + ry[1] * v[1] + ry[2] * v[2],
                    rz[0] * v[0] + rz[1] * v[1] + rz[2] * v[2],
                )
                for v in other
            ]
        else:
            return NotImplemented

    def inverse(self) -> "Rotation":
        """Return the inverse rotation (as a new Rotation).
        Such that self @ self.inverse() == Rotation.identity()."""
        return Rotation.__new__(Rotation, x=-self._x, y=-self._y, z=-self._z, w=self._w)

    def angle_to(self, other: "Rotation") -> float:
        """Calculate the angle to another rotation (in rad)."""
        _, ang = (~self @ other).as_axis_angle()
        return ang

    def axis_angle_to(self, other: "Rotation") -> Tuple[Vector, float]:
        """Calculate the axis and angle (in rad) to another rotation."""
        ax, ang = (~self @ other).as_axis_angle()
        return self @ ax, ang

    def lerp(self, other: "Rotation", f: float) -> "Rotation":
        """Linearly interpolate between two rotations (returns a new Rotation)."""
        ax, ang = (~self @ other).as_axis_angle()
        return self @ Rotation.from_axis_angle(ax, ang * f)

    class RotationMeanReport(NamedTuple):
        """Additional information about convergence of the mean method"""

        converged: bool
        iterations: int
        last_change: float

    @staticmethod
    @overload
    def mean(
        rotations: Iterable["Rotation"],
        weights: Optional[Iterable[float]] = None,
        epsilon: float = EPS,
        max_iterations: int = 20,
        return_report: Literal[False] = False,
    ) -> "Rotation": ...

    @staticmethod
    @overload
    def mean(
        rotations: Iterable["Rotation"],
        weights: Optional[Iterable[float]] = None,
        epsilon: float = EPS,
        max_iterations: int = 20,
        return_report: Literal[True] = True,
    ) -> Tuple["Rotation", RotationMeanReport]: ...

    @staticmethod
    def mean(
        rotations: Iterable["Rotation"],
        weights: Optional[Iterable[float]] = None,
        epsilon: float = EPS,
        max_iterations: int = 20,
        return_report: bool = False,
    ) -> Union["Rotation", Tuple["Rotation", RotationMeanReport]]:
        """Calculate the mean of a sequence of rotations.
        Uses the NASA algorithm (https://ntrs.nasa.gov/citations/20070017872).
        Raises when called with an empty sequence or when the sum of weights is zero.
        Set return_report to True to get additional information about convergence."""

        weights = weights or repeat(1.0)

        if (
            hasattr(rotations, "__len__")
            and hasattr(weights, "__len__")
            and rotations.__len__() != weights.__len__()
        ):
            raise ValueError("rotations and weights must have the same length")

        m11, m12, m13, m14 = 0.0, 0.0, 0.0, 0.0
        m22, m23, m24 = 0.0, 0.0, 0.0
        m33, m34 = 0.0, 0.0
        m44 = 0.0

        # compute matrix M in the Nasa paper (eq. 12)
        # M is symmetrical, so we only need to compute the upper triangle
        w_sum = 0.0
        for rot, weight in zip(rotations, weights):
            x, y, z, w = rot._x, rot._y, rot._z, rot._w
            m11 += x * x * weight
            m12 += x * y * weight
            m13 += x * z * weight
            m14 += x * w * weight
            m22 += y * y * weight
            m23 += y * z * weight
            m24 += y * w * weight
            m33 += z * z * weight
            m34 += z * w * weight
            m44 += w * w * weight
            w_sum += weight

        if w_sum == 0.0:
            raise ValueError(
                "cannot compute mean if sequence is empty or sum of weights is 0"
            )

        converged = True
        epsilon2 = epsilon * epsilon
        x, y, z, w = 0.0, 0.0, 0.0, 0.0
        for i in range(max_iterations):
            m11_ = m11 * m11 + m12 * m12 + m13 * m13 + m14 * m14
            m12_ = m11 * m12 + m12 * m22 + m13 * m23 + m14 * m24
            m13_ = m11 * m13 + m12 * m23 + m13 * m33 + m14 * m34
            m14_ = m11 * m14 + m12 * m24 + m13 * m34 + m14 * m44
            m22_ = m12 * m12 + m22 * m22 + m23 * m23 + m24 * m24
            m23_ = m12 * m13 + m22 * m23 + m23 * m33 + m24 * m34
            m24_ = m12 * m14 + m22 * m24 + m23 * m34 + m24 * m44
            m33_ = m13 * m13 + m23 * m23 + m33 * m33 + m34 * m34
            m34_ = m13 * m14 + m23 * m24 + m33 * m34 + m34 * m44
            m44_ = m14 * m14 + m24 * m24 + m34 * m34 + m44 * m44

            # trace is the sum of all squared previous elements, so always positive
            # we use it to roughly normalize the matrix so it does not diverge
            trace = m11_ + m22_ + m33_ + m44_
            m11, m12, m13, m14 = m11_ / trace, m12_ / trace, m13_ / trace, m14_ / trace
            m22, m23, m24 = m22_ / trace, m23_ / trace, m24_ / trace
            m33, m34 = m33_ / trace, m34_ / trace
            m44 = m44_ / trace

            x_, y_, z_, w_ = x, y, z, w  # previous values for convergence check

            if m44 >= m11 and m44 >= m22 and m44 >= m33:
                x, y, z, w = m14, m24, m34, m44
            elif m11 >= m22 and m11 >= m33:
                x, y, z, w = m11, m12, m13, m14
            elif m22 >= m33:
                x, y, z, w = m12, m22, m23, m24
            else:
                x, y, z, w = m13, m23, m33, m34
            n = sqrt(x * x + y * y + z * z + w * w)
            x, y, z, w = x / n, y / n, z / n, w / n

            delta2 = (x - x_) ** 2 + (y - y_) ** 2 + (z - z_) ** 2 + (w - w_) ** 2
            if delta2 < epsilon2:
                break
        else:
            converged = False

        result = Rotation.__new__(Rotation, x=x, y=y, z=z, w=w)

        if not return_report:
            return result
        else:
            return result, Rotation.RotationMeanReport(
                converged, iterations=i + 1, last_change=sqrt(delta2)
            )

    def rotated_towards(
        self, pointer: Vector, point_along: Vector, interpolate: float = 1.0
    ) -> "Rotation":
        """Start from this rotation and rotate pointer towards point_along (returns a new Rotation).
        pointer is a local vector in the current rotation,
        point_along is a global direction.
        Use interpolate to blend between the two.
        """
        current = self @ pointer
        axis = current.cross(point_along)
        if axis.norm() == 0:
            axis = current.perp()
        angle = current.angle_to(point_along)
        return Rotation.from_axis_angle(axis, angle * interpolate) @ self

    def __eq__(self, other: object) -> bool:
        """Check if two rotations are equal.
        If the underlying quaternions are opposite, they represent the same rotation
        and are considered equal."""

        if isinstance(other, Rotation):
            return (
                self._x == other._x
                and self._y == other._y
                and self._z == other._z
                and self._w == other._w
            ) or (
                self._x == -other._x
                and self._y == -other._y
                and self._z == -other._z
                and self._w == -other._w
            )
        else:
            return NotImplemented

    def __invert__(self) -> "Rotation":
        """Return the inverse rotation such that r @ ~r == Rotation.identity()."""
        return self.inverse()

    def __str__(self) -> str:
        """Return a string representation of the rotation.
        Note that opposite quaternions represent the same rotation and are considered equal
        whereas their string representations are different."""
        return f"±(x={self._x}, y={self._y}, z={self._z}, w={self._w})"

    def __format__(self, format_spec: str) -> str:
        """Return a formatted string representation of the rotation.
        The format_spec is applied to each element.
        Note that opposite quaternions represent the same rotation and are considered equal
        whereas their string representations are different."""

        fx = self._x.__format__(format_spec)
        fy = self._y.__format__(format_spec)
        fz = self._z.__format__(format_spec)
        fw = self._w.__format__(format_spec)
        return f"±(x={fx}, y={fy}, z={fz}, w={fw})"

    def __repr__(self) -> str:
        """Return an eval-able string representation of the rotation.
        Note that opposite quaternions represent the same rotation and are considered equal
        whereas their string representations are different."""
        return f"Rotation.from_quat(x={self._x}, y={self._y}, z={self._z}, w={self._w})"

    def __hash__(self) -> int:
        """Return a hash of the rotation.
        Quaternions with opposite signs are considered equal rotations and return the same hash.
        """
        if self._w != 0.0:
            s = copysign(1.0, self._w)
        elif self._x != 0.0:
            s = copysign(1.0, self._x)
        elif self._y != 0.0:
            s = copysign(1.0, self._y)
        else:
            s = copysign(1.0, self._z)
        return hash((s * self._x, s * self._y, s * self._z, s * self._w))


@dataclass(frozen=True)
class Trafo:
    """An immutable 3D transformation consisting of a translation and a rotation"""

    t: Vector
    r: Rotation

    def __init__(self, *, t: Vector = Vector.zero(), r: Rotation = Rotation.identity()):
        """Create a transformation from a translation and a rotation."""
        # kw_only parameter for @dataclass only supported for Python 3.10+
        object.__setattr__(self, "t", t)
        object.__setattr__(self, "r", r)

    @staticmethod
    def identity() -> "Trafo":
        """Return the identity transformation."""
        return Trafo()

    @staticmethod
    def from_matrix(
        matrix: Sequence[Sequence[float]],
        row_major: bool = True,
        check_matrix: bool = True,
    ) -> "Trafo":
        """Create a transformation from a 3x4 or 4x4 homogeneous transformation matrix."""
        if check_matrix:
            if row_major:
                if (
                    len(matrix) not in [3, 4]
                    or len(matrix[0]) != 4
                    or len(matrix[1]) != 4
                    or len(matrix[2]) != 4
                ):
                    raise ValueError("matrix must be 3x4 or 4x4")
            else:
                if (
                    len(matrix) != 4
                    or len(matrix[0]) not in [3, 4]
                    or len(matrix[1]) not in [3, 4]
                    or len(matrix[2]) not in [3, 4]
                    or len(matrix[3]) not in [3, 4]
                    # allows 3 4 3 4 but I mean come on
                ):
                    raise ValueError("matrix must be 3x4 or 4x4")

        return Trafo(
            t=(
                Vector(matrix[0][3], matrix[1][3], matrix[2][3])
                if row_major
                else Vector(matrix[3][0], matrix[3][1], matrix[3][2])
            ),
            r=Rotation.from_matrix(
                [matrix[0][0:3], matrix[1][0:3], matrix[2][0:3]],
                row_major=row_major,
                check_matrix=check_matrix,
            ),
        )

    def as_matrix(
        self, row_major: bool = True, num_rows: Literal[3, 4] = 4
    ) -> List[List[float]]:
        """Return the transformation as a 3x4 or 4x4 homogeneous transformation matrix."""
        matrix = self.r.as_matrix(row_major=row_major)
        if row_major:
            matrix[0].append(self.t.x)
            matrix[1].append(self.t.y)
            matrix[2].append(self.t.z)
            if num_rows == 4:
                matrix.append([0.0, 0.0, 0.0, 1.0])
        else:
            matrix.append([self.t.x, self.t.y, self.t.z])
            if num_rows == 4:
                matrix[0].append(0.0)
                matrix[1].append(0.0)
                matrix[2].append(0.0)
                matrix[3].append(1.0)
        return matrix

    @overload
    @staticmethod
    def from_dh(
        *, a: float = 0.0, alpha: float = 0.0, theta: float = 0.0, s: float = 0.0
    ) -> "Trafo": ...

    @overload
    @staticmethod
    def from_dh(
        *, r: float = 0.0, alpha: float = 0.0, theta: float = 0.0, s: float = 0.0
    ) -> "Trafo": ...

    @overload
    @staticmethod
    def from_dh(
        *, a: float = 0.0, alpha: float = 0.0, theta: float = 0.0, d: float = 0.0
    ) -> "Trafo": ...

    @overload
    @staticmethod
    def from_dh(
        *, r: float = 0.0, alpha: float = 0.0, theta: float = 0.0, d: float = 0.0
    ) -> "Trafo": ...

    @staticmethod
    def from_dh(
        *,
        a: float = 0.0,  # original letter
        alpha: float = 0.0,
        theta: float = 0.0,
        s: float = 0.0,  # original letter
        r: float = 0.0,  # alternative to a (often used to avoid confusion with alpha)
        d: float = 0.0  # alternative to s (often used since s is used to abbreviate sin)
    ) -> "Trafo":
        """Create a transformation from Denavit-Hartenberg parameters.
        https://en.wikipedia.org/wiki/Denavit%E2%80%93Hartenberg_parameters
        s or d: offset along previous z to the common normal
        theta: angle about previous z from old x to new x
        r or a: length of the common normal
        alpha: angle about common normal, from old z axis to new z axis
        """
        if not a == 0.0 and not r == 0.0:
            raise ValueError("only a or r can be set, not both")
        if not s == 0.0 and not d == 0.0:
            raise ValueError("only s or d can be set, not both")

        a_ = a + r
        s_ = s + d

        return Trafo(t=Vector(z=s_), r=Rotation.z(theta)) @ Trafo(
            t=Vector(x=a_), r=Rotation.x(alpha)
        )

    @overload
    @staticmethod
    def look_at(
        *,
        eye: Vector,
        look_axis: Vector,
        look_at: Vector,
        up_axis: Vector,
        up: Vector,
    ) -> "Trafo": ...

    @overload
    @staticmethod
    def look_at(
        *,
        eye: Vector,
        look_axis: Vector,
        look_along: Vector,
        up_axis: Vector,
        up: Vector,
    ) -> "Trafo": ...

    @staticmethod
    def look_at(
        *,
        eye: Vector,
        look_axis: Vector,
        look_at: Optional[Vector] = None,
        look_along: Optional[Vector] = None,
        up_axis: Vector,
        up: Vector,
    ) -> "Trafo":
        """Create a transformation that looks at a target point.
        eye: location
        look_axis: local view direction (from eye towards target)
        look_at: target if target is a point
        look_along: target if target is a direction
        up_axis: local up direction
        up: global up direction
        """

        # rotate the user-defined camera coordinate system (look_axis, up_axis)
        # to align with our convention:
        # x is the look axis (from eye towards target)
        # y is the up axis
        # z is the right axis

        if look_axis.norm() == 0:
            raise ValueError("look_axis must not be a zero vector")
        if up_axis.norm() == 0:
            raise ValueError("up_axis must not be a zero vector")
        if look_axis.cross(up_axis).norm() == 0:
            raise ValueError(
                "look_axis and up_axis must not be parallel or anti-parallel"
            )

        look_axis, up_axis, right_axis = Vector.make_basis(look_axis, up_axis)

        intrinsic_rotation = Rotation.from_matrix(
            [look_axis, up_axis, right_axis], check_matrix=False
        )

        # align our convention coordinate system with the environment (eye, target, up):
        # camera is located at eye
        # x points towards the target
        # roll until y points towards up as well as possible
        # z is determined from cross product

        if look_at is not None and look_along is None:
            look_along = look_at - eye
        elif look_at is None and look_along is not None:
            pass
        else:
            raise ValueError("either look_at or look_along must be set")

        if look_along.norm() == 0:
            # eye is located at target or target is the zero vector
            # orientation is undefined (but always kind of correct), return identity
            return Trafo(t=eye, r=Rotation.identity())
        if up.cross(look_along).norm() == 0:
            # up is parallel or anti-parallel to look direction or up is the zero vector
            # roll is undefined, just rotate the identity orientation to look towards the target
            return Trafo(t=eye).rotated_towards(look_axis, point_along=look_along)

        view_direction, up_direction, right_direction = Vector.make_basis(
            look_along, up
        )

        extrinsic_rotation = Rotation.from_matrix(
            [view_direction, up_direction, right_direction],
            row_major=False,
            check_matrix=False,
        )

        return Trafo(t=eye, r=extrinsic_rotation @ intrinsic_rotation)

    @overload
    def __matmul__(self, other: "Trafo") -> "Trafo":
        """Combine two transformations."""
        ...

    @overload
    def __matmul__(self, other: Vector) -> Vector:
        """Transform a point. (Use myTrafo.r @ myVector to transform a direction)."""
        ...

    @overload
    def __matmul__(self, other: Iterable[Vector]) -> Iterable[Vector]:
        """Transform a sequence of points."""
        ...

    def __matmul__(
        self, other: Union["Trafo", Vector, Iterable[Vector]]
    ) -> Union["Trafo", Vector, Iterable[Vector]]:
        """Combine two transformations or transform a point or sequence of points.
        Use myTrafo.r @ myVector to transform a Vector as a direction instead."""

        if isinstance(other, Trafo):
            return Trafo(
                t=self.t + self.r @ other.t,
                r=self.r @ other.r,
            )
        elif isinstance(other, Vector):
            return self.r._rotate_vector(other) + self.t
        elif isinstance(other, Iterable):
            other = cast(Iterable[Vector], other)
            rotated = self.r @ other
            return [r + self.t for r in rotated]
        else:
            return NotImplemented

    def inverse(self) -> "Trafo":
        """Return the inverse transformation (as a new Trafo).
        Such that t @ t.inverse() == Trafo.identity()."""
        inv_r = ~self.r
        return Trafo(t=inv_r @ -self.t, r=inv_r)

    def lerp(self, other: "Trafo", f: float) -> "Trafo":
        """Linearly interpolate between two transformations (returns a new Trafo)."""
        return Trafo(
            t=self.t.lerp(other.t, f),
            r=self.r.lerp(other.r, f),
        )

    @staticmethod
    def mean(
        trafos: Iterable["Trafo"], weights: Optional[Iterable[float]] = None
    ) -> "Trafo":
        """Calculate the weighted mean of a sequence of transformations."""
        return Trafo(
            t=Vector.mean([t.t for t in trafos], weights),
            r=Rotation.mean([t.r for t in trafos], weights),
        )

    @overload
    def rotated_towards(
        self, pointer: Vector, *, point_at: Vector, interpolate: float = 1.0
    ) -> "Trafo": ...

    @overload
    def rotated_towards(
        self, pointer: Vector, *, point_along: Vector, interpolate: float = 1.0
    ) -> "Trafo": ...

    def rotated_towards(
        self,
        pointer: Vector,
        *,
        point_at: Optional[Vector] = None,
        point_along: Optional[Vector] = None,
        interpolate: float = 1.0
    ) -> "Trafo":
        """
        Return a rotated version of the transformation, aligning a pointer.
        Such that the local pointer is rotated towards
        the global target point (point_at) or direction (point_along).
        Use interpolate to blend between current and target.
        """

        if point_at is not None and point_along is None:
            point_along = point_at - self.t
        elif point_at is None and point_along is not None:
            pass
        else:
            raise ValueError("either point_at or point_along must be set")

        return Trafo(
            t=self.t,
            r=self.r.rotated_towards(pointer, point_along, interpolate),
        )

    def __eq__(self, other: object) -> bool:
        """Check if two transformations are equal."""
        if isinstance(other, Trafo):
            return self.t == other.t and self.r == other.r
        else:
            return NotImplemented

    def __invert__(self) -> "Trafo":
        """Return the inverse transformation such that t @ ~t == Trafo.identity()."""
        return self.inverse()

    def __str__(self) -> str:
        """Return a string representation of the transformation."""
        return f"(t={self.t}, r={self.r})"

    def __format__(self, format_spec: str) -> str:
        """Return a formatted string representation of the transformation.
        The format_spec is applied to each element."""
        ft = self.t.__format__(format_spec)
        fr = self.r.__format__(format_spec)
        return f"(t={ft}, r={fr})"

    def __repr__(self) -> str:
        """Return an eval-able string representation of the transformation."""
        return f"Trafo(t={self.t.__repr__()}, r={self.r.__repr__()})"


class Node:
    """A node in a tree structure that represents a hierarchy of transformations (i.e. a scene graph)"""

    __slots__ = ("_parent", "trafo", "_children", "label")
    _parent: Union["Node", None]
    trafo: Trafo
    _children: list["Node"]
    label: str

    def __init__(
        self,
        parent: Union["Node", None] = None,
        trafo: Trafo = Trafo(),
        label: str = "",
    ):
        """Create a node with a transformation relative to a parent.
        Assign a label for debugging and visualizing."""
        self._parent = parent
        if parent is not None:
            parent._children.append(self)
        self.trafo = trafo
        self._children = []
        self.label = label

    def attach_to(
        self, new_parent: Union["Node", None], keep_relative_trafo: bool = False
    ) -> None:
        """Attach the node to a new parent.
        If keep_relative_trafo is true, the transformation of the node is updated
        to keep the relative transformation to the new parent the same."""

        ancestor = new_parent
        while ancestor is not None:
            if ancestor == self:
                raise ValueError("cannot attach, would create a cycle")
            ancestor = ancestor._parent

        if new_parent is not None and keep_relative_trafo:
            self.trafo = new_parent >> self

        if self._parent is not None:
            self._parent._children.remove(self)

        self._parent = new_parent
        if new_parent is not None:
            new_parent._children.append(self)

    def get_parent(self) -> Union["Node", None]:
        """Return the parent node."""
        return self._parent

    def get_children(self) -> list["Node"]:
        """Return the child nodes. (Returns a copy of the list that can be modified.)"""
        return self._children.copy()

    def __rshift__(self, other: "Node") -> Trafo:
        """Return the transformation from the node to another node in the hierarchy."""
        if not isinstance(other, Node):
            return NotImplemented

        my_ancestors: set["Node"] = set()
        common_ancestor: Union["Node", None] = None
        node: Union["Node", None] = self
        while node is not None:
            my_ancestors.add(node)
            node = node._parent

        node = other
        while node is not None:
            if node in my_ancestors:
                common_ancestor = node
                break
            node = node._parent

        if common_ancestor is None:
            raise ValueError(
                f'nodes "{self.label}" and "{other.label}" are not connected'
            )

        me_to_common_ancestor = Trafo()
        ancestor = self
        while ancestor != common_ancestor:
            me_to_common_ancestor = me_to_common_ancestor @ ~ancestor.trafo
            ancestor = cast("Node", ancestor._parent)

        common_ancestor_to_other = Trafo()
        ancestor = other
        while ancestor != common_ancestor:
            common_ancestor_to_other = ancestor.trafo @ common_ancestor_to_other
            ancestor = cast("Node", ancestor._parent)

        return me_to_common_ancestor @ common_ancestor_to_other


class DebugDrawer(ABC):
    """Abstract base class for a debug drawer that lets you visualize
    vectors, rotations and transformations in relation to each other.
    At minimum, the line method must be implemented."""

    Color = Literal["default", "x-red", "y-green", "z-blue"]

    def __init__(
        self,
        up: Vector = Vector.ez(),
        arrow_length: float = 1.0,
        font_size: float = 0.1,
        text_direction: Vector = Vector.ex(),
    ):
        """Create a debug drawer.
        The settings are used in the default implementations
        of the drawing methods, subclasses are free to ignore them."""
        self.up = up
        self.arrow_length = arrow_length
        self.font_size = font_size
        self.text_direction = text_direction

    @abstractmethod
    def line(
        self,
        start: Vector,
        end: Vector,
        color: Color,
    ) -> None:
        """Draw a line."""
        pass

    def arrow(self, start: Vector, end: Vector, color: Color) -> None:
        """Draw an arrow."""
        v = end - start
        if v.norm() > 0:
            barb1 = start + 0.9 * v + 0.05 * v.norm() * v.perp()
            barb2 = start + 0.9 * v - 0.05 * v.norm() * v.perp()
            self.line(start, end, color)
            self.line(end, barb1, color)
            self.line(end, barb2, color)

    def point(self, position: Vector) -> None:
        """Draw a point."""
        self.line(position - Vector(x=0.01), position + Vector(x=0.01), "default")
        self.line(position - Vector(y=0.01), position + Vector(y=0.01), "default")
        self.line(position - Vector(z=0.01), position + Vector(z=0.01), "default")

    def vector(self, vector: Vector) -> None:
        """Draw a vector as an arrow from the origin."""
        self.arrow(Vector.zero(), vector, "default")

    def rotation(self, rotation: Rotation) -> None:
        """Draw a rotation as a rotated coordinate frame."""
        o = Vector.zero()
        x = rotation @ Vector.ex()
        y = rotation @ Vector.ey()
        z = rotation @ Vector.ez()
        self.arrow(o, x * self.arrow_length, "x-red")
        self.arrow(o, y * self.arrow_length, "y-green")
        self.arrow(o, z * self.arrow_length, "z-blue")

    def trafo(self, trafo: Trafo) -> None:
        """Draw a transformation as a transformed coordinate frame."""
        o = trafo.t
        x = trafo.r @ Vector.ex()
        y = trafo.r @ Vector.ey()
        z = trafo.r @ Vector.ez()
        self.arrow(o, o + x * self.arrow_length, "x-red")
        self.arrow(o, o + y * self.arrow_length, "y-green")
        self.arrow(o, o + z * self.arrow_length, "z-blue")

    def text(self, position: Vector, text: str) -> None:
        """Draw text at a position."""
        # https://en.wikipedia.org/wiki/Fourteen-segment_display

        raster = self.font_size * 0.25  # length of a middle horizontal segment
        # (half width of a character, quarter height of an upper case character)

        # fmt: off
        segment_lines = [
            (0, 4, 2, 4), (2, 4, 2, 2), (2, 2, 2, 0), (2, 0, 0, 0),
            (0, 0, 0, 2), (0, 2, 0, 4), (0, 2, 1, 2), (1, 2, 2, 2),
            (0, 4, 1, 2), (1, 4, 1, 2), (2, 4, 1, 2), (0, 0, 1, 2),
            (1, 0, 1, 2), (2, 0, 1, 2), (1, 0, 1, 0.3),
        ]

        masks = {
            " ": 0x0000, "!": 0x4200, ",": 0x0800, "-": 0x00C0, ".": 0x4000,
            "0": 0x0C3F, "1": 0x0406, "2": 0x00DB, "3": 0x008F, "4": 0x00E6,
            "5": 0x00ED, "6": 0x00FD, "7": 0x1401, "8": 0x00FF, "9": 0x00E7,
            "?": 0x4083, "A": 0x00F7, "B": 0x128F, "C": 0x0039, "D": 0x120F,
            "E": 0x00F9, "F": 0x00F1, "G": 0x00BD, "H": 0x00F6, "I": 0x1209,
            "J": 0x001E, "K": 0x2470, "L": 0x0038, "M": 0x0536, "N": 0x2136,
            "O": 0x003F, "P": 0x00F3, "Q": 0x203F, "R": 0x20F3, "S": 0x018D,
            "T": 0x1201, "U": 0x003E, "V": 0x0C30, "W": 0x2836, "X": 0x2D00,
            "Y": 0x1500, "Z": 0x0C09, "_": 0x0008
        }
        # fmt: on

        x0 = 2.0 * raster
        y0 = -6.0 * raster

        tf = Trafo.look_at(
            eye=position,
            look_axis=Vector.ex(),
            look_along=self.text_direction,
            up_axis=Vector.ey(),
            up=self.up,
        )

        def fsd_char(i: int, mask: int, lower: bool) -> None:
            for bit, line_coords in enumerate(segment_lines):
                if mask & (1 << bit):
                    u0, v0, u1, v1 = line_coords
                    shrink = 0.7 if lower else 1
                    self.line(
                        tf
                        @ Vector(
                            x0 + (3.0 * i + u0) * raster, y0 + v0 * raster * shrink
                        ),
                        tf
                        @ Vector(
                            x0 + (3.0 * i + u1) * raster, y0 + v1 * raster * shrink
                        ),
                        "default",
                    )

        for i, c in enumerate(text):
            mask = masks[c.upper() if c.upper() in masks else "?"]
            fsd_char(i, mask, c.islower())

    def node(self, node: Node, offset: Trafo = Trafo()) -> None:
        """Draw a node.
        Draws a Trafo with an arrow from the origin and a label;
        origin and Trafo can be shifted by offset."""
        o_parent = offset.t
        o_node = offset @ node.trafo.t
        self.arrow(o_parent, o_node, "default")
        self.trafo(offset @ node.trafo)
        self.text(o_node, node.label)

    def tree(self, root: Node, offset: Trafo = Trafo()) -> None:
        """Draw a tree of Trafos starting at the root node, shifted by offset."""
        self.node(root, offset)
        for child in root.get_children():
            self.tree(child, offset=offset @ root.trafo)
