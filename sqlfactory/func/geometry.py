"""
Geometry constructor functions
(https://mariadb.com/docs/server/reference/sql-statements/geometry-constructors/geometry-constructors).

MariaDB does not check the geometry type for the ``*FromText`` / ``*FromWKB`` constructors below: all 30
``*FromText`` names share one underlying parser, and so do all 30 ``*FromWKB`` names - for example
``ST_PointFromText('LINESTRING(0 0,1 1)')`` happily returns a LINESTRING, not an error. The name only documents
intent; MariaDB does not enforce it.

Spatial functions (relations, measurements, accessors, operations and output - ST_AsText, ST_AsGeoJSON, ST_GeoHash,
ST_Buffer, ST_Union, and friends) are not part of this module; they live in :mod:`sqlfactory.func.spatial`.
"""

from typing import Any

from sqlfactory.func.base import Function
from sqlfactory.statement import Statement

# ---------------------------------------------------------------------------
# Structure constructors - build a geometry value from its component parts.
# ---------------------------------------------------------------------------


class Point(Function):
    """``POINT(x, y)`` — constructs a Point value from its coordinates."""

    def __init__(self, x: Statement | Any, y: Statement | Any) -> None:
        super().__init__("POINT", x, y)


class LineString(Function):
    """``LINESTRING(pt, ...)`` — constructs a LineString value from two or more Point values."""

    def __init__(self, *points: Statement | Any) -> None:
        super().__init__("LINESTRING", *points)


class Polygon(Function):
    """
    ``POLYGON(ls, ...)`` — constructs a Polygon value from one or more LineString values, each of which must be a
    closed, simple ring. The first ring is the exterior ring; any further rings are interior rings (holes).
    """

    def __init__(self, *rings: Statement | Any) -> None:
        super().__init__("POLYGON", *rings)


class MultiPoint(Function):
    """``MULTIPOINT(pt, ...)`` — constructs a MultiPoint value from Point values."""

    def __init__(self, *points: Statement | Any) -> None:
        super().__init__("MULTIPOINT", *points)


class MultiLineString(Function):
    """``MULTILINESTRING(ls, ...)`` — constructs a MultiLineString value from LineString values."""

    def __init__(self, *linestrings: Statement | Any) -> None:
        super().__init__("MULTILINESTRING", *linestrings)


class MultiPolygon(Function):
    """``MULTIPOLYGON(poly, ...)`` — constructs a MultiPolygon value from Polygon values."""

    def __init__(self, *polygons: Statement | Any) -> None:
        super().__init__("MULTIPOLYGON", *polygons)


class GeometryCollection(Function):
    """``GEOMETRYCOLLECTION(g, ...)`` — constructs a GeometryCollection value from any geometry values."""

    def __init__(self, *geometries: Statement | Any) -> None:
        super().__init__("GEOMETRYCOLLECTION", *geometries)


# ---------------------------------------------------------------------------
# WKT constructors - NAME(wkt[, srid]). MariaDB does not check that the WKT actually describes the geometry type
# the name suggests (see the module docstring). Every canonical class below has one or more documented non-ST
# and/or short-ST synonyms, implemented as thin subclasses that call the canonical `__init__` and then override
# the rendered function name (`self.function`).
# ---------------------------------------------------------------------------


class StGeomFromText(Function):
    """
    ``ST_GEOMFROMTEXT(wkt[, srid])`` — constructs a geometry value of any type from its WKT (Well-Known Text)
    representation, with an optional SRID.
    """

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        if srid is not None:
            super().__init__("ST_GEOMFROMTEXT", wkt, srid)
        else:
            super().__init__("ST_GEOMFROMTEXT", wkt)


class StGeometryFromText(StGeomFromText):
    """Synonym for ST_GEOMFROMTEXT."""

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkt, srid)
        self.function = "ST_GEOMETRYFROMTEXT"


class GeomFromText(StGeomFromText):
    """Synonym for ST_GEOMFROMTEXT."""

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkt, srid)
        self.function = "GEOMFROMTEXT"


class GeometryFromText(StGeomFromText):
    """Synonym for ST_GEOMFROMTEXT."""

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkt, srid)
        self.function = "GEOMETRYFROMTEXT"


