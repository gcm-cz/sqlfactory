"""
Spatial functions (https://mariadb.com/kb/en/geographic-geometric-features/).

Geometry *constructors* (POINT, ST_GeomFromText, ST_GeomFromWKB, ST_GeomFromGeoJSON, ...) are not here - they live
in a separate geometry-constructors module, added by another change.
"""

from typing import Any, overload

from sqlfactory.entities import ColumnArg
from sqlfactory.func.agg import AggregateFunction
from sqlfactory.func.base import Function
from sqlfactory.statement import Statement

# ---------------------------------------------------------------------------
# Spatial relations (https://mariadb.com/kb/en/geometry-relations/)
# ---------------------------------------------------------------------------


class StContains(Function):
    """ST_CONTAINS(g1, g2) - true (1) if geometry g1 completely contains geometry g2."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__("ST_CONTAINS", g1, g2)


class Contains(StContains):
    """Synonym for ST_CONTAINS."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__(g1, g2)
        self.function = "CONTAINS"


class StCrosses(Function):
    """ST_CROSSES(g1, g2) - true (1) if g1 and g2 spatially cross: they intersect, but neither contains the other."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__("ST_CROSSES", g1, g2)


class Crosses(StCrosses):
    """Synonym for ST_CROSSES."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__(g1, g2)
        self.function = "CROSSES"


class StDisjoint(Function):
    """
    ST_DISJOINT(g1, g2) - true (1) if g1 and g2 do not spatially intersect (share no space).

    Note: bare `DISJOINT` is *not* a synonym for this - MariaDB maps it to MBRDISJOINT (see `Disjoint` below).
    """

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__("ST_DISJOINT", g1, g2)


class StEquals(Function):
    """
    ST_EQUALS(g1, g2)

    Returns true (1) if g1 and g2 represent the same geometry (spatially, not byte-for-byte).
    """

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__("ST_EQUALS", g1, g2)


class Equals(StEquals):
    """
    Synonym for ST_EQUALS.

    Note: shadows the unrelated `=` condition `sqlfactory.Equals` (aliased `Eq`) - use `StEquals` to avoid confusion.
    """

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__(g1, g2)
        self.function = "EQUALS"


class StIntersects(Function):
    """
    ST_INTERSECTS(g1, g2) - true (1) if g1 and g2 spatially intersect (share any space).

    Note: bare `INTERSECTS` is *not* a synonym for this - MariaDB maps it to MBRINTERSECTS (see `Intersects` below).
    """

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__("ST_INTERSECTS", g1, g2)


class StOverlaps(Function):
    """
    ST_OVERLAPS(g1, g2) - true (1) if g1 and g2 intersect, have the same dimension, but neither contains the other.

    Note: bare `OVERLAPS` is *not* a synonym for this - MariaDB maps it to MBROVERLAPS (see `Overlaps` below).
    """

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__("ST_OVERLAPS", g1, g2)


class StTouches(Function):
    """ST_TOUCHES(g1, g2) - true (1) if g1 and g2 share a point but their interiors do not intersect."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__("ST_TOUCHES", g1, g2)


class Touches(StTouches):
    """Synonym for ST_TOUCHES."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__(g1, g2)
        self.function = "TOUCHES"


class StWithin(Function):
    """ST_WITHIN(g1, g2) - true (1) if g1 is completely within g2. The inverse of ST_CONTAINS."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__("ST_WITHIN", g1, g2)


class Within(StWithin):
    """Synonym for ST_WITHIN."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__(g1, g2)
        self.function = "WITHIN"


class StCoveredBy(Function):
    """
    ST_COVEREDBY(g1, g2) - whether every point of g1 lies in g2 or on its boundary.

    MariaDB 12.0+.
    """

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__("ST_COVEREDBY", g1, g2)


