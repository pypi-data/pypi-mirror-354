import math
from dataclasses import field
from typing import Annotated, ClassVar, Literal, Optional
from uuid import UUID

import numpy as np
from pydantic.dataclasses import dataclass

from edea.kicad._config import pydantic_config
from edea.kicad._fields import make_meta as m
from edea.kicad._str_enum import StrEnum
from edea.kicad.common import Effects, Pts, Stroke

from .base import KicadPcbExpr
from .common import (
    BaseTextBox,
    CanonicalLayerName,
    LayerKnockout,
    Position,
    RenderCache,
)


@dataclass(config=pydantic_config, eq=False)
class GraphicalText(KicadPcbExpr):
    """
    A graphical text element.

    `KiCad graphical text <https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_graphical_text>`_

    :param locked: Whether the text can move or not.
    :param text: The content of the text.
    :param at: The X-Y coordinates of the graphical text element.
    :param layer: The canonical layer the text resides on.
    :param effects: The style of the text.
    :param render_cache: Instance of :py:class:`~edea.kicad.common.RenderCache` object.
    :param tstamp: The unique identifier of the text object.
    :param uuid: The unique identifier of the text object.
    :cvar kicad_expr_tag_name: The KiCad expression tag name for this element ("gr_text").

    .. note::
        The `tstamp` field got renamed to `uuid` in 20240108 (KiCad 8).

    """

    locked: Annotated[bool, m("kicad_kw_bool")] = False
    text: Annotated[str, m("kicad_no_kw", "kicad_always_quotes")] = ""
    at: Position = field(default_factory=Position)
    layer: Optional[LayerKnockout] = None
    effects: Effects = field(default_factory=Effects)
    render_cache: Optional[RenderCache] = None
    tstamp: Annotated[Optional[UUID], m("kicad_omits_default")] = None
    uuid: Annotated[Optional[UUID], m("kicad_omits_default")] = None
    kicad_expr_tag_name: ClassVar[Literal["gr_text"]] = "gr_text"


@dataclass(config=pydantic_config, eq=False)
class GraphicalTextBox(BaseTextBox):
    """
    A graphical text box in KiCad.

    `KiCad graphical textbox <https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_graphical_text_box>`_

    :cvar kicad_expr_tag_name: The KiCad expression tag name for this element ("gr_text_box").
    """

    kicad_expr_tag_name = "gr_text_box"


@dataclass(config=pydantic_config, eq=False)
class GraphicalLine(KicadPcbExpr):
    """
    A graphical line element.

    `KiCad graphical line <https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_graphical_line>`_

    :param locked: Whether the line can move or not.
    :param start: The starting X-Y coordinates of the line.
    :param end: The ending X-Y coordinates of the line.
    :param width: The width of the line.
    :param stroke: Instance of :py:class:`~edea.kicad.common.Stroke` object defining the line style.
    :param layer: The canonical layer the line resides on.
    :param angle: The rotational angle of the line.
    :param tstamp: The unique identifier of the line object.
    :param uuid: The unique identifier of the line object.
    :cvar kicad_expr_tag_name: The KiCad expression tag name for this element ("gr_line").

    .. note::
        The `tstamp` field got renamed to `uuid` in 20240108 (KiCad 8).

    """

    locked: Annotated[bool, m("kicad_kw_bool")] = False
    start: tuple[float, float] = (0, 0)
    end: tuple[float, float] = (0, 0)
    width: Optional[float] = None
    stroke: Optional[Stroke] = None
    layer: Optional[CanonicalLayerName] = None
    angle: Optional[float] = None
    tstamp: Annotated[Optional[UUID], m("kicad_omits_default")] = None
    uuid: Annotated[Optional[UUID], m("kicad_omits_default")] = None
    net: Annotated[Optional[str], m("kicad_omits_default")] = None
    kicad_expr_tag_name: ClassVar[Literal["gr_line"]] = "gr_line"

    def envelope(
        self, min_x: float, max_x: float, min_y: float, max_y: float
    ) -> tuple[float, float, float, float]:
        """
        Envelopes the line in a bounding box.

        :param min_x: Initial minimum X coordinate.
        :param max_x: Initial maximum X coordinate.
        :param min_y: Initial minimum Y coordinate.
        :param max_y: Initial maximum Y coordinate.

        :returns: A tuple of the bounding box verticies with after enveloping the line.
        """
        for pt in self.start, self.end:
            min_x = min(min_x, pt[0])
            max_x = max(max_x, pt[0])
            min_y = min(min_y, pt[1])
            max_y = max(max_y, pt[1])
        return min_x, max_x, min_y, max_y


