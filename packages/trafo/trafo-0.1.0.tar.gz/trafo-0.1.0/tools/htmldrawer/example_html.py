from trafo import Vector, Trafo, Node, DEG
from htmldrawer import HtmlDrawer
import random
from math import pi

hd = HtmlDrawer(arrow_length=0.3)

hd.line(Vector(-1, 0, 0), Vector(1, 0, 0), "default")
hd.line(Vector(0, -1, 0), Vector(0, 1, 0), "default")
hd.line(Vector(0, 0, -1), Vector(0, 0, 1), "default")
hd.line(Vector(1, 1, 1), Vector(-1, -1, 1), "red")
hd.line(Vector(1, 1, 1), Vector(-1, 1, -1), "yellow")
hd.line(Vector(1, 1, 1), Vector(1, -1, -1), "lime")
hd.line(Vector(-1, -1, 1), Vector(1, -1, -1), "cyan")
hd.line(Vector(-1, 1, -1), Vector(-1, -1, 1), "royalblue")
hd.line(Vector(1, -1, -1), Vector(-1, 1, -1), "magenta")
hd.export("lines.html", "Lines")

for _ in range(100):
    x, y, z = random.gauss(0, 1), random.gauss(0, 1), random.gauss(0, 1)
    r, g, b = x * 0.5 + 0.5, y * 0.5 + 0.5, z * 0.5 + 0.5
    r, g, b = max(0, min(1, r)), max(0, min(1, g)), max(0, min(1, b))
    hd.arrow(Vector(x / 2, y / 2, z / 2), Vector(x, y, z), (r, g, b))
hd.export("arrows.html", "Arrows")

for ix in range(11):
    for iy in range(11):
        for iz in range(11):
            x, y, z = ix / 5, iy / 5, iz / 5
            hd.point(Vector(x - 1, y - 1, z - 1), color=(x / 2, y / 2, z / 2))
hd.export("points.html", "Points")

for code in range(0x2200, 0x2300):
    p = (
        Vector()
        + Vector(
            random.gauss(0, 1), random.gauss(0, 1), random.gauss(0, 1)
        ).normalized()
    )
    hd.text(p, chr(code))
hd.export("text.html", "Text")


def dh(a: float, alpha: float, d: float, theta: float) -> Trafo:
    return Trafo.from_dh(a=a, alpha=alpha, d=d, theta=theta)


joints = [-45 * DEG, -10 * DEG, -20 * DEG, 30 * DEG, -90 * DEG, 30 * DEG]
base = Node(None, Trafo(), "Base")
shoulder = Node(base, dh(0.4, pi / 2, 0.4, joints[0]), "Shoulder")
upper_arm = Node(shoulder, dh(1.5, 0, 0, pi / 2 + joints[1]), "Upper Arm")
forearm = Node(upper_arm, dh(0.2, pi / 2, 0, joints[2]), "Forearm")
wrist = Node(forearm, dh(0, -pi / 2, 1.5, joints[3]), "Wrist")
hand = Node(wrist, dh(0, pi / 2, 0, joints[4]), "Hand")
flange = Node(hand, dh(0, 0, 0.2, joints[5]), "Flange")
hd.tree(base)
hd.export("tree.html", "Tree")


base = Node(None, Trafo(), "Base")
shoulder = Node(base, dh(0.4, pi / 2, 0.4, joints[0]), "Shoulder")
upper_arm = Node(shoulder, dh(1.5, 0, 0, pi / 2 + joints[1]), "Upper Arm")
forearm = Node(upper_arm, dh(0.2, pi / 2, 0, joints[2]), "Forearm")
wrist = Node(forearm, dh(0, -pi / 2, 1.5, joints[3]), "Wrist")
hand = Node(wrist, dh(0, pi / 2, 0, joints[4]), "Hand")
flange = Node(hand, dh(0, 0, 0.2, joints[5]), "Flange")
hd.tree(base)
hd.export("tree.html", "Tree")