class CoveredBy(StCoveredBy):
    """Synonym for ST_COVEREDBY. MariaDB 12.0+."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__(g1, g2)
        self.function = "COVEREDBY"


class StRelate(Function):
    """
    ST_RELATE(g1, g2, i)

    Returns true (1) if g1 is spatially related to g2 by testing the intersections between the interior,
    boundary and exterior of both geometries, as specified by the DE-9IM intersection pattern `i`.
    """

    def __init__(self, g1: Statement | Any, g2: Statement | Any, i: Statement | Any) -> None:
        super().__init__("ST_RELATE", g1, g2, i)


# ---------------------------------------------------------------------------
# MBR (Minimum Bounding Rectangle) relations
# ---------------------------------------------------------------------------


class MbrContains(Function):
    """MBRCONTAINS(g1, g2) - whether the MBR of g1 contains the MBR of g2."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__("MBRCONTAINS", g1, g2)


class MbrCoveredBy(Function):
    """MBRCOVEREDBY(g1, g2) - whether the MBR of g1 is covered by the MBR of g2. MariaDB 12.0+."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__("MBRCOVEREDBY", g1, g2)


class MbrDisjoint(Function):
    """MBRDISJOINT(g1, g2) - whether the MBRs of g1 and g2 are disjoint."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__("MBRDISJOINT", g1, g2)


class Disjoint(MbrDisjoint):
    """Legacy name for MBRDISJOINT (compares bounding rectangles, unlike ST_DISJOINT)."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__(g1, g2)
        self.function = "DISJOINT"


class MbrEqual(Function):
    """MBREQUAL(g1, g2) - whether the MBRs of g1 and g2 are the same."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__("MBREQUAL", g1, g2)


class MbrEquals(MbrEqual):
    """Synonym for MBREQUAL."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__(g1, g2)
        self.function = "MBREQUALS"


class MbrIntersects(Function):
    """MBRINTERSECTS(g1, g2) - whether the MBRs of g1 and g2 intersect."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__("MBRINTERSECTS", g1, g2)


class Intersects(MbrIntersects):
    """Legacy name for MBRINTERSECTS (compares bounding rectangles, unlike ST_INTERSECTS)."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__(g1, g2)
        self.function = "INTERSECTS"


class MbrOverlaps(Function):
    """MBROVERLAPS(g1, g2) - whether the MBRs of g1 and g2 overlap."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__("MBROVERLAPS", g1, g2)


class Overlaps(MbrOverlaps):
    """Legacy name for MBROVERLAPS (compares bounding rectangles, unlike ST_OVERLAPS)."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__(g1, g2)
        self.function = "OVERLAPS"


class MbrTouches(Function):
    """
    MBRTOUCHES(g1, g2).

    Unlike its MBR* siblings above, MariaDB's registry maps this name itself to the precise touches
    implementation (`Create_func_touches`), so the server computes precise ST_TOUCHES semantics here, not
    whether the bounding rectangles touch.
    """

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__("MBRTOUCHES", g1, g2)


class MbrWithin(Function):
    """MBRWITHIN(g1, g2) - whether the MBR of g1 is within the MBR of g2."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__("MBRWITHIN", g1, g2)


# ---------------------------------------------------------------------------
# Measurement (https://mariadb.com/kb/en/geometry-relations/, polygon/linestring properties)
# ---------------------------------------------------------------------------


class StDistance(Function):
    """ST_DISTANCE(g1, g2) - the shortest distance between two geometries, in the SRS's units."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__("ST_DISTANCE", g1, g2)


class StDistanceSphere(Function):
    """
    ST_DISTANCE_SPHERE(g1, g2[, radius])

    The minimum distance between two geometries on a sphere, in meters. The optional radius (in meters, must be
    positive) overrides the default sphere radius, which is Earth's mean radius (6370986 m).
    """

    def __init__(self, g1: Statement | Any, g2: Statement | Any, radius: Statement | Any = None) -> None:
        if radius is not None:
            super().__init__("ST_DISTANCE_SPHERE", g1, g2, radius)
        else:
            super().__init__("ST_DISTANCE_SPHERE", g1, g2)


class StLength(Function):
    """ST_LENGTH(ls) - the length of a LineString or MultiLineString, in the SRS's units."""

    def __init__(self, ls: Statement | Any) -> None:
        super().__init__("ST_LENGTH", ls)