class StPointFromText(Function):
    """
    ``ST_POINTFROMTEXT(wkt[, srid])`` — named for Point values, with an optional SRID.
    MariaDB does not check the type (see the module docstring).
    """

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        if srid is not None:
            super().__init__("ST_POINTFROMTEXT", wkt, srid)
        else:
            super().__init__("ST_POINTFROMTEXT", wkt)


class PointFromText(StPointFromText):
    """Synonym for ST_POINTFROMTEXT."""

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkt, srid)
        self.function = "POINTFROMTEXT"


class StLineFromText(Function):
    """
    ``ST_LINEFROMTEXT(wkt[, srid])`` — named for LineString values, with an optional SRID.
    MariaDB does not check the type (see the module docstring).
    """

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        if srid is not None:
            super().__init__("ST_LINEFROMTEXT", wkt, srid)
        else:
            super().__init__("ST_LINEFROMTEXT", wkt)


class StLineStringFromText(StLineFromText):
    """Synonym for ST_LINEFROMTEXT."""

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkt, srid)
        self.function = "ST_LINESTRINGFROMTEXT"


class LineFromText(StLineFromText):
    """Synonym for ST_LINEFROMTEXT."""

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkt, srid)
        self.function = "LINEFROMTEXT"


class LineStringFromText(StLineFromText):
    """Synonym for ST_LINEFROMTEXT."""

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkt, srid)
        self.function = "LINESTRINGFROMTEXT"


class StPolyFromText(Function):
    """
    ``ST_POLYFROMTEXT(wkt[, srid])`` — named for Polygon values, with an optional SRID.
    MariaDB does not check the type (see the module docstring).
    """

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        if srid is not None:
            super().__init__("ST_POLYFROMTEXT", wkt, srid)
        else:
            super().__init__("ST_POLYFROMTEXT", wkt)


class StPolygonFromText(StPolyFromText):
    """Synonym for ST_POLYFROMTEXT."""

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkt, srid)
        self.function = "ST_POLYGONFROMTEXT"


class PolyFromText(StPolyFromText):
    """Synonym for ST_POLYFROMTEXT."""

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkt, srid)
        self.function = "POLYFROMTEXT"


class PolygonFromText(StPolyFromText):
    """Synonym for ST_POLYFROMTEXT."""

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkt, srid)
        self.function = "POLYGONFROMTEXT"


class StMultiPointFromText(Function):
    """
    ``ST_MULTIPOINTFROMTEXT(wkt[, srid])`` — named for MultiPoint values, with an optional SRID.
    MariaDB does not check the type (see the module docstring).
    """

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        if srid is not None:
            super().__init__("ST_MULTIPOINTFROMTEXT", wkt, srid)
        else:
            super().__init__("ST_MULTIPOINTFROMTEXT", wkt)


class StMPointFromText(StMultiPointFromText):
    """Synonym for ST_MULTIPOINTFROMTEXT."""

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkt, srid)
        self.function = "ST_MPOINTFROMTEXT"


class MultiPointFromText(StMultiPointFromText):
    """Synonym for ST_MULTIPOINTFROMTEXT."""

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkt, srid)
        self.function = "MULTIPOINTFROMTEXT"


class MPointFromText(StMultiPointFromText):
    """Synonym for ST_MULTIPOINTFROMTEXT."""

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkt, srid)
        self.function = "MPOINTFROMTEXT"


class StMultiLineStringFromText(Function):
    """
    ``ST_MULTILINESTRINGFROMTEXT(wkt[, srid])`` — named for MultiLineString values, with an optional SRID.
    MariaDB does not check the type (see the module docstring).
    """

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        if srid is not None:
            super().__init__("ST_MULTILINESTRINGFROMTEXT", wkt, srid)
        else:
            super().__init__("ST_MULTILINESTRINGFROMTEXT", wkt)


class StMLineFromText(StMultiLineStringFromText):
    """Synonym for ST_MULTILINESTRINGFROMTEXT."""

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkt, srid)
        self.function = "ST_MLINEFROMTEXT"


class MultiLineStringFromText(StMultiLineStringFromText):
    """Synonym for ST_MULTILINESTRINGFROMTEXT."""

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkt, srid)
        self.function = "MULTILINESTRINGFROMTEXT"


