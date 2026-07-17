"""Backward-compatible re-export of the RailwayCrossing model."""

from app.models.railway_crossing import Crossing, RailwayCrossing

__all__ = ["Crossing", "RailwayCrossing"]