class GLength(StLength):
    """Synonym for ST_LENGTH."""

    def __init__(self, ls: Statement | Any) -> None:
        super().__init__(ls)
        self.function = "GLENGTH"


class StArea(Function):
    """ST_AREA(poly) - the area of a Polygon or MultiPolygon, in the SRS's units."""

    def __init__(self, poly: Statement | Any) -> None:
        super().__init__("ST_AREA", poly)


class Area(StArea):
    """Synonym for ST_AREA."""

    def __init__(self, poly: Statement | Any) -> None:
        super().__init__(poly)
        self.function = "AREA"


# ---------------------------------------------------------------------------
# Accessors / properties (https://mariadb.com/kb/en/geometry-properties/,
# https://mariadb.com/kb/en/linestring-properties/, https://mariadb.com/kb/en/polygon-properties/)
# ---------------------------------------------------------------------------


class StX(Function):
    """
    ST_X(p) - the X-coordinate of a Point. One-argument only: MariaDB rejects the MySQL 8.0 two-argument setter
    form with ER_WRONG_PARAMCOUNT_TO_NATIVE_FCT.
    """

    def __init__(self, point: Statement | Any) -> None:
        super().__init__("ST_X", point)


class X(StX):
    """Synonym for ST_X."""

    def __init__(self, point: Statement | Any) -> None:
        super().__init__(point)
        self.function = "X"


class StY(Function):
    """
    ST_Y(p) - the Y-coordinate of a Point. One-argument only: MariaDB rejects the MySQL 8.0 two-argument setter
    form with ER_WRONG_PARAMCOUNT_TO_NATIVE_FCT.
    """

    def __init__(self, point: Statement | Any) -> None:
        super().__init__("ST_Y", point)


class Y(StY):
    """Synonym for ST_Y."""

    def __init__(self, point: Statement | Any) -> None:
        super().__init__(point)
        self.function = "Y"


class StSrid(Function):
    """
    ST_SRID(g) - the SRID (Spatial Reference Identifier) of a geometry. One-argument only: MariaDB rejects the
    MySQL 8.0 two-argument setter form with ER_WRONG_PARAMCOUNT_TO_NATIVE_FCT.
    """

    def __init__(self, g: Statement | Any) -> None:
        super().__init__("ST_SRID", g)


class Srid(StSrid):
    """Synonym for ST_SRID."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__(g)
        self.function = "SRID"


class StDimension(Function):
    """ST_DIMENSION(g) - the inherent dimension of g: 0 for points, 1 for curves, 2 for surfaces."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__("ST_DIMENSION", g)


class Dimension(StDimension):
    """Synonym for ST_DIMENSION."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__(g)
        self.function = "DIMENSION"


class StGeometryType(Function):
    """ST_GEOMETRYTYPE(g) - the name of g's geometry type, e.g. 'POINT'."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__("ST_GEOMETRYTYPE", g)


class GeometryType(StGeometryType):
    """Synonym for ST_GEOMETRYTYPE."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__(g)
        self.function = "GEOMETRYTYPE"


class StIsEmpty(Function):
    """ST_ISEMPTY(g) - whether g is an empty geometry."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__("ST_ISEMPTY", g)


class IsEmpty(StIsEmpty):
    """Synonym for ST_ISEMPTY."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__(g)
        self.function = "ISEMPTY"


class StIsSimple(Function):
    """ST_ISSIMPLE(g) - whether g has no anomalous geometric points, such as self-intersection or self-tangency."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__("ST_ISSIMPLE", g)


class IsSimple(StIsSimple):
    """Synonym for ST_ISSIMPLE."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__(g)
        self.function = "ISSIMPLE"


class StIsClosed(Function):
    """ST_ISCLOSED(ls) - whether a LineString/MultiLineString's start and end points are the same."""

    def __init__(self, ls: Statement | Any) -> None:
        super().__init__("ST_ISCLOSED", ls)


