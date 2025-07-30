from urdfloader import load_urdf
from trafo import Vector, Trafo, Rotation
import webbrowser
import sys
import os

sys.path.append(f"{os.path.dirname(__file__)}/../htmldrawer")
from htmldrawer import HtmlDrawer  # noqa: E402


root_node, joints = load_urdf("test.urdf")

joints["revolute_joint"].set_value(0.5)
joints["continuous_joint"].set_value(0.5)
joints["prismatic_joint"].set_value(0.5)
joints["planar_joint"].set_value(Vector(0.0, 0.5, 0.5))
joints["floating_joint"].set_value(
    Trafo(t=Vector(0.5, 0.5, 0.5), r=Rotation.from_rpy(0.5, 0.5, 0.5))
)

hd = HtmlDrawer(arrow_length=0.1)
hd.tree(root_node)
hd.export("test.html", root_node.label)
webbrowser.open("test.html")
