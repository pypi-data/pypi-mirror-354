from __future__ import annotations

from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from edea.kicad._str_enum import StrEnum


class Severity(StrEnum):
    """
    Different severity levels for checker violations.
    """

    error = "error"
    warning = "warning"
    ignore = "ignore"

    def __le__(self, other):
        members = list(Severity.__members__.values())
        return members.index(self) <= members.index(other)

    def __lt__(self, other):
        members = list(Severity.__members__.values())
        return members.index(self) <= members.index(other)


class CoordinateUnits(StrEnum):
    mm = "mm"
    mils = "mils"
    in_ = "in"


class Coordinate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    x: float = Field(..., description="x coordinate")
    y: float = Field(..., description="y coordinate")


class AffectedItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    description: str = Field(..., description="Description of the item")
    pos: Coordinate
    uuid: UUID


class Violation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: str = Field(..., description="KiCad type name for the violation")
    description: str = Field(..., description="Description of the violation")
    severity: Severity
    items: List[AffectedItem]