class IsClosed(StIsClosed):
    """Synonym for ST_ISCLOSED."""

    def __init__(self, ls: Statement | Any) -> None:
        super().__init__(ls)
        self.function = "ISCLOSED"


class StIsRing(Function):
    """ST_ISRING(ls) - whether ls is closed (ST_IsClosed) and simple (ST_IsSimple)."""

    def __init__(self, ls: Statement | Any) -> None:
        super().__init__("ST_ISRING", ls)


class IsRing(StIsRing):
    """Synonym for ST_ISRING."""

    def __init__(self, ls: Statement | Any) -> None:
        super().__init__(ls)
        self.function = "ISRING"


class StIsValid(Function):
    """
    ST_ISVALID(g) - whether g is a valid, OGC-compliant geometry.

    Unlike ST_VALIDATE, raises an error on malformed GIS data instead of returning 0/NULL.

    MariaDB 12.0+.
    """

    def __init__(self, g: Statement | Any) -> None:
        super().__init__("ST_ISVALID", g)


class IsValid(StIsValid):
    """Synonym for ST_ISVALID. MariaDB 12.0+."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__(g)
        self.function = "ISVALID"


class StNumPoints(Function):
    """ST_NUMPOINTS(ls) - the number of Points in a LineString."""

    def __init__(self, ls: Statement | Any) -> None:
        super().__init__("ST_NUMPOINTS", ls)


class NumPoints(StNumPoints):
    """Synonym for ST_NUMPOINTS."""

    def __init__(self, ls: Statement | Any) -> None:
        super().__init__(ls)
        self.function = "NUMPOINTS"


class StPointN(Function):
    """ST_POINTN(ls, n) - the N-th Point in a LineString (1-based)."""

    def __init__(self, ls: Statement | Any, n: Statement | Any) -> None:
        super().__init__("ST_POINTN", ls, n)


class PointN(StPointN):
    """Synonym for ST_POINTN."""

    def __init__(self, ls: Statement | Any, n: Statement | Any) -> None:
        super().__init__(ls, n)
        self.function = "POINTN"


class StStartPoint(Function):
    """ST_STARTPOINT(ls) - the first Point of a LineString."""

    def __init__(self, ls: Statement | Any) -> None:
        super().__init__("ST_STARTPOINT", ls)


class StartPoint(StStartPoint):
    """Synonym for ST_STARTPOINT."""

    def __init__(self, ls: Statement | Any) -> None:
        super().__init__(ls)
        self.function = "STARTPOINT"


class StEndPoint(Function):
    """ST_ENDPOINT(ls) - the last Point of a LineString."""

    def __init__(self, ls: Statement | Any) -> None:
        super().__init__("ST_ENDPOINT", ls)


class EndPoint(StEndPoint):
    """Synonym for ST_ENDPOINT."""

    def __init__(self, ls: Statement | Any) -> None:
        super().__init__(ls)
        self.function = "ENDPOINT"


class StExteriorRing(Function):
    """ST_EXTERIORRING(poly) - the exterior ring of a Polygon, as a LineString."""

    def __init__(self, poly: Statement | Any) -> None:
        super().__init__("ST_EXTERIORRING", poly)


class ExteriorRing(StExteriorRing):
    """Synonym for ST_EXTERIORRING."""

    def __init__(self, poly: Statement | Any) -> None:
        super().__init__(poly)
        self.function = "EXTERIORRING"


class StInteriorRingN(Function):
    """ST_INTERIORRINGN(poly, n) - the N-th interior ring of a Polygon, as a LineString (1-based)."""

    def __init__(self, poly: Statement | Any, n: Statement | Any) -> None:
        super().__init__("ST_INTERIORRINGN", poly, n)


class InteriorRingN(StInteriorRingN):
    """Synonym for ST_INTERIORRINGN."""

    def __init__(self, poly: Statement | Any, n: Statement | Any) -> None:
        super().__init__(poly, n)
        self.function = "INTERIORRINGN"


class StNumInteriorRings(Function):
    """ST_NUMINTERIORRINGS(poly) - the number of interior rings in a Polygon."""

    def __init__(self, poly: Statement | Any) -> None:
        super().__init__("ST_NUMINTERIORRINGS", poly)


class NumInteriorRings(StNumInteriorRings):
    """Synonym for ST_NUMINTERIORRINGS."""

    def __init__(self, poly: Statement | Any) -> None:
        super().__init__(poly)
        self.function = "NUMINTERIORRINGS"


class StNumGeometries(Function):
    """ST_NUMGEOMETRIES(gc) - the number of geometries in a GeometryCollection."""

    def __init__(self, gc: Statement | Any) -> None:
        super().__init__("ST_NUMGEOMETRIES", gc)


class NumGeometries(StNumGeometries):
    """Synonym for ST_NUMGEOMETRIES."""

    def __init__(self, gc: Statement | Any) -> None:
        super().__init__(gc)
        self.function = "NUMGEOMETRIES"


class StGeometryN(Function):
    """ST_GEOMETRYN(gc, n) - the N-th geometry in a GeometryCollection (1-based)."""

    def __init__(self, gc: Statement | Any, n: Statement | Any) -> None:
        super().__init__("ST_GEOMETRYN", gc, n)


class GeometryN(StGeometryN):
    """Synonym for ST_GEOMETRYN."""

    def __init__(self, gc: Statement | Any, n: Statement | Any) -> None:
        super().__init__(gc, n)
        self.function = "GEOMETRYN"


class StEnvelope(Function):
    """
    ST_ENVELOPE(g) - the bounding box of g, as a Polygon:
    `POLYGON((MINX MINY, MAXX MINY, MAXX MAXY, MINX MAXY, MINX MINY))`.
    """

    def __init__(self, g: Statement | Any) -> None:
        super().__init__("ST_ENVELOPE", g)


class Envelope(StEnvelope):
    """Synonym for ST_ENVELOPE."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__(g)
        self.function = "ENVELOPE"