@dataclass(config=pydantic_config, eq=False)
class GraphicalRectangle(KicadPcbExpr):
    """
    A graphical rectangle.

    `KiCad graphical rectangle <https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_graphical_rectangle>`_

    :param locked: Whether the rectangle can move or not.
    :param start: The X-Y coordinates of the upper left corner of the rectangle.
    :param width: The line width of the rectangle.
    :param end: The X-Y coordinates of the low right corner of the rectangle.
    :param stroke: Instance of :py:class:`~edea.kicad.common.Stroke` object the line style of the rectangle's edge.
    :param fill: How the rectangle is filled.
    :param layer: The canonical layer the rectangle resides on.
    :cvar kicad_expr_tag_name: The KiCad expression tag name for this element ("gr_rect").

    .. note::
        The `tstamp` field got renamed to `uuid` in 20240108 (KiCad 8).

    """

    locked: Annotated[bool, m("kicad_kw_bool")] = False
    start: tuple[float, float] = (0, 0)
    end: tuple[float, float] = (0, 0)
    width: Optional[float] = None
    stroke: Optional[Stroke] = None
    fill: Optional[Literal["solid", "yes", "none"]] = None
    layer: Optional[CanonicalLayerName] = None
    net: Optional[int] = None
    tstamp: Annotated[Optional[UUID], m("kicad_omits_default")] = None
    uuid: Annotated[Optional[UUID], m("kicad_omits_default")] = None
    kicad_expr_tag_name: ClassVar[Literal["gr_rect"]] = "gr_rect"

    def envelope(
        self, min_x: float, max_x: float, min_y: float, max_y: float
    ) -> tuple[float, float, float, float]:
        """
        Envelopes the rectangle in a bounding box.

        :param min_x: Initial minimum X coordinate.
        :param max_x: Initial maximum X coordinate.
        :param min_y: Initial minimum Y coordinate.
        :param max_y: Initial maximum Y coordinate.

        :returns: A tuple of the bounding box verticies with after enveloping the rectangle.
        """
        for pt in self.start, self.end:
            min_x = min(min_x, pt[0])
            max_x = max(max_x, pt[0])
            min_y = min(min_y, pt[1])
            max_y = max(max_y, pt[1])
        return min_x, max_x, min_y, max_y


@dataclass(config=pydantic_config, eq=False)
class GraphicalCircle(KicadPcbExpr):
    """
    A graphical circle element.

    `KiCad graphical circle <https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_graphical_circle>`_

    :param locked: Whether the circle can move or not.
    :param center: The X-Y coordinates of the center of the circle.
    :param end: The coordinates of the end of the radius of the circle.
    :param stroke: Instance of :py:class:`~edea.kicad.common.Stroke` object defining the line style of the circle's edge.
    :param width: The line width of the circle.
    :param fill: How the circle is filled
    :param layer: The canonical layer the circle resides on.
    :param tstamp: The unique identifier of the circle object.
    :param uuid: The unique identifier of the circle object.
    :cvar kicad_expr_tag_name: The KiCad expression tag name for this element ("gr_circle").

    .. note::
        The `tstamp` field got renamed to `uuid` in 20240108 (KiCad 8).

    """

    locked: Annotated[bool, m("kicad_kw_bool")] = False
    center: tuple[float, float] = (0, 0)
    end: tuple[float, float] = (0, 0)
    stroke: Optional[Stroke] = None
    width: Optional[float] = None
    fill: Optional[Literal["solid", "yes", "no", "none"]] = None
    layer: Optional[CanonicalLayerName] = None
    tstamp: Annotated[Optional[UUID], m("kicad_omits_default")] = None
    uuid: Annotated[Optional[UUID], m("kicad_omits_default")] = None
    kicad_expr_tag_name: ClassVar[Literal["gr_circle"]] = "gr_circle"

    def envelope(
        self, min_x: float, max_x: float, min_y: float, max_y: float
    ) -> tuple[float, float, float, float]:
        """
        Envelopes the circle in a bounding box.

        :param min_x: Initial minimum X coordinate.
        :param max_x: Initial maximum X coordinate.
        :param min_y: Initial minimum Y coordinate.
        :param max_y: Initial maximum Y coordinate.

        :returns: A tuple of the bounding box verticies with after enveloping the circle.
        """
        radius = math.dist(self.end, self.center)
        min_x = min(min_x, self.center[0] - radius)
        max_x = max(max_x, self.center[0] + radius)
        min_y = min(min_y, self.center[1] - radius)
        max_y = max(max_y, self.center[1] + radius)
        return min_x, max_x, min_y, max_y


