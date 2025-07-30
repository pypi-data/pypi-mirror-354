import trafo
from trafo import (
    Vector,
    Rotation,
    Trafo,
    Node,
    norm,
    DebugDrawer,
    DEG,
    EPS,
)

import unittest
import math
import random
import hashlib
from typing import Sequence, Any


def deterministic_hash(data: str) -> str:
    # default hash() function has a random seed which ruins it for our purpose
    return hashlib.sha256(data.encode()).hexdigest()[0:8]


mu = 5e-324  # smallest positive double


class TestBase(unittest.TestCase):

    def assertClose(self, a: Any, b: Any, delta: float = 1e-14) -> None:
        super().assertAlmostEqual(a, b, delta=delta)

    def assertElementsClose(
        self, a: Sequence[float], b: Sequence[float], delta: float = 1e-14
    ) -> None:
        for x, y in zip(a, b):
            self.assertClose(x, y, delta=delta)

    def assertRotationsClose(
        self, r1: Rotation, r2: Rotation, delta: float = 1e-14
    ) -> None:
        x1, y1, z1, w1 = r1.as_quat("xyzw")
        x2, y2, z2, w2 = r2.as_quat("xyzw")
        dot = x1 * x2 + y1 * y2 + z1 * z2 + w1 * w2
        if dot < 0.0:
            x2, y2, z2, w2 = -x2, -y2, -z2, -w2
        self.assertElementsClose((x1, y1, z1, w1), (x2, y2, z2, w2), delta=delta)

    def assertRotationNormalized(self, r: Rotation, delta: float = 1e-14) -> None:
        self.assertClose(norm(*r.as_quat("xyzw")), 1.0, delta=delta)

    def assertTrafosClose(self, tf1: Trafo, tf2: Trafo, delta: float = 1e-14) -> None:
        self.assertElementsClose(tf1.t, tf2.t, delta=delta)
        self.assertRotationsClose(tf1.r, tf2.r, delta=delta)


class TestUtilities(TestBase):

    def test_imports(self) -> None:
        import trafo.trafo as direct_import

        expected = []
        for name, obj in vars(direct_import).items():
            if "__module__" not in dir(obj) or obj.__module__ == "trafo.trafo":
                if not name.startswith("_") and name not in ["pi", "random"]:
                    expected.append(name)
        for name in expected:
            self.assertIn(name, dir(trafo))

    def test_epsilon(self) -> None:
        self.assertEqual(math.cos(EPS), 1.0)
        self.assertEqual(math.cos(-EPS), 1.0)
        self.assertEqual(math.sin(EPS), EPS)
        self.assertEqual(math.sin(-EPS), -EPS)
        self.assertEqual(math.sqrt(1.0 + EPS * EPS), 1.0)
        self.assertEqual(math.sqrt(1.0 - EPS * EPS), 1.0)

    def test_deg(self) -> None:
        self.assertEqual(math.sin(90.0 * DEG), 1.0)

    def test_norm(self) -> None:
        self.assertEqual(norm(0.0, 0.0), 0.0)
        a = 3.0 * mu
        b = 4.0 * mu
        c = norm(a, b)
        self.assertEqual(c, 5.0 * mu)