class StBoundary(Function):
    """ST_BOUNDARY(g) - the combinatorial boundary of g."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__("ST_BOUNDARY", g)


class Boundary(StBoundary):
    """Synonym for ST_BOUNDARY."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__(g)
        self.function = "BOUNDARY"


class StCentroid(Function):
    """ST_CENTROID(poly) - the mathematical centroid of a Polygon/MultiPolygon, as a Point."""

    def __init__(self, poly: Statement | Any) -> None:
        super().__init__("ST_CENTROID", poly)


class Centroid(StCentroid):
    """Synonym for ST_CENTROID."""

    def __init__(self, poly: Statement | Any) -> None:
        super().__init__(poly)
        self.function = "CENTROID"


class StPointOnSurface(Function):
    """ST_POINTONSURFACE(poly) - a Point guaranteed to be on the surface of poly."""

    def __init__(self, poly: Statement | Any) -> None:
        super().__init__("ST_POINTONSURFACE", poly)


class PointOnSurface(StPointOnSurface):
    """Synonym for ST_POINTONSURFACE."""

    def __init__(self, poly: Statement | Any) -> None:
        super().__init__(poly)
        self.function = "POINTONSURFACE"


# ---------------------------------------------------------------------------
# Operations (https://mariadb.com/docs/server/reference/sql-statements/geometry-constructors/
# miscellaneous-gis-functions)
# ---------------------------------------------------------------------------


class StBuffer(Function):
    """ST_BUFFER(g, r) - a geometry representing all points within distance r of g."""

    def __init__(self, g: Statement | Any, r: Statement | Any) -> None:
        super().__init__("ST_BUFFER", g, r)


class Buffer(StBuffer):
    """Synonym for ST_BUFFER."""

    def __init__(self, g: Statement | Any, r: Statement | Any) -> None:
        super().__init__(g, r)
        self.function = "BUFFER"