@dataclass(config=pydantic_config, eq=False)
class GraphicalArc(KicadPcbExpr):
    """
    A graphical arc element.

    `KiCad graphical arc <https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_graphical_arc>`_

    :param locked: Whether the arc can move or not.
    :param start: The X-Y coordinates of the start position of the arc radius.
    :param mid: The X-Y coordinates of the midpoint along the arc.
    :param end: The X-Y coordinates of the end position of the arc radius.
    :param width: The line width of the arc.
    :param stroke: Instance of :py:class:`~edea.kicad.common.Stroke` object defining the line style of the arc's edge.
    :param layer: The canonical layer the arc resides on.
    :param net: The net number of the arc.
    :param tstamp: The unique identifier of the arc object.
    :param uuid: The unique identifier of the arc object.
    :cvar kicad_expr_tag_name: The KiCad expression tag name for this element ("gr_arc").

    .. note::
        The `net` field got added in 20240108 (KiCad 8).

    .. note::
        The `tstamp` field got renamed to `uuid` in 20240108 (KiCad 8).

    """

    locked: Annotated[bool, m("kicad_kw_bool")] = False
    start: tuple[float, float] = (0, 0)
    mid: tuple[float, float] = (0, 0)
    end: tuple[float, float] = (0, 0)
    width: Optional[float] = None
    stroke: Optional[Stroke] = None
    layer: Optional[CanonicalLayerName] = None
    net: Optional[int] = None
    tstamp: Annotated[Optional[UUID], m("kicad_omits_default")] = None
    uuid: Annotated[Optional[UUID], m("kicad_omits_default")] = None
    kicad_expr_tag_name: ClassVar[Literal["gr_arc"]] = "gr_arc"

    def center(self) -> tuple[float, float]:
        """
        Algebraic solution to find the center of an arc
        given three points on its circumference.

        :returns: (x, y) coordinates of the center of the arc.
        """
        x1, y1 = self.start
        x2, y2 = self.mid
        x3, y3 = self.end

        A_1_2 = np.linalg.det(
            np.array(
                [
                    [x1**2 + y1**2, y1, 1],
                    [x2**2 + y2**2, y2, 1],
                    [x3**2 + y3**2, y3, 1],
                ]
            )
        )
        A_1_1 = np.linalg.det(np.array([[x1, y1, 1], [x2, y2, 1], [x3, y3, 1]]))
        A_1_3 = np.linalg.det(
            np.array(
                [
                    [x1**2 + y1**2, x1, 1],
                    [x2**2 + y2**2, x2, 1],
                    [x3**2 + y3**2, x3, 1],
                ]
            )
        )
        return (A_1_2 / (2 * A_1_1), -A_1_3 / (2 * A_1_1))

    def angles_rad(self):
        """
        Calculates the angles of the arc in radians.

        :returns: Set of angles in radians.
        """
        center = self.center()
        start_angle = round(
            math.degrees(
                math.atan2(self.start[1] - center[1], self.start[0] - center[0])
            )
        )
        mid_angle = round(
            math.degrees(math.atan2(self.mid[1] - center[1], self.mid[0] - center[0]))
        )
        end_angle = round(
            math.degrees(math.atan2(self.end[1] - center[1], self.end[0] - center[0]))
        )

        is_counterclockwise = start_angle <= mid_angle <= end_angle
        # Calculate the angle range based on direction
        if is_counterclockwise:
            angle_range = range(start_angle, end_angle + 1)
        else:
            end_angle %= 360
            if end_angle < start_angle:
                angle_range = range(end_angle, start_angle - 360 - 1, -1)
            else:
                angle_range = range(start_angle, end_angle + 1)

        return set(math.radians(angle % 360) for angle in angle_range)

    def envelope(
        self, min_x: float, max_x: float, min_y: float, max_y: float
    ) -> tuple[float, float, float, float]:
        """
        Envelopes the arc in a bounding box.

        :param min_x: Initial minimum X coordinate.
        :param max_x: Initial maximum X coordinate.
        :param min_y: Initial minimum Y coordinate.
        :param max_y: Initial maximum Y coordinate.

        :returns: A tuple of the bounding box verticies with after enveloping the arc.
        """
        center = self.center()
        radius = math.dist(center, self.start)
        for angle in self.angles_rad():
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
        return min_x, max_x, min_y, max_y