class TestVector(TestBase):

    def test_init(self) -> None:
        v1 = Vector()
        self.assertEqual(v1[:], (0.0, 0.0, 0.0))
        v2 = Vector(1.0, 2.0, 3.0)
        self.assertEqual(v2[:], (1.0, 2.0, 3.0))

    def test_slots(self) -> None:
        v = Vector()
        _ = v.x
        _ = v.y
        _ = v.z
        with self.assertRaises(AttributeError):
            v.w = 1.0  # type: ignore

    def test_get_iter(self) -> None:
        v = Vector(1.0, 2.0, 3.0)
        for i, e in enumerate(v):
            self.assertEqual(e, i + 1.0)
        with self.assertRaises(IndexError):
            _ = v[3]  # type: ignore
        self.assertEqual(v[0:3:2], (1.0, 3.0))
        self.assertEqual(v[-1], 3.0)

    def test_immutable(self) -> None:
        v = Vector(1.0, 2.0, 3.0)
        with self.assertRaises(AttributeError):
            v.x = 4.0  # type: ignore
        with self.assertRaises(TypeError):
            v[0] = 4.0  # type: ignore
        with self.assertRaises(AttributeError):
            del v.x  # type: ignore

    def test_init_sugar(self) -> None:
        self.assertEqual(Vector.zero(), Vector(0.0, 0.0, 0.0))
        self.assertEqual(Vector.ex(), Vector(1.0, 0.0, 0.0))
        self.assertEqual(Vector.ey(), Vector(0.0, 1.0, 0.0))
        self.assertEqual(Vector.ez(), Vector(0.0, 0.0, 1.0))

    def test_rand_box(self) -> None:
        n = 10000

        self.assertNotEqual(Vector.rand_box()[0], Vector.rand_box()[0])

        v1 = Vector.rand_box(generator=random.Random(123))
        v2 = Vector.rand_box(generator=random.Random(123))
        self.assertEqual(v1[:], v2[:])

        bucket = 0
        rng = random.Random(123)
        for _ in range(n):
            x, y, z = Vector.rand_box(generator=rng)
            self.assertGreaterEqual(x, 0.0)
            self.assertLess(x, 1.0)
            self.assertGreaterEqual(y, 0.0)
            self.assertLess(y, 1.0)
            self.assertGreaterEqual(z, 0.0)
            self.assertLess(z, 1.0)
            if x < 0.5 and y < 0.6 and z < 0.7:
                bucket += 1
        self.assertClose(bucket / n, 0.5 * 0.6 * 0.7, delta=0.01)

        bucket = 0
        for _ in range(n):
            x, y, z = Vector.rand_box(
                min=(1.0, 2.0, 3.0), max=(4.0, 5.0, 6.0), generator=rng
            )
            self.assertGreaterEqual(x, 1.0)
            self.assertLess(x, 4.0)
            self.assertGreaterEqual(y, 2.0)
            self.assertLess(y, 5.0)
            self.assertGreaterEqual(z, 3.0)
            self.assertLess(z, 6.0)
            if x < 2.0 and y < 3.0 and z < 4.0:
                bucket += 1
        self.assertClose(bucket / n, 1 / 27, delta=0.01)

    def test_rand_sphere(self) -> None:
        n = 10000

        self.assertNotEqual(Vector.rand_sphere()[0], Vector.rand_sphere()[0])

        xyz1 = Vector.rand_sphere(generator=random.Random(123))
        xyz2 = Vector.rand_sphere(generator=random.Random(123))
        self.assertEqual(xyz1[:], xyz2[:])

        bucket1 = 0
        bucket2 = 0
        bucket3 = 0
        rng = random.Random(125)  # 123 did not work :P
        for _ in range(n):
            xyz = Vector.rand_sphere(generator=rng)
            v = Vector(*xyz)
            self.assertClose(v.norm(), 1.0)
            if v[0] > 0.0:
                bucket1 += 1
            if v.dot(Vector(0, 1, 1).normalized()) > 0.0:
                bucket2 += 1
            if v.dot(Vector(-1, -2, -3).normalized()) > 0.0:
                bucket3 += 1
        self.assertClose(bucket1 / n, 0.5, delta=0.01)
        self.assertClose(bucket2 / n, 0.5, delta=0.01)
        self.assertClose(bucket3 / n, 0.5, delta=0.01)

        bucket1 = 0
        bucket2 = 0
        bucket3 = 0
        bucket4 = 0
        rng = random.Random(123)
        for _ in range(n):
            xyz = Vector.rand_sphere(fill=True, generator=rng)
            v = Vector(*xyz)
            self.assertLess(v.norm(), 1.0 - 1e-9)
            if v[0] > 0.0:
                bucket1 += 1
            if v.dot(Vector(0, 1, 1).normalized()) > 0.0:
                bucket2 += 1
            if v.dot(Vector(-1, -2, -3).normalized()) > 0.0:
                bucket3 += 1
            if v.norm() < 0.7:
                bucket4 += 1
        self.assertClose(bucket1 / n, 0.5, delta=0.01)
        self.assertClose(bucket2 / n, 0.5, delta=0.01)
        self.assertClose(bucket3 / n, 0.5, delta=0.01)
        self.assertClose(bucket4 / n, 0.7**3, delta=0.01)

        rng = random.Random(123)
        avg_x, avg_y, avg_z = 0.0, 0.0, 0.0
        for _ in range(n):
            x, y, z = Vector.rand_sphere(
                radius=0.6,
                center=Vector(1, 2, 3),
                fill=rng.random() > 0.5,
                generator=rng,
            )
            v = Vector(x, y, z) - Vector(1, 2, 3)
            self.assertLess(v.norm(), 0.6 + 1e-14)
            avg_x += x / n
            avg_y += y / n
            avg_z += z / n
        self.assertClose(avg_x, 1.0, delta=0.01)
        self.assertClose(avg_y, 2.0, delta=0.01)
        self.assertClose(avg_z, 3.0, delta=0.01)

    def test_equal(self) -> None:
        v1 = Vector(1.0, 2.0, 3.0)
        v2 = Vector(1.0, 2.0, 3.0)
        v3 = Vector(0.0, 2.0, 3.0)
        t = (1.0, 2.0, 3.0)
        s = "abc"
        self.assertEqual(v1, v2)
        self.assertEqual(v1[:], t[:])
        self.assertNotEqual(v1, s)
        self.assertNotEqual(v1, v3)
        self.assertEqual(v1, t)  # LSP demands this if Vectors inherit from NamedTuple
        self.assertEqual(t, v1)  # LSP demands this if Vectors inherit from NamedTuple

    def test_add_sub_neg(self) -> None:
        v1 = Vector(1.0, 2.0, 3.0)
        v2 = Vector(4.0, 5.0, 6.0)
        self.assertEqual(v1 + v2, Vector(5.0, 7.0, 9.0))
        self.assertEqual(v1 - v2, Vector(-3.0, -3.0, -3.0))
        self.assertEqual(-v1, Vector(-1.0, -2.0, -3.0))
        with self.assertRaises(TypeError):
            _ = v1 + 1  # type: ignore
        with self.assertRaises(TypeError):
            _ = 1 + v1  # type: ignore
        with self.assertRaises(TypeError):
            _ = v1 - 1  # type: ignore
        with self.assertRaises(TypeError):
            _ = 1 - v1  # type: ignore

    def test_mul_div(self) -> None:
        v1 = Vector(1.0, 2.0, 3.0)
        v2 = Vector(4.0, 5.0, 6.0)
        self.assertEqual(v1 * 2.0, Vector(2.0, 4.0, 6.0))
        self.assertEqual(2.0 * v1, Vector(2.0, 4.0, 6.0))
        with self.assertRaises(TypeError):
            _ = v1 * v2  # type: ignore
        with self.assertRaises(TypeError):
            _ = "spoon" * v1  # type: ignore
        self.assertEqual(v1 / 2.0, Vector(0.5, 1.0, 1.5))
        with self.assertRaises(TypeError):
            _ = v1 / v2  # type: ignore
        with self.assertRaises(ZeroDivisionError):
            _ = v1 / 0.0
        with self.assertRaises(TypeError):
            _ = 2.0 / v1  # type: ignore

    def test_dot_cross(self) -> None:
        v1 = Vector(1.0, 2.0, 3.0)
        v2 = Vector(4.0, 5.0, 6.0)
        self.assertEqual(v1.dot(v2), 32.0)
        self.assertEqual(v2.dot(v1), 32.0)
        self.assertEqual(v1.cross(v2), Vector(-3.0, 6.0, -3.0))
        self.assertEqual(v2.cross(v1), Vector(3.0, -6.0, 3.0))

    def test_norms(self) -> None:
        v1 = Vector(1.0, 4.0, 8.0)
        self.assertClose(v1.norm(), 9.0)
        self.assertClose(v1.length(), 9.0)
        self.assertClose(v1.normalized().norm(), 1.0)
        self.assertClose(v1.distance_to(-v1), 18.0)
        v2 = Vector(mu, 4.0 * mu, 8.0 * mu)
        self.assertEqual(v2.norm(), 9.0 * mu)
        self.assertClose(v2.normalized().norm(), 1.0)

    def test_perp(self) -> None:
        v0 = Vector.zero()
        v1 = Vector(1.0, 2.0, 3.0)
        self.assertClose(v1.perp().dot(v1), 0.0)
        self.assertClose(v1.perp().norm(), 1.0)
        v2 = Vector(2.0, 1.0, 3.0)
        self.assertClose(v2.perp().dot(v2), 0.0)
        self.assertClose(v2.perp().norm(), 1.0)
        v3 = Vector(3.0, 2.0, 1.0)
        self.assertClose(v3.perp().dot(v3), 0.0)
        self.assertClose(v3.perp().norm(), 1.0)
        vp12 = v1.perp(v2)
        self.assertClose(vp12.dot(v1), 0.0)
        self.assertClose(vp12.dot(v2), 0.0)
        self.assertClose(vp12.norm(), 1.0)
        with self.assertRaises(ValueError):
            _ = v0.perp()
        with self.assertRaises(ValueError):
            _ = v0.perp(v1)
        with self.assertRaises(ValueError):
            _ = v1.perp(v0)

    def test_make_basis(self) -> None:
        a = Vector(1.0, 2.0, 3.0)
        b = Vector(4.0, 5.0, -6.0)
        x, y, z = Vector.make_basis(a, b)
        self.assertClose(x.angle_to(a), 0.0)
        self.assertClose(x.norm(), 1.0)
        self.assertClose(z.angle_to(a.cross(b)), 0.0)
        self.assertClose(z.norm(), 1.0)
        self.assertClose(y.dot(x), 0.0)
        self.assertClose(y.dot(z), 0.0)
        self.assertClose(y.norm(), 1.0)

    def test_angle(self) -> None:
        v1 = Vector(2.0, 3.0, 4.0)
        v2 = Vector(9.0, 8.0, 7.0)
        ang = math.acos(math.sqrt(2450.0 / 2813.0))
        self.assertClose(v1.angle_to(v2), ang)
        v3 = Vector(1.0, 4.0, 8.0)
        v4 = Vector(1.0 + 1e-15, 4.0, 8.0)
        self.assertClose(v3.angle_to(v4), 1.226e-16, delta=1e-17)

    def test_lerp(self) -> None:
        v1 = Vector(1.0, 2.0, 3.0)
        v2 = Vector(4.0, 5.0, 6.0)
        v3 = v1.lerp(v2, 0.5)
        self.assertEqual(v3, Vector(2.5, 3.5, 4.5))
        v4 = v1.lerp(v2, 0.0)
        self.assertEqual(v4, v1)
        v5 = v1.lerp(v2, 1.0)
        self.assertEqual(v5, v2)
        v6 = v1.lerp(v2, 2.0)
        self.assertEqual(v6, Vector(7.0, 8.0, 9.0))

    def test_mean(self) -> None:
        v1 = Vector(1.0, 2.0, 3.0)
        v2 = Vector(4.0, 5.0, 6.0)
        v3 = Vector(-8.0, 11.0, 0.0)
        vm = Vector.mean([v1, v2, v3])
        self.assertEqual(vm, Vector(-1.0, 6.0, 3.0))
        vwm = Vector.mean([v1, v2, v3], [1.0, 2.0, 3.0])
        self.assertEqual(vwm, Vector(-2.5, 7.5, 2.5))
        with self.assertRaises(ValueError):
            _ = Vector.mean([v1, v2, v3], [1.0, 2.0])
        with self.assertRaises(ValueError):
            _ = Vector.mean([v1, v2, v3], [1.0, 0.0, -1.0])
        with self.assertRaises(ValueError):
            _ = Vector.mean([])

    def test_str_format_repr(self) -> None:
        v = Vector(1.0, 2.0, 3.0)
        self.assertEqual(str(v), "(x=1.0, y=2.0, z=3.0)")
        self.assertEqual(f"{v:2.2f}", "(x=1.00, y=2.00, z=3.00)")
        self.assertEqual(eval(repr(v)), v)

    def test_hash(self) -> None:
        v1 = Vector(1.0, 2.0, 3.0)
        v2 = Vector(1.0, 2.0, 3.0)
        v3 = Vector(4.0, 5.0, 6.0)
        self.assertEqual(hash(v1), hash(v2))
        self.assertNotEqual(hash(v1), hash(v3))