class StConvexHull(Function):
    """ST_CONVEXHULL(g) - the smallest convex polygon that encloses g."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__("ST_CONVEXHULL", g)


class ConvexHull(StConvexHull):
    """Synonym for ST_CONVEXHULL."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__(g)
        self.function = "CONVEXHULL"


class StDifference(Function):
    """ST_DIFFERENCE(g1, g2) - the geometry representing the points in g1 that are not in g2."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__("ST_DIFFERENCE", g1, g2)


class StIntersection(Function):
    """ST_INTERSECTION(g1, g2) - the geometry representing the shared points of g1 and g2."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__("ST_INTERSECTION", g1, g2)


class StSymDifference(Function):
    """ST_SYMDIFFERENCE(g1, g2) - the geometry representing the points in g1 or g2, but not both."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__("ST_SYMDIFFERENCE", g1, g2)


class StUnion(Function):
    """ST_UNION(g1, g2) - the geometry representing all points in g1 or g2."""

    def __init__(self, g1: Statement | Any, g2: Statement | Any) -> None:
        super().__init__("ST_UNION", g1, g2)


class StSimplify(Function):
    """
    ST_SIMPLIFY(g, max_distance) - a simplified version of g, using the Ramer-Douglas-Peucker algorithm with the
    given distance tolerance. The result may become invalid (e.g. self-intersecting); check it with ST_ISVALID.

    MariaDB 12.0+.
    """

    def __init__(self, g: Statement | Any, max_distance: Statement | Any) -> None:
        super().__init__("ST_SIMPLIFY", g, max_distance)


class Simplify(StSimplify):
    """Synonym for ST_SIMPLIFY. MariaDB 12.0+."""

    def __init__(self, g: Statement | Any, max_distance: Statement | Any) -> None:
        super().__init__(g, max_distance)
        self.function = "SIMPLIFY"


class StValidate(Function):
    """
    ST_VALIDATE(g) - g itself if it is valid (reversing the rings of a clockwise Polygon/MultiPolygon first),
    or NULL if it is not.

    MariaDB 12.0+.
    """

    def __init__(self, g: Statement | Any) -> None:
        super().__init__("ST_VALIDATE", g)


class Validate(StValidate):
    """Synonym for ST_VALIDATE. MariaDB 12.0+."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__(g)
        self.function = "VALIDATE"


class StCollect(AggregateFunction):
    """
    - ST_COLLECT(g)
    - ST_COLLECT(DISTINCT g)

    Aggregate function (usable as a window function too) that collects the non-NULL geometries of a group into a
    single MultiPoint, MultiLineString, MultiPolygon or GeometryCollection - whichever type can represent them.

    MariaDB 12.0+.
    """

    #: Unlike most aggregates, MariaDB accepts ``ST_COLLECT(DISTINCT g) OVER (...)`` (verified on 13.0.2).
    _distinct_over = True

    def __init__(self, geometry: ColumnArg | Statement, *, distinct: bool = False) -> None:
        super().__init__("ST_COLLECT", geometry, distinct=distinct)


# ---------------------------------------------------------------------------
# Output (https://mariadb.com/kb/en/st_astext/, st_asbinary, st_asgeojson, geohash functions)
# ---------------------------------------------------------------------------


class StAsText(Function):
    """ST_ASTEXT(g) - the Well-Known Text (WKT) representation of g."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__("ST_ASTEXT", g)


class AsText(StAsText):
    """Synonym for ST_ASTEXT."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__(g)
        self.function = "ASTEXT"


class StAsWkt(StAsText):
    """Synonym for ST_ASTEXT."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__(g)
        self.function = "ST_ASWKT"


class AsWkt(StAsText):
    """Synonym for ST_ASTEXT."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__(g)
        self.function = "ASWKT"


class StAsBinary(Function):
    """ST_ASBINARY(g) - the Well-Known Binary (WKB) representation of g."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__("ST_ASBINARY", g)


class AsBinary(StAsBinary):
    """Synonym for ST_ASBINARY."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__(g)
        self.function = "ASBINARY"


