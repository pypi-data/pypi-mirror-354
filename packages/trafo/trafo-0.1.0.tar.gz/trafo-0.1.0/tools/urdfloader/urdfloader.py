import xml.etree.ElementTree as ET
from typing import Dict, Tuple, Optional
from trafo import Vector, Rotation, Trafo, Node


class Joint:
    def __init__(
        self,
        name: str,
        parent: str,
        child: str,
        origin: Trafo,
        joint_type: str,
        axis: Vector,
    ) -> None:
        self.name = name
        self.parent = parent
        self.child = child
        self.origin = origin
        self.joint_type = joint_type
        self.axis = axis
        self.trafo = Trafo()
        self.node = Node(parent=None, trafo=origin, label=name)

    def set_value(self, value: float | Vector | Trafo) -> None:
        if self.joint_type in ["revolute", "continuous"]:
            assert isinstance(value, float), "Revolute joint value must be a float"
            self.trafo = Trafo(r=Rotation.from_axis_angle(self.axis, value))
        elif self.joint_type == "prismatic":
            assert isinstance(value, float), "Prismatic joint value must be a float"
            self.trafo = Trafo(t=Vector(*self.axis) * value)
        elif self.joint_type == "planar":
            assert isinstance(value, Vector), "Planar joint value must be a Vector"
            assert (
                abs(self.axis.dot(value)) < 1e-9
            ), "Planar joint value vector must be perpendicular to axis"
            self.trafo = Trafo(t=value)
        elif self.joint_type == "floating":
            assert isinstance(value, Trafo), "Floating joint value must be a Trafo"
            self.trafo = value
        elif self.joint_type == "fixed":
            raise ValueError("Fixed joint cannot be updated")
        else:
            raise ValueError(f"Unknown joint type: {self.joint_type}")
        self.node.trafo = self.origin @ self.trafo


def load_urdf(filename: str) -> Tuple[Node, Dict[str, Joint]]:

    def get_attrib_str(elem: ET.Element, attrib: str) -> str:
        value = elem.attrib.get(attrib)
        assert isinstance(value, str)
        return value

    def get_child_attrib_str(elem: ET.Element, child: str, attrib: str) -> str:
        child_elem = elem.find(child)
        assert isinstance(child_elem, ET.Element)
        return get_attrib_str(child_elem, attrib)

    link_parents: Dict[str, Optional[Joint]] = {}

    tree = ET.parse(filename)
    xml_root = tree.getroot()

    for link in xml_root.findall("link"):
        name = link.attrib.get("name")
        assert isinstance(name, str)
        link_parents[name] = None

    joints: Dict[str, Joint] = {}
    for joint_xml in xml_root.findall("joint"):
        joint_type = get_attrib_str(joint_xml, "type")
        name = get_attrib_str(joint_xml, "name")
        parent = get_child_attrib_str(joint_xml, "parent", "link")
        child = get_child_attrib_str(joint_xml, "child", "link")

        origin_xml = joint_xml.find("origin")
        if origin_xml is None:
            origin = Trafo()
        else:
            xyz_str = get_attrib_str(origin_xml, "xyz")
            rpy_str = get_attrib_str(origin_xml, "rpy")
            xyz = [float(v) for v in xyz_str.split()] if xyz_str else [0, 0, 0]
            rpy = [float(v) for v in rpy_str.split()] if rpy_str else [0, 0, 0]
            origin = Trafo(t=Vector(*xyz), r=Rotation.from_rpy(*rpy))

        axis_xml = joint_xml.find("axis")
        if axis_xml is None:
            axis = Vector(1, 0, 0)
        else:
            axis_str = get_attrib_str(axis_xml, "xyz")
            axis_list = [float(v) for v in axis_str.split()] if axis_str else [1, 0, 0]
            axis = Vector(*axis_list)

        assert (
            parent in link_parents
        ), f"Parent link {parent} of joint {name} not found in link_parents"
        assert (
            child in link_parents
        ), f"Child link {child} of joint {name} not found in link_parents"

        joint = Joint(name, parent, child, origin, joint_type, axis)

        assert (
            link_parents[child] is None
        ), f"Child link {parent} of joint {name} already has parent {link_parents[child]}"
        link_parents[child] = joint

        assert name not in joints, f"Joint {name} already exists"
        joints[name] = joint

    root_link: Optional[str] = None
    for link, parent_joint in link_parents.items():
        if parent_joint is None:
            assert (
                root_link is None
            ), f"Multiple root links found: {root_link} and {link}"
            root_link = link

    robot_name = xml_root.attrib.get("name", "UnnamedRobot")
    root_node = Node(label=robot_name)
    for joint in joints.values():
        parent_joint = link_parents[joint.parent]
        if parent_joint is None:
            joint.node.attach_to(root_node)
        else:
            joint.node.attach_to(parent_joint.node)

    return root_node, joints


if __name__ == "__main__":
    import sys
    import os

    sys.path.append(f"{os.path.dirname(__file__)}/../htmldrawer")

    from htmldrawer import HtmlDrawer
    import webbrowser

    if len(sys.argv) < 3:
        print(
            f"Usage: python {sys.argv[0]} <input_file.urdf> <output_file.html> [<joint_value> | <joint_name=value> ...]"
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    joint_values = sys.argv[3:]

    root_node, joints = load_urdf(input_file)

    for index, arg in enumerate(joint_values):
        joint_name, value = arg.split("=")
        joints[joint_name].set_value(float(value))

    hd = HtmlDrawer(arrow_length=0.1)
    hd.tree(root_node)
    hd.export(output_file, root_node.label)
    webbrowser.open(f"file://{os.path.abspath(output_file)}")