class TestRotation(TestBase):

    def test_init(self) -> None:
        r = Rotation()
        self.assertEqual((r._x, r._y, r._z, r._w), (0.0, 0.0, 0.0, 1.0))
        self.assertEqual(Rotation.identity(), r)

    def test_slots(self) -> None:
        r = Rotation()
        _ = r._x
        _ = r._y
        _ = r._z
        _ = r._w
        with self.assertRaises(AttributeError):
            r.u = 0.1  # type: ignore
        with self.assertRaises(TypeError):
            _ = r[0]  # type: ignore

    def test_immutable(self) -> None:
        r = Rotation()
        with self.assertRaises(AttributeError):
            r._x = 0.1  # type: ignore
        with self.assertRaises(AttributeError):
            del r._x  # type: ignore

    def test_from_quat(self) -> None:
        r1 = Rotation.from_quat(x=0.1, y=0.3, z=-0.3, w=0.9)
        self.assertElementsClose((r1._x, r1._y, r1._z, r1._w), (0.1, 0.3, -0.3, 0.9))
        with self.assertRaises(ValueError):
            _ = Rotation.from_quat(x=1.0, y=2.0, z=3.0, w=4.0)
        with self.assertRaises(ValueError):
            _ = Rotation.from_quat(x=2.0, y=2.0, z=2.0, w=2.0, tolerance=3.0 - 1e-15)
        r2 = Rotation.from_quat(x=2.0, y=2.0, z=2.0, w=2.0, tolerance=3.0)
        self.assertElementsClose((r2._x, r2._y, r2._z, r2._w), (0.5, 0.5, 0.5, 0.5))

    def test_as_quat(self) -> None:
        r = Rotation.from_quat(x=0.1, y=0.3, z=-0.3, w=0.9)
        self.assertElementsClose(r.as_quat("xyzw"), (0.1, 0.3, -0.3, 0.9))
        self.assertElementsClose(r.as_quat("wxyz"), (0.9, 0.1, 0.3, -0.3))
        with self.assertRaises(ValueError):
            _ = r.as_quat("xwyz")  # type: ignore
        with self.assertRaises(TypeError):
            _ = r.as_quat()  # type: ignore

    def test_from_axis_angle(self) -> None:
        r = Rotation.from_axis_angle(Vector(1.0, 2.0, 3.0), 4.0)
        r_expected = Rotation.from_quat(
            x=0.24301995956120354,
            y=0.48603991912240707,
            z=0.7290598786836107,
            w=-0.4161468365471424,
        )
        self.assertRotationsClose(r, r_expected)

    def test_as_axis_angle(self) -> None:
        v = Vector(1.0, 2.0, 3.0)
        phi1 = 0.5
        r = Rotation.from_axis_angle(v, phi1)
        axis, angle = r.as_axis_angle()
        self.assertClose(angle, phi1)
        self.assertElementsClose(axis, v.normalized())
        phi2 = 1e-320
        r = Rotation.from_axis_angle(v, phi2)
        axis, angle = r.as_axis_angle()
        self.assertClose(angle, phi2, delta=phi2 / 100)

        for x in [-1.0, -0.5, 0.0, 0.5, 1.0]:
            for y in [-1.0, -0.5, 0.0, 0.5, 1.0]:
                for z in [-1.0, -0.5, 0.0, 0.5, 1.0]:
                    if x == y == z == 0.0:
                        continue
                    for phi in [a * DEG for a in range(-405, 405, 45)]:
                        v = Vector(x, y, z)
                        r_expected1 = Rotation.from_axis_angle(v, phi)

                        axis1, angle1 = r_expected1.as_axis_angle()
                        self.assertGreaterEqual(angle1, 0.0)
                        self.assertLessEqual(angle1, math.pi)
                        self.assertClose(axis1.norm(), 1.0)
                        r_actual1 = Rotation.from_axis_angle(axis1, angle1)
                        self.assertRotationsClose(r_actual1, r_expected1)

                        x_, y_, z_, w_ = r_expected1.as_quat("xyzw")
                        r_expected2 = Rotation.from_quat(x=-x_, y=-y_, z=-z_, w=-w_)
                        axis2, angle2 = r_expected2.as_axis_angle()
                        self.assertGreaterEqual(angle2, 0.0)
                        self.assertLessEqual(angle2, math.pi)
                        self.assertClose(axis2.norm(), 1.0)
                        r_actual2 = Rotation.from_axis_angle(axis2, angle2)
                        self.assertRotationsClose(r_actual2, r_expected2)

        v = Vector(7.0, 8.0, 9.0)
        r = Rotation.from_axis_angle(v, 0.0)
        axis, angle = r.as_axis_angle()
        self.assertEqual(axis, Vector(1.0, 0.0, 0.0))
        self.assertEqual(angle, 0.0)

        # this test does not work because sin(2*pi) == -2.45e-16
        # r = Rotation.from_axis_angle(v, 2.0 * math.pi)
        # axis, angle = r.as_axis_angle()
        # self.assertEqual(axis, Vector(1.0, 0.0, 0.0))
        # self.assertEqual(angle, 0.0)

        with self.assertRaises(ValueError):
            r = Rotation.from_axis_angle(Vector(0.0, 0.0, 0.0), 0.0)

    def test_from_rotvec(self) -> None:
        r1 = Rotation.from_rotvec(Vector(1.0, 2.0, 3.0))
        r_expected = Rotation.from_quat(
            x=0.2553218600452643,
            y=0.5106437200905286,
            z=0.765965580135793,
            w=-0.29555112749297824,
        )
        self.assertRotationsClose(r1, r_expected)
        r2 = Rotation.from_rotvec(Vector(0.0, 0.0, 0.0))
        self.assertEqual(r2, Rotation())
        r3 = Rotation.from_rotvec(Vector(mu, 2.0 * mu, 4.0 * mu))
        self.assertEqual(r3.as_quat("xyzw"), (mu, 2 * mu, 4 * mu, 1.0))

    def test_as_rotvec(self) -> None:
        v = Vector(0.1, 0.2, 0.3)
        r1 = Rotation.from_rotvec(v)
        rotvec = r1.as_rotvec()
        self.assertElementsClose(rotvec, v)
        v2 = Vector(0.0, 0.0, 0.0)
        r2 = Rotation.from_rotvec(v2)
        self.assertEqual(r2.as_rotvec(), v2)
        r3 = Rotation.from_rotvec(Vector(math.pi - 1e-15, 0.0, 0.0))
        self.assertClose(r3.as_rotvec().x, math.pi)
        r4 = Rotation.from_rotvec(Vector(math.pi + 1e-15, 0.0, 0.0))
        self.assertClose(r4.as_rotvec().x, -math.pi)

    def test_from_matrix(self) -> None:
        q25 = 0.2545584412271571
        q02 = 0.0282842712474619
        q33 = 0.3394112549695428
        q90 = 0.9050966799187807

        mtx = [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
        r0 = Rotation.from_matrix(mtx)
        self.assertRotationsClose(r0, Rotation())
        mtx = [
            [0.768, 0.6, 0.224],
            [-0.6288, 0.64, 0.4416],
            [0.1216, -0.48, 0.8688],
        ]
        r1 = Rotation.from_matrix(mtx)
        self.assertRotationsClose(
            r1,
            Rotation.from_quat(x=-q25, y=q02, z=-q33, w=q90),
        )
        r1T = Rotation.from_matrix(mtx, row_major=False)
        self.assertRotationsClose(r1T, Rotation.from_quat(x=q25, y=-q02, z=q33, w=q90))
        mtx = [
            [0.768, 0.6, 0.224],
            [0.6288, -0.64, -0.4416],
            [-0.1216, 0.48, -0.8688],
        ]
        r2 = Rotation.from_matrix(mtx)
        self.assertRotationsClose(
            r2,
            Rotation.from_quat(x=q90, y=q33, z=q02, w=q25),
        )
        mtx = [
            [-0.768, -0.6, -0.224],
            [-0.6288, 0.64, 0.4416],
            [-0.1216, 0.48, -0.8688],
        ]
        r3 = Rotation.from_matrix(mtx)
        self.assertRotationsClose(
            r3,
            Rotation.from_quat(x=-q33, y=q90, z=q25, w=-q02),
        )
        mtx = [
            [-0.768, -0.6, -0.224],
            [0.6288, -0.64, -0.4416],
            [0.1216, -0.48, 0.8688],
        ]
        r4 = Rotation.from_matrix(mtx)
        self.assertRotationsClose(
            r4,
            Rotation.from_quat(x=-q02, y=-q25, z=q90, w=q33),
        )
        with self.assertRaisesRegex(ValueError, "3x3"):
            _ = Rotation.from_matrix([[0, 0], [0, 0]])
        with self.assertRaisesRegex(ValueError, "3x3"):
            _ = Rotation.from_matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0, 0]])
        with self.assertRaisesRegex(ValueError, "ortho"):
            _ = Rotation.from_matrix([[1, 0, 0], [0, 1, 0], [0, 0.1, 1]])
        with self.assertRaisesRegex(ValueError, "hand"):
            _ = Rotation.from_matrix([[1, 0, 0], [0, 1, 0], [0, 0, -1]])
        with self.assertRaisesRegex(ValueError, "not normalized"):
            _ = Rotation.from_matrix(
                [[1, 2, 3], [4, 5, 6], [7, 8, 9]], check_matrix=False
            )

    def test_as_matrix_and_basis(self) -> None:
        mtx_expected = [
            [0.768, 0.6, 0.224],
            [-0.6288, 0.64, 0.4416],
            [0.1216, -0.48, 0.8688],
        ]
        r = Rotation.from_matrix(mtx_expected)
        mtx_actual = r.as_matrix()
        for row1, row2 in zip(mtx_actual, mtx_expected):
            for v1, v2 in zip(row1, row2):
                self.assertClose(v1, v2)

        mtx_actual2 = r.as_matrix(row_major=False)
        basis = r.basis()
        for i in range(3):
            for j in range(3):
                self.assertClose(mtx_actual2[i][j], mtx_expected[j][i])
                self.assertClose(basis[i][j], mtx_expected[j][i])

    def test_x_y_z(self) -> None:
        sqrt3_2 = math.sqrt(3.0) / 2.0
        self.assertRotationsClose(
            Rotation.x(math.pi / 3.0),
            Rotation.from_quat(x=0.5, y=0.0, z=0.0, w=sqrt3_2),
        )
        self.assertRotationsClose(
            Rotation.y(math.pi / 3.0),
            Rotation.from_quat(x=0.0, y=0.5, z=0.0, w=sqrt3_2),
        )
        self.assertRotationsClose(
            Rotation.z(math.pi / 3.0),
            Rotation.from_quat(x=0.0, y=0.0, z=0.5, w=sqrt3_2),
        )

    def test_compose(self) -> None:
        x = Rotation.x(0.1)
        X = Rotation.x(0.2)
        Y = Rotation.y(0.3)
        y = Rotation.y(0.4)
        z = Rotation.z(0.5)
        Z = Rotation.z(0.6)
        # upper are intrinsic (multiplied from the right), lower are extrinsic (multiplied from the left)
        self.assertRotationsClose(
            Rotation.compose("xXYyzZ", [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]),
            z @ y @ x @ X @ Y @ Z,
        )
        with self.assertRaises(ValueError):
            _ = Rotation.compose("xyz", [0.1, 0.2, 0.3, 0.4])
        with self.assertRaises(ValueError):
            _ = Rotation.compose("xyzö", [0.1, 0.2, 0.3, 0.4])

    def test_euler_orders(self) -> None:
        n = 0
        for a in "xyz":
            for b in "xyz":
                for c in "xyz":
                    if a == b or b == c:
                        continue
                    abc = a + b + c
                    self.assertIn(abc, Rotation._euler_orders)
                    self.assertIn(abc.upper(), Rotation._euler_orders)
                    n += 2
        self.assertEqual(len(Rotation._euler_orders), n)

    def test_from_euler(self) -> None:
        self.assertRotationsClose(
            Rotation.from_euler("xyz", (0.1, 0.2, 0.3)),
            Rotation.compose("xyz", [0.1, 0.2, 0.3]),
        )
        with self.assertRaises(ValueError):
            _ = Rotation.from_euler("xxy", (0.1, 0.2, 0.3))

    def test_as_euler(self) -> None:

        for order in Rotation._euler_orders:
            d = EPS * 2.0
            alphae = [
                -math.pi - 0.1,
                -math.pi + d,
                -1.0,
                0.0,
                1.0,
                math.pi - d,
                math.pi + 0.1,
            ]
            alpha_limits = [-math.pi, math.pi]
            betae = [
                -math.pi / 2.0 - 0.1,
                -math.pi / 2.0 - d,
                -math.pi / 2.0,
                -math.pi / 2.0 + d,
                -1.0,
                0.0,
                1.0,
                math.pi / 2.0 - d,
                math.pi / 2.0,
                math.pi / 2.0 + d,
                math.pi / 2.0 + 0.1,
            ]
            beta_limits = [-math.pi / 2.0, math.pi / 2.0]
            if order[0] == order[2]:  # proper Euler
                betae = [beta + math.pi / 2.0 for beta in betae]
                beta_limits = [0.0, math.pi]
            gammae = alphae
            gamma_limits = [-math.pi, math.pi]

            for alpha in alphae:
                for beta in betae:
                    for gamma in gammae:
                        angles = (alpha, beta, gamma)
                        r = Rotation.from_euler(order, angles)
                        result = r.as_euler(order)

                        expect_round_trip = (
                            alpha_limits[0] < alpha < alpha_limits[1]
                            and beta_limits[0] < beta < beta_limits[1]
                            and gamma_limits[0] < gamma < gamma_limits[1]
                        )

                        if expect_round_trip:
                            # delta=EPS was too small for some cases :(
                            self.assertElementsClose(result, angles, delta=2.0 * EPS)
                        else:
                            r_compare = Rotation.from_euler(order, result)
                            self.assertRotationsClose(r, r_compare, delta=EPS)

        with self.assertRaises(ValueError):
            _ = Rotation().as_euler("xxy")

    def test_ypr(self) -> None:
        ypr = (0.1, 0.2, 0.3)
        r1 = Rotation.from_ypr(*ypr)
        expected = Rotation.from_quat(
            x=0.14357217502739189,
            y=0.10602051106179562,
            z=0.03427079855048210,
            w=0.98334744325635581,
        )
        self.assertRotationsClose(r1, expected)
        result = r1.as_ypr()
        self.assertElementsClose(result, ypr)
        rpy = (0.3, 0.2, 0.1)
        r2 = Rotation.from_rpy(*rpy)
        self.assertRotationsClose(r2, expected)
        result = r2.as_rpy()
        self.assertElementsClose(result, rpy)

    def test_rand(self) -> None:
        n = 10000
        rng = random.Random(123)
        for v in [Vector(1.0, 0.0, 0.0), Vector(0.0, 1.0, 1.0), Vector(1.0, 2.0, 3.0)]:
            bucket1 = 0
            bucket2 = 0
            bucket3 = 0
            for _ in range(n):
                r = Rotation.rand(rng)
                if (r @ v).x > 0.0:
                    bucket1 += 1
                if (r @ v).y > 0.0:
                    bucket2 += 1
                if (r @ v).z > 0.0:
                    bucket3 += 1
            self.assertClose(bucket1 / n, 0.5, delta=0.02)
            self.assertClose(bucket2 / n, 0.5, delta=0.02)
            self.assertClose(bucket3 / n, 0.5, delta=0.02)

    def test_normalize(self) -> None:
        r1 = Rotation.from_quat(x=0.1, y=0.2, z=0.3, w=0.4, tolerance=2.0)
        self.assertRotationNormalized(r1)
        r2 = Rotation.from_quat(x=mu, y=2.0 * mu, z=4.0 * mu, w=0.0, tolerance=2.0)
        self.assertRotationNormalized(r2)
        with self.assertRaises(ValueError):
            _ = Rotation.from_quat(x=1.0, y=2.0, z=3.0, w=4.0)
        with self.assertRaises(ValueError):
            _ = Rotation.from_quat(x=0.0, y=0.0, z=0.0, w=0.0, tolerance=3.0)

    def test_rotate_vector(self) -> None:
        r = Rotation.from_quat(x=-0.62, y=0.1, z=0.34, w=-0.7)
        v = Vector(3, -4, 5)
        result = r._rotate_vector(v)
        expected = [-1.9696, -5.8, -3.5328]
        self.assertElementsClose(result, expected)

    def test_multiply(self) -> None:
        r1 = Rotation.from_quat(x=0.7, y=-0.5, z=0.46, w=-0.22)
        r2 = Rotation.from_quat(x=-0.3, y=0.9, z=0.18, w=0.26)
        result = r1 @ r2
        expected1 = Rotation.from_quat(x=-0.256, y=-0.592, z=0.56, w=0.52)
        self.assertRotationsClose(result, expected1)

        r3 = Rotation.from_quat(x=-0.62, y=0.1, z=0.34, w=-0.7)
        v = Vector(3, -4, 5)
        result2 = r3 @ v
        expected2 = [-1.9696, -5.8, -3.5328]
        for v1, v2 in zip(result2, expected2):
            self.assertClose(v1, v2)

        rng = random.Random(123)
        vectors = [Vector.rand_sphere(generator=rng) for _ in range(10)]
        results = r1 @ vectors
        expecteds = [r1 @ v for v in vectors]

        for v1_, v2_ in zip(results, expecteds):
            self.assertElementsClose(v1_, v2_)

        r = Rotation.from_quat(x=0.7, y=-0.5, z=0.46, w=-0.22)
        for _ in range(60):
            r = r @ r
        self.assertRotationNormalized(r)

        with self.assertRaises(TypeError):
            _ = r1 @ 1  # type: ignore
        with self.assertRaises(TypeError):
            _ = 1 @ r1  # type: ignore

    def test_inverse(self) -> None:
        r = Rotation.from_quat(x=0.1, y=0.3, z=-0.3, w=0.9)
        r_inv = r.inverse()
        self.assertElementsClose(
            (r_inv._x, r_inv._y, r_inv._z, r_inv._w), (-0.1, -0.3, 0.3, 0.9)
        )
        self.assertRotationsClose(r @ r_inv, Rotation())
        self.assertRotationsClose(r_inv @ r, Rotation())
        self.assertRotationsClose(~r, r_inv)

    def test_axis_angle_to(self) -> None:
        r1 = Rotation.from_quat(x=0.1, y=0.3, z=-0.3, w=0.9)
        axis = Vector(1.0, 2.0, 3.0).normalized()
        angle = 0.5
        r2 = Rotation.from_axis_angle(axis, angle) @ r1
        axis2, angle2 = r1.axis_angle_to(r2)
        self.assertClose(angle2, angle)
        self.assertElementsClose(axis2, axis)
        angle22 = r1.angle_to(r2)
        self.assertEqual(angle2, angle22)

    def test_lerp(self) -> None:
        def r(angle: float) -> Rotation:
            return Rotation.compose("XYZXXYZ", [0.1, 0.2, 0.3, angle, 0.4, 0.5, 0.6])

        r0 = r(0.0)
        r03 = r(0.3)
        r1 = r(1.0)
        rpi = r(math.pi)

        self.assertRotationsClose(r0.lerp(r1, 0.3), r03)
        self.assertRotationsClose(r0.lerp(r0, 100), r0)
        self.assertRotationsClose(r0.lerp(r1, 1.0), r1)
        self.assertRotationsClose(r0.lerp(rpi, 2.0), r0)
        self.assertRotationsClose(
            r0.lerp(r(math.pi - 2e-12), 0.5), r(0.5 * math.pi - 1e-12)
        )
        self.assertRotationsClose(
            r0.lerp(r(math.pi + 2e-12), 0.5), r(1.5 * math.pi + 1e-12)
        )

        r0 = Rotation()
        rpi = Rotation.from_quat(x=1.0, y=0.0, z=0.0, w=0.0)
        r05 = r0.lerp(rpi, 0.5)
        delta = r0.axis_angle_to(r05)[1]
        self.assertClose(delta, math.pi / 2.0)

    def test_mean(self) -> None:

        for r0 in [
            Rotation.from_quat(w=0.9, x=0.3, y=-0.3, z=0.1),
            Rotation.from_quat(w=0.1, x=0.9, y=0.3, z=-0.3),
            Rotation.from_quat(w=-0.3, x=0.3, y=0.9, z=0.1),
            Rotation.from_quat(w=0.3, x=-0.3, y=0.1, z=0.9),
        ]:
            spread = []
            n = 5
            for i in range(n):
                phi = i / n * 2 * math.pi
                spread.append(
                    r0
                    @ Rotation.from_axis_angle(
                        Vector(math.cos(phi), math.sin(phi), 0.0), 30.0 * DEG
                    )
                )

            r = Rotation.mean(spread)
            self.assertRotationsClose(r, r0)

        r, report = Rotation.mean(
            spread, return_report=True, epsilon=0.1, max_iterations=30
        )
        self.assertTrue(report.converged)
        self.assertTrue(1 <= report.iterations <= 5)
        self.assertTrue(1e-6 <= report.last_change <= 0.1)

        r, report = Rotation.mean(
            spread, return_report=True, epsilon=1e-12, max_iterations=3
        )
        self.assertFalse(report.converged)
        self.assertEqual(report.iterations, 3)
        self.assertGreater(report.last_change, 1e-12)

        spread = []
        weights = []
        r0 = Rotation.from_euler("xyz", (0.1, 0.2, 0.3))
        n = 5
        for i in range(n):
            phi = i / n * 2 * math.pi
            for _ in range(i + 1):
                spread.append(
                    r0
                    @ Rotation.from_axis_angle(
                        Vector(math.cos(phi), math.sin(phi), 0.0), 30.0 * DEG
                    )
                )
                weights.append(1 / (i + 1))

        r = Rotation.mean(spread, weights)
        self.assertRotationsClose(r, r0)

        qx = Rotation.from_quat(x=1.0, y=0.0, z=0.0, w=0.0)
        qy = Rotation.from_quat(x=0.0, y=1.0, z=0.0, w=0.0)
        # qz = Rotation.from_quat(x=0.0, y=0.0, z=1.0, w=0.0)
        # this is a big todo: if we don't converge because we got stuck,
        # it looks like we converged
        # r, report = Rotation.mean([qx, qy, qz], return_report=True)
        # self.assertFalse(report.converged)

        with self.assertRaises(ValueError):
            _ = Rotation.mean([qx, qy], [1.0])

        with self.assertRaises(ValueError):
            _ = Rotation.mean([])

    def test_rotated_towards(self) -> None:
        r = Rotation.from_quat(x=0.1, y=0.3, z=-0.3, w=0.9)
        pointer = Vector(1.0, 2.0, 3.0)
        point_along = Vector(-7.0, 8.0, -9.0)
        angle = (r @ pointer).angle_to(point_along)
        for f in [-0.1, 0.0, 0.3, 1.0, 1.1]:
            rf = r.rotated_towards(pointer, point_along, f)
            new_global_pointer = rf @ pointer
            angle_to_start = new_global_pointer.angle_to(r @ pointer)
            angle_to_target = new_global_pointer.angle_to(point_along)
            self.assertClose(angle_to_start / angle, abs(f))
            self.assertClose(angle_to_target / angle, abs(1.0 - f))

        r = Rotation()
        point_along = Vector(10.0, 20.0, 30.0)
        r05 = r.rotated_towards(pointer, point_along, 0.5)
        self.assertRotationsClose(r05, r)

        r = Rotation()
        point_along = Vector(-10.0, -20.0, -30.0)
        r05 = r.rotated_towards(pointer, point_along, 0.5)
        new_global_pointer = r05 @ pointer
        angle_to_start = new_global_pointer.angle_to(r @ pointer)
        angle_to_target = new_global_pointer.angle_to(point_along)
        self.assertClose(angle_to_start, 90 * DEG)
        self.assertClose(angle_to_target, 90 * DEG)

        with self.assertRaises(ValueError):
            _ = r.rotated_towards(pointer, Vector.zero())

        with self.assertRaises(ValueError):
            _ = r.rotated_towards(Vector.zero(), point_along)

    def test_equal(self) -> None:
        r1 = Rotation.from_quat(x=0.1, y=0.3, z=-0.3, w=0.9)
        r2 = Rotation.from_quat(x=0.1, y=0.3, z=-0.3, w=0.9)
        r3 = Rotation.from_quat(x=0.0, y=0.3, z=-0.3, w=0.9, tolerance=1.0)
        s = "abc"
        self.assertEqual(r1, r2)
        self.assertNotEqual(r1, s)
        self.assertNotEqual(r1, r3)

    def test_str_format_repr(self) -> None:
        r = Rotation.from_quat(x=4 / 9, y=5 / 9, z=6 / 9, w=2 / 9)
        self.assertEqual(str(r), f"±(x={4/9}, y={5/9}, z={6/9}, w={2/9})")
        self.assertEqual(f"{r:2.2f}", "±(x=0.44, y=0.56, z=0.67, w=0.22)")
        self.assertEqual(eval(repr(r)), r)

    def test_hash(self) -> None:
        def quat_hash(x: float, y: float, z: float, w: float) -> int:
            return hash(Rotation.from_quat(x=x, y=y, z=z, w=w, tolerance=100.0))

        def raw_quat_hash(x: float, y: float, z: float, w: float) -> int:
            return hash(Rotation.__new__(Rotation, x=x, y=y, z=z, w=w))

        self.assertEqual(quat_hash(1, 2, 3, 4), quat_hash(1, 2, 3, 4))
        self.assertNotEqual(quat_hash(1, 2, 3, 4), quat_hash(4, 3, 2, 1))
        self.assertEqual(quat_hash(1, 2, 3, 4), quat_hash(-1, -2, -3, -4))
        self.assertNotEqual(quat_hash(1, 2, 3, 4), quat_hash(1, 2, 3, -4))
        self.assertEqual(quat_hash(1, 0, 0, 0), quat_hash(-1, 0, 0, 0))
        self.assertEqual(quat_hash(0, 1, 0, 0), quat_hash(0, -1, 0, 0))
        self.assertEqual(quat_hash(0, 0, 1, 0), quat_hash(0, 0, -1, 0))
        self.assertEqual(quat_hash(0, 0, 0, 1), quat_hash(0, 0, 0, -1))
        self.assertEqual(
            raw_quat_hash(0.0, 0.0, 0.0, 0.0), raw_quat_hash(0.0, 0.0, 0.0, -0.0)
        )
        self.assertEqual(
            raw_quat_hash(0.0, 0.0, 0.0, 0.0), raw_quat_hash(0.0, 0.0, -0.0, 0.0)
        )
        self.assertEqual(
            raw_quat_hash(0.0, 0.0, 0.0, 0.0), raw_quat_hash(0.0, -0.0, 0.0, 0.0)
        )
        self.assertEqual(
            raw_quat_hash(0.0, 0.0, 0.0, 0.0), raw_quat_hash(-0.0, 0.0, 0.0, 0.0)
        )


