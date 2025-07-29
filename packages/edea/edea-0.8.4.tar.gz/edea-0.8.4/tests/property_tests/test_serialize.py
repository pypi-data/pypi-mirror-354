import pytest
from hypothesis import given

import edea.kicad.common as common
import edea.kicad.pcb as pcb
import edea.kicad.pcb.common as pcb_common
import edea.kicad.pcb.footprint as pcb_footprint
import edea.kicad.pcb.graphics as pcb_graphics
import edea.kicad.schematic as schematic
import edea.kicad.schematic.shapes as shapes
import edea.kicad.schematic.symbol as symbol
from edea.kicad.base import KicadExpr
from edea.kicad.parser import from_list, from_str
from edea.kicad.serializer import from_list_to_str, to_list

from ._utils import any_kicad_expr_from_module
from .config import configure_hypothesis

configure_hypothesis()


@pytest.mark.skip(reason="pydantic v2 not supported yet")
@given(any_kicad_expr_from_module(common))
def test_serialize_any_common(expr: KicadExpr):
    """
    Test that serializing then parsing `common` classes results in the same
    expression.
    """
    lst = to_list(expr)
    string = from_list_to_str(lst)
    expr2 = from_list(lst)
    assert expr2 == expr
    expr3 = from_str(string)
    assert expr3 == expr


@pytest.mark.skip(reason="pydantic v2 not supported yet")
@given(any_kicad_expr_from_module(shapes))
def test_serialize_any_sch_shapes(expr: KicadExpr):
    """
    Test that serializing then parsing `schematic.shapes` results in the same
    expression.
    """
    lst = to_list(expr)
    string = from_list_to_str(lst)
    expr2 = from_list(lst)
    assert expr2 == expr
    expr3 = from_str(string)
    assert expr3 == expr


@pytest.mark.skip(reason="pydantic v2 not supported yet")
@given(any_kicad_expr_from_module(symbol))
def test_serialize_any_sch_symbol(expr: KicadExpr):
    """
    Test that serializing then parsing `schematic.symbol` results in the same
    expression.
    """
    lst = to_list(expr)
    string = from_list_to_str(lst)
    expr2 = from_list(lst)
    assert expr2 == expr
    expr3 = from_str(string)
    assert expr3 == expr


@pytest.mark.skip(reason="pydantic v2 not supported yet")
@given(any_kicad_expr_from_module(schematic))
def test_serialize_any_schematic_expr(expr: KicadExpr):
    """
    Test that serializing then parsing `schematic` expressions results in
    the same expression.
    """
    lst = to_list(expr)
    string = from_list_to_str(lst)
    expr2 = from_list(lst)
    assert expr2 == expr
    expr3 = from_str(string)
    assert expr3 == expr


@pytest.mark.skip(reason="pydantic v2 not supported yet")
@given(any_kicad_expr_from_module(pcb_common))
def test_serialize_any_pcb_common(expr: KicadExpr):
    """
    Test that serializing then parsing `pcb.common` expressions results in
    the same expression.
    """
    lst = to_list(expr)
    string = from_list_to_str(lst)
    expr2 = from_list(lst)
    assert expr2 == expr
    expr3 = from_str(string)
    assert expr3 == expr


@pytest.mark.skip(reason="pydantic v2 not supported yet")
@given(any_kicad_expr_from_module(pcb_graphics))
def test_serialize_any_pcb_graphics(expr: KicadExpr):
    """
    Test that serializing then parsing `pcb.graphics` expressions results in
    the same expression.
    """
    lst = to_list(expr)
    string = from_list_to_str(lst)
    expr2 = from_list(lst)
    assert expr2 == expr
    expr3 = from_str(string)
    assert expr3 == expr


@pytest.mark.skip(reason="pydantic v2 not supported yet")
@given(any_kicad_expr_from_module(pcb_footprint))
def test_serialize_any_pcb_footprint(expr: KicadExpr):
    """
    Test that serializing then parsing `pcb.footprint` expressions results in
    the same expression.
    """
    lst = to_list(expr)
    string = from_list_to_str(lst)
    expr2 = from_list(lst)
    assert expr2 == expr
    expr3 = from_str(string)
    assert expr3 == expr


@pytest.mark.skip(reason="pydantic v2 not supported yet")
@given(any_kicad_expr_from_module(pcb))
def test_serialize_any_pcb_expr(expr: KicadExpr):
    """
    Test that serializing then parsing `pcb.pcb` expressions results in
    the same expression.
    """
    lst = to_list(expr)
    string = from_list_to_str(lst)
    expr2 = from_list(lst)
    expr2 = from_list(lst)
    assert expr2 == expr
    expr3 = from_str(string)
    assert expr3 == expr