class MLineFromText(StMultiLineStringFromText):
    """Synonym for ST_MULTILINESTRINGFROMTEXT."""

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkt, srid)
        self.function = "MLINEFROMTEXT"


class StMultiPolygonFromText(Function):
    """
    ``ST_MULTIPOLYGONFROMTEXT(wkt[, srid])`` — named for MultiPolygon values, with an optional SRID.
    MariaDB does not check the type (see the module docstring).
    """

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        if srid is not None:
            super().__init__("ST_MULTIPOLYGONFROMTEXT", wkt, srid)
        else:
            super().__init__("ST_MULTIPOLYGONFROMTEXT", wkt)


class StMPolyFromText(StMultiPolygonFromText):
    """Synonym for ST_MULTIPOLYGONFROMTEXT."""

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkt, srid)
        self.function = "ST_MPOLYFROMTEXT"


class MultiPolygonFromText(StMultiPolygonFromText):
    """Synonym for ST_MULTIPOLYGONFROMTEXT."""

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkt, srid)
        self.function = "MULTIPOLYGONFROMTEXT"


class MPolyFromText(StMultiPolygonFromText):
    """Synonym for ST_MULTIPOLYGONFROMTEXT."""

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkt, srid)
        self.function = "MPOLYFROMTEXT"


class StGeomCollFromText(Function):
    """
    ``ST_GEOMCOLLFROMTEXT(wkt[, srid])`` — named for GeometryCollection values, with an optional SRID.
    MariaDB does not check the type (see the module docstring).
    """

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        if srid is not None:
            super().__init__("ST_GEOMCOLLFROMTEXT", wkt, srid)
        else:
            super().__init__("ST_GEOMCOLLFROMTEXT", wkt)


class StGeometryCollectionFromText(StGeomCollFromText):
    """Synonym for ST_GEOMCOLLFROMTEXT."""

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkt, srid)
        self.function = "ST_GEOMETRYCOLLECTIONFROMTEXT"


class GeomCollFromText(StGeomCollFromText):
    """Synonym for ST_GEOMCOLLFROMTEXT."""

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkt, srid)
        self.function = "GEOMCOLLFROMTEXT"


class GeometryCollectionFromText(StGeomCollFromText):
    """Synonym for ST_GEOMCOLLFROMTEXT."""

    def __init__(self, wkt: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkt, srid)
        self.function = "GEOMETRYCOLLECTIONFROMTEXT"


# ---------------------------------------------------------------------------
# WKB constructors - NAME(wkb[, srid]). Same family shape as the WKT constructors above, same lack of type
# checking (see the module docstring).
# ---------------------------------------------------------------------------


class StGeomFromWkb(Function):
    """
    ``ST_GEOMFROMWKB(wkb[, srid])`` — constructs a geometry value of any type from its WKB (Well-Known Binary)
    representation, with an optional SRID.
    """

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        if srid is not None:
            super().__init__("ST_GEOMFROMWKB", wkb, srid)
        else:
            super().__init__("ST_GEOMFROMWKB", wkb)


class StGeometryFromWkb(StGeomFromWkb):
    """Synonym for ST_GEOMFROMWKB."""

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkb, srid)
        self.function = "ST_GEOMETRYFROMWKB"


class GeomFromWkb(StGeomFromWkb):
    """Synonym for ST_GEOMFROMWKB."""

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkb, srid)
        self.function = "GEOMFROMWKB"


class GeometryFromWkb(StGeomFromWkb):
    """Synonym for ST_GEOMFROMWKB."""

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkb, srid)
        self.function = "GEOMETRYFROMWKB"


class StPointFromWkb(Function):
    """
    ``ST_POINTFROMWKB(wkb[, srid])`` — named for Point values, with an optional SRID.
    MariaDB does not check the type (see the module docstring).
    """

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        if srid is not None:
            super().__init__("ST_POINTFROMWKB", wkb, srid)
        else:
            super().__init__("ST_POINTFROMWKB", wkb)


class PointFromWkb(StPointFromWkb):
    """Synonym for ST_POINTFROMWKB."""

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkb, srid)
        self.function = "POINTFROMWKB"