@dataclass(config=pydantic_config, eq=False)
class GraphicalPolygon(KicadPcbExpr):
    """
    A graphical polygon element.

    `KiCad graphical polygon <https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_graphical_polygon>`_

    :param locked: Whether the polygon can move or not.
    :param pts: The list of X-Y coordinates of the polygon outline.
    :param stroke: Instance of :py:class:`~edea.kicad.common.Stroke` object defining the line style of the polygon's edge.
    :param width: The line width of the polygon.
    :param fill: How the polygon is filled.
    :param layer: The canonical layer the polygon resides on.
    :param net: The net number of the polygon.
    :param tstamp: The unique identifier of the polygon object.
    :param uuid: The unique identifier of the polygon object.
    :cvar kicad_expr_tag_name: The KiCad expression tag name for this element ("gr_poly").

    .. note::
        The `net` field got added in 20240108 (KiCad 8).

    .. note::
        The `tstamp` field got renamed to `uuid` in 20240108 (KiCad 8).

    """

    locked: Annotated[bool, m("kicad_kw_bool")] = False
    pts: Pts = field(default_factory=Pts)
    stroke: Optional[Stroke] = None
    width: Optional[float] = None
    fill: Optional[Literal["solid", "yes", "no", "none"]] = None
    layer: Optional[CanonicalLayerName] = None
    net: Optional[int] = None
    tstamp: Annotated[Optional[UUID], m("kicad_omits_default")] = None
    uuid: Annotated[Optional[UUID], m("kicad_omits_default")] = None
    kicad_expr_tag_name: ClassVar[Literal["gr_poly"]] = "gr_poly"

    def envelope(
        self, min_x: float, max_x: float, min_y: float, max_y: float
    ) -> tuple[float, float, float, float]:
        """
        Envelopes the polygon in a bounding box.

        :param min_x: Initial minimum X coordinate.
        :param max_x: Initial maximum X coordinate.
        :param min_y: Initial minimum Y coordinate.
        :param max_y: Initial maximum Y coordinate.

        :returns: A tuple of the bounding box verticies with after enveloping the polygon.
        """
        for pt in self.pts.xys:
            min_x = min(min_x, pt.x)
            max_x = max(max_x, pt.x)
            min_y = min(min_y, pt.y)
            max_y = max(max_y, pt.y)
        return min_x, max_x, min_y, max_y