class StAsWkb(StAsBinary):
    """Synonym for ST_ASBINARY."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__(g)
        self.function = "ST_ASWKB"


class AsWkb(StAsBinary):
    """Synonym for ST_ASBINARY."""

    def __init__(self, g: Statement | Any) -> None:
        super().__init__(g)
        self.function = "ASWKB"


class StAsGeoJson(Function):
    """
    ST_ASGEOJSON(g[, max_decimals[, options]])

    The GeoJSON representation of g. max_decimals limits the number of decimal digits in the coordinates.
    options can be set to 1 to add a bounding box to the output; since the arguments are positional, options can
    only be given together with max_decimals - passing options without max_decimals raises ValueError instead of
    silently dropping it.
    """

    def __init__(self, g: Statement | Any, max_decimals: Statement | Any = None, options: Statement | Any = None) -> None:
        if options is not None and max_decimals is None:
            raise ValueError("StAsGeoJson: max_decimals must be given when options is given (arguments are positional).")

        args: list[Statement | Any] = [g]

        if max_decimals is not None:
            args.append(max_decimals)

            if options is not None:
                args.append(options)

        super().__init__("ST_ASGEOJSON", *args)


class StGeoHash(Function):
    """
    - ST_GEOHASH(longitude, latitude, max_length)
    - ST_GEOHASH(point, max_length)

    Encodes a location (as longitude/latitude, or as a Point where X is longitude and Y is latitude) into a
    geohash string of at most max_length characters.

    MariaDB 12.0+.
    """

    @overload
    def __init__(self, point: Statement | Any, max_length: Statement | Any, /) -> None: ...

    @overload
    def __init__(self, longitude: Statement | Any, latitude: Statement | Any, max_length: Statement | Any, /) -> None: ...

    def __init__(self, *args: Statement | Any) -> None:
        if len(args) not in (2, 3):
            raise TypeError(f"StGeoHash takes 2 (point, max_length) or 3 (lon, lat, max_length) arguments, got {len(args)}.")

        super().__init__("ST_GEOHASH", *args)


class GeoHash(StGeoHash):
    """
    - GEOHASH(longitude, latitude, max_length)
    - GEOHASH(point, max_length)

    Synonym for ST_GEOHASH. MariaDB 12.0+.
    """

    @overload
    def __init__(self, point: Statement | Any, max_length: Statement | Any, /) -> None: ...

    @overload
    def __init__(self, longitude: Statement | Any, latitude: Statement | Any, max_length: Statement | Any, /) -> None: ...

    def __init__(self, *args: Statement | Any) -> None:
        super().__init__(*args)
        self.function = "GEOHASH"


class StLatFromGeoHash(Function):
    """ST_LATFROMGEOHASH(geohash) - decodes geohash and returns its latitude, in [-90, 90]. MariaDB 12.0+."""

    def __init__(self, geohash: Statement | Any) -> None:
        super().__init__("ST_LATFROMGEOHASH", geohash)


class LatFromGeoHash(StLatFromGeoHash):
    """Synonym for ST_LATFROMGEOHASH. MariaDB 12.0+."""

    def __init__(self, geohash: Statement | Any) -> None:
        super().__init__(geohash)
        self.function = "LATFROMGEOHASH"


class StLongFromGeoHash(Function):
    """ST_LONGFROMGEOHASH(geohash) - decodes geohash and returns its longitude, in [-180, 180]. MariaDB 12.0+."""

    def __init__(self, geohash: Statement | Any) -> None:
        super().__init__("ST_LONGFROMGEOHASH", geohash)


class LongFromGeoHash(StLongFromGeoHash):
    """Synonym for ST_LONGFROMGEOHASH. MariaDB 12.0+."""

    def __init__(self, geohash: Statement | Any) -> None:
        super().__init__(geohash)
        self.function = "LONGFROMGEOHASH"
