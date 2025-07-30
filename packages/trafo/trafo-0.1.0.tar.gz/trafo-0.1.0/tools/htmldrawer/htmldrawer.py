from typing import Union, Tuple, List, Any
from trafo import Vector, Rotation, Trafo, Node, DebugDrawer
import os
import json

template_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "viewer_template.html"
)
with open(template_file, "r") as file:
    html_template = file.read()


class HtmlDrawer(DebugDrawer):
    """
    An implementation of the DebugDrawer which generates an interactive
    HTML document.
    """

    Json = Any

    # also allow css color names and rgb values (range 0.0..1.0)
    Color = Union[DebugDrawer.Color, str, Tuple[float, float, float]]

    def __init__(
        self,
        up: Vector = Vector.ez(),
        arrow_length: float = 1.0,
        font_size: float = 0.1,
    ):
        super().__init__(up=up, arrow_length=arrow_length, font_size=font_size)
        self._buffer: List[Any] = []

    class _Frame:
        """
        _Frame Allows for elements to have a scope so that the document
        can be aware e.g. what coordinate system some arrow belongs to.
        This is important for the random shifting function,
        so that elements that belong together get the same random shift.
        """

        def __init__(self, drawer: "HtmlDrawer", type_: str) -> None:
            self.drawer = drawer
            self.type_ = type_

        def __enter__(self) -> None:
            self.outer = self.drawer._buffer
            self.drawer._buffer = []

        def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
            children = self.drawer._buffer
            self.drawer._buffer = self.outer
            self.drawer._append(self.type_, {"children": children})

    def _frame(self, type_: str) -> _Frame:
        """Open a new frame to which new elements will be appended."""
        return HtmlDrawer._Frame(self, type_)

    def _append(self, type_: str, kwargs: Any) -> None:
        """Append an element to the currently open frame."""
        if "self" in kwargs:
            kwargs.pop("self")
        self._buffer.append({"type": type_, **kwargs})

    def line(
        self, start: Vector, end: Vector, color: Color = "default", width: float = 2.0
    ) -> None:
        """Draw a line."""
        self._append("line", locals())

    def text(self, position: Vector, text: str, color: Color = "default") -> None:
        """Draw text at a position."""
        self._append("text", locals())

    def arrow(
        self, start: Vector, end: Vector, color: Color = "default", width: float = 2.0
    ) -> None:
        """Draw an arrow."""
        self._append("arrow", locals())

    def point(
        self, position: Vector, color: Color = "default", width: float = 4.0
    ) -> None:
        """Draw a point."""
        self._append("point", locals())

    def rotation(self, rotation: Rotation) -> None:
        """Draw a rotation as a rotated coordinate frame."""
        with self._frame("rotation"):
            super().rotation(rotation)

    def trafo(self, trafo: Trafo) -> None:
        """Draw a transformation as a transformed coordinate frame."""
        with self._frame("trafo"):
            super().trafo(trafo)

    def node(self, node: Node, offset: Trafo = Trafo()) -> None:
        """Draw a node - a Trafo with an arrow from the origin and a label;
        origin and Trafo can be shifted by offset."""
        with self._frame("node"):
            super().node(node, offset)

    def tree(self, root: Node, offset: Trafo = Trafo()) -> None:
        """Draw a tree of Trafos starting at the root node, shifted by offset."""
        with self._frame("tree"):
            super().tree(root, offset)

    def export(
        self, file: str, title: str = "trafo", clear: bool = True, precision: int = 6
    ) -> None:
        """Export the current scene as an html document."""

        def round_floats(o: Any) -> Any:
            if isinstance(o, float):
                return round(o, precision)
            if isinstance(o, dict):
                return {k: round_floats(v) for k, v in o.items()}
            if isinstance(o, (list, tuple)):
                return [round_floats(x) for x in o]
            return o

        html = html_template.replace("/*TITLE*/", title)
        html = html.replace(
            "/*SCENE_DEFINITION*/",
            f"const scene = {json.dumps(round_floats(self._buffer))};\n",
        )
        up_n = self.up.normalized()
        html = html.replace(
            "/*CAMERA_UP*/",
            f"const CAMERA_UP = [{up_n.x}, {up_n.y}, {up_n.z}];",
        )

        with open(file, "w") as f:
            f.write(html)
        if clear:
            self.clear()

    def clear(self) -> None:
        """Flush the drawing buffer and begin a new scene."""
        self._buffer = []