@dataclass(config=pydantic_config, eq=False)
class GraphicalBezier(KicadPcbExpr):
    """
    A graphical bezier curve element.

    `KiCad graphical bezier <https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_graphical_curve>`_

    :param locked: Whether the bezier curve can move or not.
    :param pts: A list of X-Y coordinates of the bezier curve.
    :param stroke: Instance of :py:class:`~edea.kicad.common.Stroke` object defining the line style of the bezier curve's edge.
    :param layer: The canonical layer the curve resides on.
    :param tstamp: The unique identifier of the curve object.
    :param uuid: The unique identifier of the curve object.
    :cvar kicad_expr_tag_name: The KiCad expression tag name for this element ("bezier").

    .. note::
        The `tstamp` field got renamed to `uuid` in 20240108 (KiCad 8).

    """

    locked: Annotated[bool, m("kicad_kw_bool")] = False
    pts: Pts = field(default_factory=Pts)
    stroke: Stroke = field(default_factory=Stroke)
    layer: Optional[CanonicalLayerName] = None
    tstamp: Annotated[Optional[UUID], m("kicad_omits_default")] = None
    uuid: Annotated[Optional[UUID], m("kicad_omits_default")] = None
    kicad_expr_tag_name: ClassVar[Literal["bezier", "gr_curve"]] = "bezier"

    def envelope(
        self, min_x: float, max_x: float, min_y: float, max_y: float
    ) -> tuple[float, float, float, float]:
        """
        Envelopes the curve in a bounding box.

        :param min_x: Initial minimum X coordinate.
        :param max_x: Initial maximum X coordinate.
        :param min_y: Initial minimum Y coordinate.
        :param max_y: Initial maximum Y coordinate.

        :returns: A tuple of the bounding box verticies with after enveloping the curve.
        """
        for pt in self.pts.xys:
            min_x = min(min_x, pt.x)
            max_x = max(max_x, pt.x)
            min_y = min(min_y, pt.y)
            max_y = max(max_y, pt.y)
        return min_x, max_x, min_y, max_y


@dataclass(config=pydantic_config, eq=False)
class GraphicalCurve(GraphicalBezier):
    """
    A graphical curve element.

    .. warning::
        This isn't documented in the Kicad docs, but it is in some files.
        This is what bezier was called before KiCad 7.

    :cvar kicad_expr_tag_name: The KiCad expression tag name for this element ("gr_curve").
    """

    kicad_expr_tag_name = "gr_curve"


@dataclass(config=pydantic_config, eq=False)
class GraphicalBoundingBox(KicadPcbExpr):
    """
    A graphical bounding box element.

    `KiCad graphical bounding box <https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_annotation_bounding_box>`_

    :param locked: Whether the bounding box can move or not.
    :param start: The X-Y coordinates of the upper left corner of the rectangle.
    :param end: The X-Y coordinates of the low right corner of the rectangle.
    :cvar kicad_expr_tag_name: The KiCad expression tag name for this element ("gr_bbox").
    """

    locked: Annotated[bool, m("kicad_kw_bool")] = False
    start: tuple[float, float] = (0, 0)
    end: tuple[float, float] = (0, 0)
    kicad_expr_tag_name: ClassVar[Literal["gr_bbox"]] = "gr_bbox"


class DimensionFormatUnits(StrEnum):
    """
    The different unit options for dimension text formatting within KiCad.

    `KiCad dimension format <https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_dimension_format>`_

    """

    Inches = "0"
    Mils = "1"
    Millimeters = "2"
    Automatic = "3"


class DimensionFormatUnitsFormat(StrEnum):
    """
    The different formatting styles for unit suffixes in dimension text.

    `KiCad dimension format <https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_dimension_format>`_

    """

    NoSuffix = "0"
    """
    No unit suffix is appended to the dimension value.
    """
    BareSuffix = "1"
    """
    The unit suffix is appended directly to the dimension value.
    """
    WrapSuffix = "2"
    """
    The unit suffix is wrapped in parentheses after the dimension value.
    """


@dataclass(config=pydantic_config, eq=False)
class DimensionFormat(KicadPcbExpr):
    """
    The formatting options for dimension text displayed in KiCad.

    `KiCad dimension format <https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_dimension_format>`_

    :param prefix: the string to add to the beginning of the dimension text.
    :param suffix: the string to add to the end of the dimension text.
    :param units: The dimension units.
    :param units_format: How the unit's suffix is formatted.
    :param precision: The number of significant digits.
    :param override_value: The text to substitute for the actual physical dimension.
    :param suppress_zeroes: Whether to removes all trailing zeros from the dimension text or not.
    :cvar kicad_expr_tag_name: The KiCad expression tag name for this element ("format").
    """

    prefix: Optional[str] = None
    suffix: Optional[str] = None
    units: DimensionFormatUnits = DimensionFormatUnits.Millimeters
    units_format: DimensionFormatUnitsFormat = DimensionFormatUnitsFormat.WrapSuffix
    precision: int = 4
    override_value: Optional[str] = None
    suppress_zeroes: Annotated[bool, m("kicad_kw_bool")] = False
    kicad_expr_tag_name: ClassVar[Literal["format"]] = "format"