class StLineFromWkb(Function):
    """
    ``ST_LINEFROMWKB(wkb[, srid])`` — named for LineString values, with an optional SRID.
    MariaDB does not check the type (see the module docstring).
    """

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        if srid is not None:
            super().__init__("ST_LINEFROMWKB", wkb, srid)
        else:
            super().__init__("ST_LINEFROMWKB", wkb)


class StLineStringFromWkb(StLineFromWkb):
    """Synonym for ST_LINEFROMWKB."""

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkb, srid)
        self.function = "ST_LINESTRINGFROMWKB"


class LineFromWkb(StLineFromWkb):
    """Synonym for ST_LINEFROMWKB."""

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkb, srid)
        self.function = "LINEFROMWKB"


class LineStringFromWkb(StLineFromWkb):
    """Synonym for ST_LINEFROMWKB."""

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkb, srid)
        self.function = "LINESTRINGFROMWKB"


class StPolyFromWkb(Function):
    """
    ``ST_POLYFROMWKB(wkb[, srid])`` — named for Polygon values, with an optional SRID.
    MariaDB does not check the type (see the module docstring).
    """

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        if srid is not None:
            super().__init__("ST_POLYFROMWKB", wkb, srid)
        else:
            super().__init__("ST_POLYFROMWKB", wkb)


class StPolygonFromWkb(StPolyFromWkb):
    """Synonym for ST_POLYFROMWKB."""

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkb, srid)
        self.function = "ST_POLYGONFROMWKB"


class PolyFromWkb(StPolyFromWkb):
    """Synonym for ST_POLYFROMWKB."""

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkb, srid)
        self.function = "POLYFROMWKB"


class PolygonFromWkb(StPolyFromWkb):
    """Synonym for ST_POLYFROMWKB."""

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkb, srid)
        self.function = "POLYGONFROMWKB"


class StMultiPointFromWkb(Function):
    """
    ``ST_MULTIPOINTFROMWKB(wkb[, srid])`` — named for MultiPoint values, with an optional SRID.
    MariaDB does not check the type (see the module docstring).
    """

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        if srid is not None:
            super().__init__("ST_MULTIPOINTFROMWKB", wkb, srid)
        else:
            super().__init__("ST_MULTIPOINTFROMWKB", wkb)


class StMPointFromWkb(StMultiPointFromWkb):
    """Synonym for ST_MULTIPOINTFROMWKB."""

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkb, srid)
        self.function = "ST_MPOINTFROMWKB"


class MultiPointFromWkb(StMultiPointFromWkb):
    """Synonym for ST_MULTIPOINTFROMWKB."""

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkb, srid)
        self.function = "MULTIPOINTFROMWKB"


class MPointFromWkb(StMultiPointFromWkb):
    """Synonym for ST_MULTIPOINTFROMWKB."""

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkb, srid)
        self.function = "MPOINTFROMWKB"


class StMultiLineStringFromWkb(Function):
    """
    ``ST_MULTILINESTRINGFROMWKB(wkb[, srid])`` — named for MultiLineString values, with an optional SRID.
    MariaDB does not check the type (see the module docstring).
    """

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        if srid is not None:
            super().__init__("ST_MULTILINESTRINGFROMWKB", wkb, srid)
        else:
            super().__init__("ST_MULTILINESTRINGFROMWKB", wkb)


class StMLineFromWkb(StMultiLineStringFromWkb):
    """Synonym for ST_MULTILINESTRINGFROMWKB."""

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkb, srid)
        self.function = "ST_MLINEFROMWKB"


class MultiLineStringFromWkb(StMultiLineStringFromWkb):
    """Synonym for ST_MULTILINESTRINGFROMWKB."""

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkb, srid)
        self.function = "MULTILINESTRINGFROMWKB"


class MLineFromWkb(StMultiLineStringFromWkb):
    """Synonym for ST_MULTILINESTRINGFROMWKB."""

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkb, srid)
        self.function = "MLINEFROMWKB"


class StMultiPolygonFromWkb(Function):
    """
    ``ST_MULTIPOLYGONFROMWKB(wkb[, srid])`` — named for MultiPolygon values, with an optional SRID.
    MariaDB does not check the type (see the module docstring).
    """

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        if srid is not None:
            super().__init__("ST_MULTIPOLYGONFROMWKB", wkb, srid)
        else:
            super().__init__("ST_MULTIPOLYGONFROMWKB", wkb)