class TestTrafo(TestBase):

    def test_init(self) -> None:
        tf = Trafo()
        self.assertEqual(tf.t, Vector())
        self.assertEqual(tf.r, Rotation())
        v = Vector(1.0, 2.0, 3.0)
        r = Rotation.from_quat(x=0.5, y=0.5, z=-0.5, w=0.5)
        tf = Trafo(t=v, r=r)
        self.assertEqual(tf.t, v)
        self.assertEqual(tf.r, r)
        with self.assertRaises(TypeError):
            _ = Trafo(Vector(), Rotation())  # type: ignore
        self.assertEqual(Trafo.identity(), Trafo())

    def test_slots(self) -> None:
        v = Vector()
        r = Rotation()
        tf = Trafo(t=v, r=r)
        self.assertIs(tf.t, v)
        self.assertIs(tf.r, r)
        with self.assertRaises(AttributeError):
            tf.scale = 0.1  # type: ignore

    def test_immutable(self) -> None:
        tf = Trafo()
        with self.assertRaises(AttributeError):
            tf.t = Vector()  # type: ignore
        with self.assertRaises(AttributeError):
            del tf.t  # type: ignore

    def test_from_matrix(self) -> None:

        mtx_rw = [
            [0.768, 0.6, 0.224, 1.0],
            [-0.6288, 0.64, 0.4416, 2.0],
            [0.1216, -0.48, 0.8688, 3.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
        tf1 = Trafo.from_matrix(mtx_rw)

        mtx_cw = [
            [0.768, -0.6288, 0.1216, 0.0],
            [0.6, 0.64, -0.48, 0.0],
            [0.224, 0.4416, 0.8688, 0.0],
            [1.0, 2.0, 3.0, 1.0],
        ]
        tf2 = Trafo.from_matrix(mtx_cw, row_major=False)

        expected = Trafo(
            t=Vector(1.0, 2.0, 3.0),
            r=Rotation.from_matrix([mtx_rw[0][:3], mtx_rw[1][:3], mtx_rw[2][:3]]),
        )

        self.assertTrafosClose(tf1, expected)
        self.assertTrafosClose(tf2, expected)

        with self.assertRaises(ValueError):
            _ = Trafo.from_matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0]])
        with self.assertRaises(ValueError):
            _ = Trafo.from_matrix(
                [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]], row_major=False
            )
        with self.assertRaisesRegex(ValueError, "not normalized"):
            _ = Trafo.from_matrix(
                [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]], check_matrix=False
            )

    def test_as_matrix(self) -> None:
        tf = Trafo(
            t=Vector(1.0, 2.0, 3.0),
            r=Rotation.from_quat(
                x=math.sqrt(2.0) / 2.0,
                y=0.0,
                z=0.0,
                w=math.sqrt(2.0) / 2.0,
            ),
        )
        expected_rw_4x4 = [
            [1.0, 0.0, 0.0, 1.0],
            [0.0, 0.0, -1.0, 2.0],
            [0.0, 1.0, 0.0, 3.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
        expected_rw_3x4 = expected_rw_4x4[0:3]
        expected_cw_4x4 = [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, -1.0, 0.0, 0.0],
            [1.0, 2.0, 3.0, 1.0],
        ]
        expected_cw_3x4 = [col[0:3] for col in expected_cw_4x4]

        actual_rw_4x4 = tf.as_matrix()
        actual_rw_4x4 = [[round(v, 14) for v in row] for row in actual_rw_4x4]
        self.assertEqual(actual_rw_4x4, expected_rw_4x4)

        actual_rw_3x4 = tf.as_matrix(num_rows=3)
        actual_rw_3x4 = [[round(v, 14) for v in row] for row in actual_rw_3x4]
        self.assertEqual(actual_rw_3x4, expected_rw_3x4)

        actual_cw_4x4 = tf.as_matrix(row_major=False)
        actual_cw_4x4 = [[round(v, 14) for v in row] for row in actual_cw_4x4]
        self.assertEqual(actual_cw_4x4, expected_cw_4x4)

        actual_cw_3x4 = tf.as_matrix(num_rows=3, row_major=False)
        actual_cw_3x4 = [[round(v, 14) for v in row] for row in actual_cw_3x4]
        self.assertEqual(actual_cw_3x4, expected_cw_3x4)

    def test_from_dh(self) -> None:
        d = 2.0
        theta = 3.0
        r = 4.0
        alpha = 5.0

        st = math.sin(theta)
        ct = math.cos(theta)
        sa = math.sin(alpha)
        ca = math.cos(alpha)

        expected = Trafo.from_matrix(
            [
                [ct, -st * ca, st * sa, r * ct],
                [st, ct * ca, -ct * sa, r * st],
                [0.0, sa, ca, d],
            ]
        )

        actual = Trafo.from_dh(d=d, theta=theta, r=r, alpha=alpha)
        self.assertTrafosClose(actual, expected)

        with self.assertRaises(ValueError):
            _ = Trafo.from_dh(r=1.0, a=1.0)  # type: ignore
        with self.assertRaises(ValueError):
            _ = Trafo.from_dh(d=1.0, s=1.0)  # type: ignore
        with self.assertRaises(TypeError):
            _ = Trafo.from_dh(1.0, 2.0, 3.0, 4.0)  # type: ignore

    def test_look_at(self) -> None:

        # target is a point

        eye = Vector(1.0, 2.0, 3.0)
        look_axis = Vector(0.4, 0.5, 0.6)
        look_at = Vector(4.0, 5.0, -6.0)
        up_axis = Vector(0.7, -0.8, 0.9)
        up = Vector(7.0, 8.0, 9.0)

        tf = Trafo.look_at(
            eye=eye, look_axis=look_axis, look_at=look_at, up_axis=up_axis, up=up
        )

        self.assertEqual(tf.t, eye)
        self.assertClose((tf.r @ look_axis).angle_to(look_at - eye), 0.0)
        # angle between up_axis and up should be minimal
        up_delta_mid = (tf.r @ up_axis).angle_to(up)
        rot_left = Rotation.from_axis_angle(look_at - eye, -0.001) @ tf.r
        up_delta_left = (rot_left @ up_axis).angle_to(up)
        rot_right = Rotation.from_axis_angle(look_at - eye, 0.001) @ tf.r
        up_delta_right = (rot_right @ up_axis).angle_to(up)

        self.assertLess(up_delta_mid, up_delta_left)
        self.assertLess(up_delta_mid, up_delta_right)

        # target is a direction

        look_along = Vector(0.4, 0.5, 0.6)

        tf = Trafo.look_at(
            eye=eye,
            look_axis=look_axis,
            look_along=look_along,
            up_axis=up_axis,
            up=up,
        )

        self.assertClose((tf.r @ look_axis).angle_to(look_along), 0.0)
        up_delta_mid = (tf.r @ up_axis).angle_to(up)
        rot_left = Rotation.from_axis_angle(look_along, -0.001) @ tf.r
        up_delta_left = (rot_left @ up_axis).angle_to(up)
        rot_right = Rotation.from_axis_angle(look_along, 0.001) @ tf.r
        up_delta_right = (rot_right @ up_axis).angle_to(up)

        self.assertLess(up_delta_mid, up_delta_left)
        self.assertLess(up_delta_mid, up_delta_right)

        with self.assertRaises(ValueError):
            _ = Trafo.look_at(
                eye=eye,
                look_axis=Vector.zero(),  # view axis must not be zero
                look_along=look_along,
                up_axis=up_axis,
                up=up,
            )
        with self.assertRaises(ValueError):
            _ = Trafo.look_at(
                eye=eye,
                look_axis=look_axis,
                look_along=look_along,
                up_axis=Vector.zero(),  # up axis must not be zero
                up=up,
            )
        with self.assertRaises(ValueError):
            _ = Trafo.look_at(
                eye=eye,
                look_axis=Vector.ex(),  # view axis must not be parallel/anti-parallel to up axis
                look_along=look_along,
                up_axis=-Vector.ex(),
                up=up,
            )
        with self.assertRaises(ValueError):
            _ = Trafo.look_at(  # type: ignore
                eye=eye,
                look_axis=look_axis,
                look_at=look_along,  # both look_at
                look_along=look_along,  # as well as look_along provided
                up_axis=up_axis,
                up=up,
            )
        with self.assertRaises(ValueError):
            _ = Trafo.look_at(  # type: ignore
                eye=eye,
                look_axis=look_axis,
                # neither look_at nor look_along provided
                up_axis=up_axis,
                up=up,
            )

        self.assertEqual(
            Trafo.look_at(
                eye=eye,
                look_axis=look_axis,
                look_at=eye,  # eye and target are equal
                up_axis=up_axis,
                up=up,
            ),
            Trafo(t=eye),
        )

        tf = Trafo.look_at(
            eye=eye,
            look_axis=look_axis,
            look_along=look_along,
            up_axis=up_axis,
            up=Vector.zero(),  # up vector is zero
        )
        self.assertClose((tf.r @ look_axis).angle_to(look_along), 0.0)

        tf = Trafo.look_at(
            eye=eye,
            look_axis=look_axis,
            look_along=look_along,
            up_axis=up_axis,
            up=-look_along,  # up vector is parallel to target vector
        )
        self.assertClose((tf.r @ look_axis).angle_to(look_along), 0.0)

    def test_multiply(self) -> None:
        tf1 = Trafo(
            t=Vector(1.1, 1.2, 1.3),
            r=Rotation.from_quat(x=0.7, y=-0.5, z=0.46, w=-0.22),
        )
        tf2 = Trafo(
            t=Vector(2.1, 2.2, 2.3),
            r=Rotation.from_quat(x=-0.62, y=0.1, z=0.34, w=-0.7),
        )
        result1 = tf1 @ tf2
        self.assertIsInstance(result1, Trafo)
        self.assertTrafosClose(
            result1,
            Trafo(
                t=Vector(2.15376, -1.93168, -0.6032),
                r=Rotation.from_quat(x=-0.5696, y=-0.1952, z=-0.6368, w=0.4816),
            ),
        )

        direction = Vector(3.0, -4.0, 5.0)
        result2 = tf1.r @ direction
        self.assertIsInstance(result2, Vector)
        expected = [6.5408, -1.8544, 1.944]
        self.assertElementsClose(result2, expected)
        with self.assertRaises(TypeError):
            _ = direction @ tf1.r  # type: ignore

        point = Vector(3.0, -4.0, 5.0)
        result3 = tf1 @ point
        self.assertIsInstance(result3, Vector)
        expected = [7.6408, -0.6544, 3.244]
        self.assertElementsClose(result3, expected)
        with self.assertRaises(TypeError):
            _ = point @ tf1  # type: ignore

        r = Rotation.from_quat(x=-0.62, y=0.1, z=0.34, w=-0.7)
        result4 = tf1.r @ r
        self.assertIsInstance(result4, Rotation)
        TestRotation().assertRotationsClose(
            result4, Rotation.from_quat(x=-0.5696, y=-0.1952, z=-0.6368, w=0.4816)
        )

        rng = random.Random(123)
        vectors = [Vector.rand_sphere(generator=rng) for _ in range(10)]
        results = tf1 @ vectors
        expecteds = [tf1 @ v for v in vectors]

        for v1_, v2_ in zip(results, expecteds):
            self.assertElementsClose(v1_, v2_)

        with self.assertRaises(TypeError):
            _ = point @ tf1  # type: ignore
        with self.assertRaises(TypeError):
            _ = tf1 @ r  # type: ignore
        with self.assertRaises(TypeError):
            _ = tf1 @ "(ツ)"  # type: ignore

    def test_inverse(self) -> None:
        tf = Trafo(
            t=Vector(1.0, 2.0, 3.0),
            r=Rotation.from_quat(x=0.1, y=0.3, z=-0.3, w=0.9),
        )
        tf_inv = tf.inverse()
        self.assertTrafosClose(tf @ tf_inv, Trafo())
        self.assertTrafosClose(tf_inv @ tf, Trafo())
        self.assertTrafosClose(~tf, tf_inv)

    def test_lerp(self) -> None:
        tf0 = Trafo(
            t=Vector(1.0, 2.0, 3.0),
            r=Rotation.from_quat(x=0.1, y=0.3, z=-0.3, w=0.9),
        )
        tf1 = Trafo(
            t=Vector(2.0, 3.0, 4.0),
            r=Rotation.from_quat(x=-0.1, y=-0.3, z=0.3, w=0.9),
        )
        tf05 = Trafo(
            t=Vector(1.5, 2.5, 3.5),
            r=Rotation.from_quat(x=0.0, y=0.0, z=0.0, w=1.0),
        )
        self.assertTrafosClose(tf0.lerp(tf1, 0.5), tf05)

    def test_mean(self) -> None:

        tf1 = Trafo(
            t=Vector(2.0, 3.0, 4.0),
            r=Rotation.from_axis_angle(Vector(1.0, 2.0, 3.0), 20.0 * DEG),
        )
        tf2 = Trafo(
            t=Vector(3.0, -4.0, 5.0),
            r=Rotation.from_axis_angle(Vector(1.0, 2.0, 3.0), 30.0 * DEG),
        )
        result = Trafo.mean([tf1, tf1, tf2], [1, 1, 2])
        self.assertTrafosClose(
            result,
            Trafo(
                t=Vector(2.5, -0.5, 4.5),
                r=Rotation.from_axis_angle(Vector(1.0, 2.0, 3.0), 25.0 * DEG),
            ),
        )

    def test_rotated_towards(self) -> None:
        tf = Trafo(
            t=Vector(1.0, 2.0, 3.0),
            r=Rotation.from_quat(x=0.1, y=0.3, z=-0.3, w=0.9),
        )
        pointer = Vector(3.0, -1.0, 4.0)

        point_along = Vector(-7.0, 8.0, -9.0)
        rtf = tf.rotated_towards(pointer, point_along=point_along)
        self.assertClose((rtf.r @ pointer).angle_to(point_along), 0.0)

        point_at = Vector(-7.0, 8.0, -9.0)
        rtf = tf.rotated_towards(pointer, point_at=point_at)
        point_along = point_at - tf.t
        self.assertClose((rtf.r @ pointer).angle_to(point_along), 0.0)

        with self.assertRaises(ValueError):
            _ = tf.rotated_towards(  # type: ignore
                pointer, point_at=point_at, point_along=point_along
            )
        with self.assertRaises(ValueError):
            _ = tf.rotated_towards(pointer)  # type: ignore

    def test_equal(self) -> None:
        tf1 = Trafo(
            t=Vector(1.0, 2.0, 3.0),
            r=Rotation.from_quat(x=0.1, y=0.3, z=-0.3, w=0.9),
        )
        tf2 = Trafo(
            t=Vector(1.0, 2.0, 3.0),
            r=Rotation.from_quat(x=0.1, y=0.3, z=-0.3, w=0.9),
        )
        tf3 = Trafo(
            t=Vector(1.0, 2.0, 3.0),
            r=Rotation.from_quat(x=-0.1, y=-0.3, z=0.3, w=-0.9),
        )
        tf4 = Trafo(
            t=Vector(1.0, 2.0, 3.0),
            r=Rotation.from_quat(x=-0.1, y=-0.3, z=0.3, w=-0.9),
        )
        self.assertEqual(tf1, tf2)
        self.assertEqual(tf1, tf3)
        self.assertEqual(tf1, tf4)
        self.assertNotEqual(tf1, Vector())

    def test_str_format_repr(self) -> None:
        tf = Trafo(
            t=Vector(1.0, 2.0, 3.0),
            r=Rotation.from_quat(x=-0.5, y=0.5, z=-0.5, w=0.5),
        )
        self.assertEqual(
            str(tf), "(t=(x=1.0, y=2.0, z=3.0), r=±(x=-0.5, y=0.5, z=-0.5, w=0.5))"
        )
        self.assertEqual(
            f"{tf:2.2f}",
            "(t=(x=1.00, y=2.00, z=3.00), r=±(x=-0.50, y=0.50, z=-0.50, w=0.50))",
        )
        self.assertEqual(eval(repr(tf)), tf)

    def test_hash(self) -> None:
        tf1 = Trafo(
            t=Vector(1.0, 2.0, 3.0),
            r=Rotation.from_quat(x=0.1, y=0.3, z=0.3, w=0.9),
        )
        tf2 = Trafo(
            t=Vector(1.0, 2.0, 3.0),
            r=Rotation.from_quat(x=-0.1, y=-0.3, z=-0.3, w=-0.9),  # quat is negated
        )
        tf3 = Trafo(
            t=Vector(1.0, 2.0, 3.0),
            r=Rotation.from_quat(x=0.0, y=0.0, z=0.0, w=1.0),  # x is 0
        )
        tf4 = Trafo(
            t=Vector(0.0, 2.0, 3.0),  # x is 0
            r=Rotation.from_quat(x=0.1, y=0.3, z=0.3, w=0.9),
        )
        self.assertEqual(hash(tf1), hash(tf2))
        self.assertNotEqual(hash(tf1), hash(tf3))
        self.assertNotEqual(hash(tf1), hash(tf4))


class TestNode(TestBase):
    def test_init_and_getters(self) -> None:
        world = Node(None, Trafo(), "world")
        tf = Trafo()
        n = Node(world, tf)
        self.assertIs(n.get_parent(), world)
        self.assertIs(n.trafo, tf)
        self.assertEqual(n.label, "")
        self.assertEqual(n.get_children(), [])
        self.assertIn(n, world.get_children())

        n = Node(None, tf, "myNode")
        self.assertIs(n.get_parent(), None)
        self.assertEqual(n.label, "myNode")

    def test_slots(self) -> None:
        n = Node(None, Trafo(), "myNode")
        n.label = "newLabel"
        self.assertEqual(n.label, "newLabel")
        tf2 = Trafo()
        n.trafo = tf2
        self.assertIs(n.trafo, tf2)
        with self.assertRaises(AttributeError):
            n.scale = 0.1  # type: ignore

    def test_attach(self) -> None:
        world = Node(None, Trafo(), "world")
        tf1 = Trafo(t=Vector(x=1.0))
        tf2 = Trafo(t=Vector(y=2.0))
        n1 = Node(world, tf1, "n1")
        n2 = Node(n1, tf2, "n2")
        self.assertIs(n2.get_parent(), n1)
        self.assertEqual(n1.get_children(), [n2])
        with self.assertRaisesRegex(ValueError, "cycle"):
            n1.attach_to(n1)
        with self.assertRaisesRegex(ValueError, "cycle"):
            n1.attach_to(n2)
        n2.attach_to(None)
        self.assertIs(n2.get_parent(), None)
        self.assertEqual(n1.get_children(), [])
        n1.attach_to(n2)
        self.assertIs(n1.get_parent(), n2)
        self.assertEqual(n2.get_children(), [n1])
        self.assertIs(n1.trafo, tf1)
        self.assertIs(n2.trafo, tf2)
        n1.attach_to(world)
        n2.attach_to(world)
        n2.attach_to(n1, keep_relative_trafo=True)
        self.assertIsNot(n2.trafo, tf2)
        self.assertEqual(n2.trafo, Trafo(t=Vector(x=-1.0, y=2.0)))

    def test_relative_trafo(self) -> None:
        world = Node(None, Trafo(), "world")
        na1 = Node(world, Trafo(t=Vector(x=1.0)), "na1")
        na2 = Node(na1, Trafo(t=Vector(y=2.0)), "na2")
        na3 = Node(na2, Trafo(t=Vector(z=3.0)), "na3")
        na3_ = Node(na2, Trafo(t=Vector(z=-3.0)), "na3_")
        nb1 = Node(world, Trafo(t=Vector(x=10.0)), "nb1")
        nb2 = Node(nb1, Trafo(t=Vector(y=20.0)), "nb2")
        nb3 = Node(nb2, Trafo(t=Vector(z=30.0)), "nb3")
        nc1 = Node(None, Trafo(), "nc1")
        nc2 = Node(nc1, Trafo(), "nc2")

        self.assertEqual(world >> na1, na1.trafo)
        self.assertEqual(na1 >> na1, Trafo())
        self.assertEqual(na1 >> world, Trafo(t=Vector(x=-1.0)))
        self.assertEqual(na1 >> na2, Trafo(t=Vector(y=2.0)))
        self.assertEqual(na1 >> na3, Trafo(t=Vector(y=2.0, z=3.0)))
        self.assertEqual(na3 >> nb3, Trafo(t=Vector(x=9.0, y=18.0, z=27.0)))
        self.assertEqual(na3 >> na3_, Trafo(t=Vector(z=-6.0)))

        with self.assertRaisesRegex(ValueError, "not connected"):
            _ = world >> nc1
        with self.assertRaisesRegex(ValueError, "not connected"):
            _ = na1 >> nc2
        with self.assertRaisesRegex(ValueError, "not connected"):
            _ = na3 >> nc1
        with self.assertRaisesRegex(ValueError, "not connected"):
            _ = na3 >> nc2
        with self.assertRaises(TypeError):
            _ = na1 >> None  # type: ignore
        with self.assertRaises(TypeError):
            _ = None >> na1  # type: ignore


class TestDebugDrawer(TestBase):
    def test_draw(self) -> None:

        class DrawingLogger(DebugDrawer):
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                super().__init__(*args, **kwargs)
                self.log = ""

            def line(self, *args: Any, **kwargs: Any) -> None:
                vals = ", ".join(
                    [repr(a) for a in args]
                    + [f"{k}={repr(v)}" for k, v in kwargs.items()]
                )
                self.log += f"drawer.line({vals})\n"

        logger = DrawingLogger(text_direction=Vector(1, 1, 1))

        def tf(
            x: float, y: float, z: float, roll: float, pitch: float, yaw: float
        ) -> Trafo:
            return Trafo(t=Vector(x, y, z), r=Rotation.from_rpy(roll, pitch, yaw))

        world = Node(None, Trafo(), "world")
        na1 = Node(world, tf(1, 0, 0, 45 * DEG, 0, 0), "na1")
        na2 = Node(na1, tf(0, 1, 0, 0, 45 * DEG, 0), "na2")
        Node(na2, tf(0, 0, 1, 0, 0, 45 * DEG), "na3")
        Node(world, tf(-1, -1, -1, -1, -1, -1), "nb1")
        txtNode = Node(
            None,
            tf(2, 0, 0, 0, 0, 0),
            " !,-.0123456789?ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz#",
        )

        logger.tree(world)
        logger.point(Vector(1, 2, 3))
        logger.vector(Vector(4, 5, 6))
        logger.rotation(Rotation.from_quat(x=0.1, y=0.3, z=0.3, w=0.9))
        logger.trafo(tf(2, 2, 2, 3, 3, 3))
        logger.node(txtNode)

        expected_hash = "fb3692ca"
        actual_hash = deterministic_hash(logger.log)
        if actual_hash != expected_hash:  # pragma: no cover
            print("The hash of the debug draw test log has changed.")
            print("Please inspect the new output and update the expected hash.")
            try:
                import sys
                import os

                sys.path.insert(
                    0,
                    os.path.abspath(
                        os.path.join(os.path.dirname(__file__), "../tools/htmldrawer")
                    ),
                )
                from htmldrawer import HtmlDrawer

                drawer = HtmlDrawer()
                exec(logger.log)
                drawer.export("test_inspection.html")
                print("Check out test_inspection.html!")
            except Exception as e:
                print(
                    f"unable to create html drawing of the debug draw test scene:\n{e}"
                )
                print("Here is the raw method call log:")
                print(logger.log)

            print(f"hash: {actual_hash}")
        self.assertEqual(expected_hash, actual_hash)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