class DimensionStyleTextPositionMode(StrEnum):
    """
    The different positioning options for dimension text in KiCad.

    `KiCad dimension style <https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_dimension_style>`_
    """

    Outside = "0"
    InLine = "1"
    Manual = "2"


class DimensionStyleTextFrame(StrEnum):
    """
    The various frame styles for dimension text in KiCad.

    `KiCad dimension style <https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_dimension_style>`_
    """

    NoFrame = "0"
    Rectangle = "1"
    Circle = "2"
    RoundedRectangle = "3"


@dataclass(config=pydantic_config, eq=False)
class DimensionStyle(KicadPcbExpr):
    """
    The visual style options for dimensions displayed in KiCad.

    `KiCad dimension style <https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_dimension_style>`_

    :param thickness: The line thickness of the dimension.
    :param arrow_length: The length of the dimension arrows.
    :param text_position_mode: The position mode of the dimension text.
    :param extension_height: The length of the extension lines past the dimension crossbar.
    :param extension_offset: The distance from feature points to extension line start.
    :param text_frame: The style of the frame around the dimension text.
    :param keep_text_aligned: Whether the dimension text should be kept in line with the dimension crossbar or not.
    :cvar kicad_expr_tag_name: The KiCad expression tag name for this element ("style").
    """

    thickness: float = 0.0
    arrow_length: float = 0.0
    text_position_mode: DimensionStyleTextPositionMode = (
        DimensionStyleTextPositionMode.Outside
    )
    extension_height: Optional[float] = None
    extension_offset: Optional[float] = None
    text_frame: Optional[DimensionStyleTextFrame] = None
    keep_text_aligned: Annotated[bool, m("kicad_kw_bool")] = False
    kicad_expr_tag_name: ClassVar[Literal["style"]] = "style"


@dataclass(config=pydantic_config, eq=False)
class GraphicalDimension(KicadPcbExpr):
    """
    A graphical dimension element.

    `KiCad graphical dimension <https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html#_dimension>`_

    :param locked: Whether the dimension can move or not.
    :param type: The type of dimension (aligned, leader, center, orthogonal, and radial).
    :param layer: The canonical layer the dimension resides on.
    :param pts: A list of X-Y coordinates of the dimension.
    :param height: The height of aligned dimensions.
    :param orientation: The rotation angle for orthogonal dimensions.
    :param leader_length: The distance from the marked radius to the knee for radial dimensions.
    :param gr_text: The dimension text formatting for all dimension types except center dimensions.
    :param format: The dimension formatting for all dimension types except center dimensions.
    :param style: The dimension style information.
    :param tstamp: The unique identifier of the dimension object.
    :param uuid: The unique identifier of the dimension object.
    :cvar kicad_expr_tag_name: The KiCad expression tag name for this element ("dimension").

    .. note::
        The `tstamp` field got renamed to `uuid` in 20240108 (KiCad 8).

    """

    locked: Annotated[bool, m("kicad_kw_bool")] = False
    type: Literal["aligned", "leader", "center", "orthogonal", "radial"] = "aligned"
    layer: CanonicalLayerName = "F.Cu"
    pts: Pts = field(default_factory=Pts)
    height: Optional[float] = None
    orientation: Optional[float] = None
    leader_length: Optional[float] = None
    gr_text: Optional[GraphicalText] = None
    format: Optional[DimensionFormat] = None
    style: DimensionStyle = field(default_factory=DimensionStyle)
    tstamp: Annotated[Optional[UUID], m("kicad_omits_default")] = None
    uuid: Annotated[Optional[UUID], m("kicad_omits_default")] = None
    kicad_expr_tag_name: ClassVar[Literal["dimension"]] = "dimension"