class StMPolyFromWkb(StMultiPolygonFromWkb):
    """Synonym for ST_MULTIPOLYGONFROMWKB."""

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkb, srid)
        self.function = "ST_MPOLYFROMWKB"


class MultiPolygonFromWkb(StMultiPolygonFromWkb):
    """Synonym for ST_MULTIPOLYGONFROMWKB."""

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkb, srid)
        self.function = "MULTIPOLYGONFROMWKB"


class MPolyFromWkb(StMultiPolygonFromWkb):
    """Synonym for ST_MULTIPOLYGONFROMWKB."""

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkb, srid)
        self.function = "MPOLYFROMWKB"


class StGeomCollFromWkb(Function):
    """
    ``ST_GEOMCOLLFROMWKB(wkb[, srid])`` — named for GeometryCollection values, with an optional SRID.
    MariaDB does not check the type (see the module docstring).
    """

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        if srid is not None:
            super().__init__("ST_GEOMCOLLFROMWKB", wkb, srid)
        else:
            super().__init__("ST_GEOMCOLLFROMWKB", wkb)


class StGeometryCollectionFromWkb(StGeomCollFromWkb):
    """Synonym for ST_GEOMCOLLFROMWKB."""

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkb, srid)
        self.function = "ST_GEOMETRYCOLLECTIONFROMWKB"


class GeomCollFromWkb(StGeomCollFromWkb):
    """Synonym for ST_GEOMCOLLFROMWKB."""

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkb, srid)
        self.function = "GEOMCOLLFROMWKB"


class GeometryCollectionFromWkb(StGeomCollFromWkb):
    """Synonym for ST_GEOMCOLLFROMWKB."""

    def __init__(self, wkb: Statement | Any, srid: Statement | int | None = None) -> None:
        super().__init__(wkb, srid)
        self.function = "GEOMETRYCOLLECTIONFROMWKB"


# ---------------------------------------------------------------------------
# GeoJSON / GeoHash constructors
# ---------------------------------------------------------------------------


class StGeomFromGeoJson(Function):
    """
    ``ST_GEOMFROMGEOJSON(g[, option[, srid]])`` — parses a GeoJSON document and returns the corresponding
    geometry, with an optional dimension-handling flag and SRID.

    ``option`` controls what happens when ``g`` contains coordinates with more than 2 dimensions: omitting it, or
    passing ``NULL``, strips the extra dimensions, as do ``2``-``4``; ``1`` raises ``ERROR 3037``; any other value
    raises ``ERROR 1411`` (incorrect option value). The MariaDB KB calls ``1`` "the default", but the server does
    not apply it when ``option`` is omitted.

    When ``srid`` is given without ``option``, ``option`` is bound as ``NULL`` — the server treats a ``NULL``
    option the same as an omitted one.
    """

    def __init__(self, g: Statement | Any, option: Statement | int | None = None, srid: Statement | int | None = None) -> None:
        if srid is not None:
            super().__init__("ST_GEOMFROMGEOJSON", g, option, srid)
        elif option is not None:
            super().__init__("ST_GEOMFROMGEOJSON", g, option)
        else:
            super().__init__("ST_GEOMFROMGEOJSON", g)


class StPointFromGeoHash(Function):
    """
    ``ST_POINTFROMGEOHASH(geohash, srid)`` — decodes a geohash string into a Point at the center of the geohashed
    area. Unlike the WKT/WKB constructors, ``srid`` is required, not optional.

    MariaDB 12.0+.
    """

    def __init__(self, geohash: Statement | Any, srid: Statement | int) -> None:
        super().__init__("ST_POINTFROMGEOHASH", geohash, srid)


class PointFromGeoHash(StPointFromGeoHash):
    """
    Synonym for ST_POINTFROMGEOHASH. MariaDB 12.0+ (registered by the server, not documented in the KB).
    """

    def __init__(self, geohash: Statement | Any, srid: Statement | int) -> None:
        super().__init__(geohash, srid)
        self.function = "POINTFROMGEOHASH"
