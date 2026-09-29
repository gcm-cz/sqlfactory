"""Tests for geometry constructor functions."""

from sqlfactory import Column, Eq, Insert, Raw, Select, SQLiteDialect, Update
from sqlfactory.func.geometry import (
    GeomCollFromText,
    GeomCollFromWkb,
    GeometryCollection,
    GeometryCollectionFromText,
    GeometryCollectionFromWkb,
    GeometryFromText,
    GeometryFromWkb,
    GeomFromText,
    GeomFromWkb,
    LineFromText,
    LineFromWkb,
    LineString,
    LineStringFromText,
    LineStringFromWkb,
    MLineFromText,
    MLineFromWkb,
    MPointFromText,
    MPointFromWkb,
    MPolyFromText,
    MPolyFromWkb,
    MultiLineString,
    MultiLineStringFromText,
    MultiLineStringFromWkb,
    MultiPoint,
    MultiPointFromText,
    MultiPointFromWkb,
    MultiPolygon,
    MultiPolygonFromText,
    MultiPolygonFromWkb,
    Point,
    PointFromGeoHash,
    PointFromText,
    PointFromWkb,
    PolyFromText,
    PolyFromWkb,
    Polygon,
    PolygonFromText,
    PolygonFromWkb,
    StGeomCollFromText,
    StGeomCollFromWkb,
    StGeomFromGeoJson,
    StGeomFromText,
    StGeomFromWkb,
    StGeometryCollectionFromText,
    StGeometryCollectionFromWkb,
    StGeometryFromText,
    StGeometryFromWkb,
    StLineFromText,
    StLineFromWkb,
    StLineStringFromText,
    StLineStringFromWkb,
    StMLineFromText,
    StMLineFromWkb,
    StMPointFromText,
    StMPointFromWkb,
    StMPolyFromText,
    StMPolyFromWkb,
    StMultiLineStringFromText,
    StMultiLineStringFromWkb,
    StMultiPointFromText,
    StMultiPointFromWkb,
    StMultiPolygonFromText,
    StMultiPolygonFromWkb,
    StPointFromGeoHash,
    StPointFromText,
    StPointFromWkb,
    StPolyFromText,
    StPolyFromWkb,
    StPolygonFromText,
    StPolygonFromWkb,
)

# ---------------------------------------------------------------------------
# Structure constructors
# ---------------------------------------------------------------------------


def test_point():
    p = Point(1, 2)
    assert str(p) == "POINT(%s, %s)"
    assert p.args == [1, 2]


def test_point_with_statement_args():
    p = Point(Column("t.lon"), Column("t.lat"))
    assert str(p) == "POINT(`t`.`lon`, `t`.`lat`)"
    assert p.args == []


def test_linestring():
    ls = LineString(Point(1, 1), Point(2, 2))
    assert str(ls) == "LINESTRING(POINT(%s, %s), POINT(%s, %s))"
    assert ls.args == [1, 1, 2, 2]


def test_polygon():
    poly = Polygon(LineString(Point(0, 0), Point(0, 1), Point(1, 1), Point(0, 0)))
    assert str(poly) == "POLYGON(LINESTRING(POINT(%s, %s), POINT(%s, %s), POINT(%s, %s), POINT(%s, %s)))"
    assert poly.args == [0, 0, 0, 1, 1, 1, 0, 0]


def test_polygon_with_hole():
    exterior = LineString(Point(0, 0), Point(0, 50), Point(50, 50), Point(0, 0))
    hole = LineString(Point(10, 10), Point(10, 20), Point(20, 20), Point(10, 10))
    poly = Polygon(exterior, hole)
    assert str(poly) == (
        "POLYGON(LINESTRING(POINT(%s, %s), POINT(%s, %s), POINT(%s, %s), POINT(%s, %s)), "
        "LINESTRING(POINT(%s, %s), POINT(%s, %s), POINT(%s, %s), POINT(%s, %s)))"
    )
    assert poly.args == [0, 0, 0, 50, 50, 50, 0, 0, 10, 10, 10, 20, 20, 20, 10, 10]


def test_multipoint():
    mp = MultiPoint(Point(1, 1), Point(2, 2))
    assert str(mp) == "MULTIPOINT(POINT(%s, %s), POINT(%s, %s))"
    assert mp.args == [1, 1, 2, 2]


def test_multilinestring():
    mls = MultiLineString(LineString(Point(0, 0), Point(1, 1)), LineString(Point(2, 2), Point(3, 3)))
    assert str(mls) == "MULTILINESTRING(LINESTRING(POINT(%s, %s), POINT(%s, %s)), LINESTRING(POINT(%s, %s), POINT(%s, %s)))"
    assert mls.args == [0, 0, 1, 1, 2, 2, 3, 3]


def test_multipolygon():
    poly1 = Polygon(LineString(Point(0, 0), Point(0, 1), Point(1, 1), Point(0, 0)))
    poly2 = Polygon(LineString(Point(5, 5), Point(5, 6), Point(6, 6), Point(5, 5)))
    mpoly = MultiPolygon(poly1, poly2)
    assert str(mpoly) == (
        "MULTIPOLYGON(POLYGON(LINESTRING(POINT(%s, %s), POINT(%s, %s), POINT(%s, %s), POINT(%s, %s))), "
        "POLYGON(LINESTRING(POINT(%s, %s), POINT(%s, %s), POINT(%s, %s), POINT(%s, %s))))"
    )
    assert mpoly.args == [0, 0, 0, 1, 1, 1, 0, 0, 5, 5, 5, 6, 6, 6, 5, 5]


def test_geometrycollection():
    gc = GeometryCollection(Point(0, 0), LineString(Point(0, 1), Point(0, 2)))
    assert str(gc) == "GEOMETRYCOLLECTION(POINT(%s, %s), LINESTRING(POINT(%s, %s), POINT(%s, %s)))"
    assert gc.args == [0, 0, 0, 1, 0, 2]


# ---------------------------------------------------------------------------
# WKT constructors: ST_GeomFromText and synonyms
# ---------------------------------------------------------------------------


def test_st_geom_from_text():
    g = StGeomFromText("POINT(1 1)")
    assert str(g) == "ST_GEOMFROMTEXT(%s)"
    assert g.args == ["POINT(1 1)"]

    g_srid = StGeomFromText("POINT(1 1)", 4326)
    assert str(g_srid) == "ST_GEOMFROMTEXT(%s, %s)"
    assert g_srid.args == ["POINT(1 1)", 4326]

    g_stmt = StGeomFromText(Raw("%s", "POINT(1 1)"), 4326)
    assert str(g_stmt) == "ST_GEOMFROMTEXT(%s, %s)"
    assert g_stmt.args == ["POINT(1 1)", 4326]


def test_st_geometry_from_text():
    g = StGeometryFromText("POINT(1 1)")
    assert str(g) == "ST_GEOMETRYFROMTEXT(%s)"
    assert g.args == ["POINT(1 1)"]

    g_srid = StGeometryFromText("POINT(1 1)", 4326)
    assert str(g_srid) == "ST_GEOMETRYFROMTEXT(%s, %s)"
    assert g_srid.args == ["POINT(1 1)", 4326]


def test_geom_from_text():
    g = GeomFromText("POINT(1 1)")
    assert str(g) == "GEOMFROMTEXT(%s)"
    assert g.args == ["POINT(1 1)"]


def test_geometry_from_text():
    g = GeometryFromText("POINT(1 1)")
    assert str(g) == "GEOMETRYFROMTEXT(%s)"
    assert g.args == ["POINT(1 1)"]


# ---------------------------------------------------------------------------
# WKT constructors: ST_PointFromText and synonyms
# ---------------------------------------------------------------------------


def test_st_point_from_text():
    p = StPointFromText("POINT(1 1)")
    assert str(p) == "ST_POINTFROMTEXT(%s)"
    assert p.args == ["POINT(1 1)"]

    p_srid = StPointFromText("POINT(1 1)", 4326)
    assert str(p_srid) == "ST_POINTFROMTEXT(%s, %s)"
    assert p_srid.args == ["POINT(1 1)", 4326]


def test_point_from_text():
    p = PointFromText("POINT(1 1)")
    assert str(p) == "POINTFROMTEXT(%s)"
    assert p.args == ["POINT(1 1)"]

    p_srid = PointFromText("POINT(1 1)", 4326)
    assert str(p_srid) == "POINTFROMTEXT(%s, %s)"
    assert p_srid.args == ["POINT(1 1)", 4326]


# ---------------------------------------------------------------------------
# WKT constructors: ST_LineFromText and synonyms
# ---------------------------------------------------------------------------


def test_st_line_from_text():
    line = StLineFromText("LINESTRING(0 0,1 1)")
    assert str(line) == "ST_LINEFROMTEXT(%s)"
    assert line.args == ["LINESTRING(0 0,1 1)"]

    line_srid = StLineFromText("LINESTRING(0 0,1 1)", 4326)
    assert str(line_srid) == "ST_LINEFROMTEXT(%s, %s)"
    assert line_srid.args == ["LINESTRING(0 0,1 1)", 4326]


def test_st_line_string_from_text():
    line = StLineStringFromText("LINESTRING(0 0,1 1)")
    assert str(line) == "ST_LINESTRINGFROMTEXT(%s)"
    assert line.args == ["LINESTRING(0 0,1 1)"]

    line_srid = StLineStringFromText("LINESTRING(0 0,1 1)", 4326)
    assert str(line_srid) == "ST_LINESTRINGFROMTEXT(%s, %s)"
    assert line_srid.args == ["LINESTRING(0 0,1 1)", 4326]


def test_line_from_text():
    line = LineFromText("LINESTRING(0 0,1 1)")
    assert str(line) == "LINEFROMTEXT(%s)"
    assert line.args == ["LINESTRING(0 0,1 1)"]


def test_line_string_from_text():
    line = LineStringFromText("LINESTRING(0 0,1 1)")
    assert str(line) == "LINESTRINGFROMTEXT(%s)"
    assert line.args == ["LINESTRING(0 0,1 1)"]


# ---------------------------------------------------------------------------
# WKT constructors: ST_PolyFromText and synonyms
# ---------------------------------------------------------------------------


def test_st_poly_from_text():
    poly = StPolyFromText("POLYGON((0 0,0 1,1 1,0 0))")
    assert str(poly) == "ST_POLYFROMTEXT(%s)"
    assert poly.args == ["POLYGON((0 0,0 1,1 1,0 0))"]

    poly_srid = StPolyFromText("POLYGON((0 0,0 1,1 1,0 0))", 4326)
    assert str(poly_srid) == "ST_POLYFROMTEXT(%s, %s)"
    assert poly_srid.args == ["POLYGON((0 0,0 1,1 1,0 0))", 4326]


def test_st_polygon_from_text():
    poly = StPolygonFromText("POLYGON((0 0,0 1,1 1,0 0))")
    assert str(poly) == "ST_POLYGONFROMTEXT(%s)"
    assert poly.args == ["POLYGON((0 0,0 1,1 1,0 0))"]

    poly_srid = StPolygonFromText("POLYGON((0 0,0 1,1 1,0 0))", 4326)
    assert str(poly_srid) == "ST_POLYGONFROMTEXT(%s, %s)"
    assert poly_srid.args == ["POLYGON((0 0,0 1,1 1,0 0))", 4326]


def test_poly_from_text():
    poly = PolyFromText("POLYGON((0 0,0 1,1 1,0 0))")
    assert str(poly) == "POLYFROMTEXT(%s)"
    assert poly.args == ["POLYGON((0 0,0 1,1 1,0 0))"]


def test_polygon_from_text():
    poly = PolygonFromText("POLYGON((0 0,0 1,1 1,0 0))")
    assert str(poly) == "POLYGONFROMTEXT(%s)"
    assert poly.args == ["POLYGON((0 0,0 1,1 1,0 0))"]


# ---------------------------------------------------------------------------
# WKT constructors: ST_MultiPointFromText and synonyms
# ---------------------------------------------------------------------------


def test_st_multi_point_from_text():
    mp = StMultiPointFromText("MULTIPOINT(0 0,1 1)")
    assert str(mp) == "ST_MULTIPOINTFROMTEXT(%s)"
    assert mp.args == ["MULTIPOINT(0 0,1 1)"]

    mp_srid = StMultiPointFromText("MULTIPOINT(0 0,1 1)", 4326)
    assert str(mp_srid) == "ST_MULTIPOINTFROMTEXT(%s, %s)"
    assert mp_srid.args == ["MULTIPOINT(0 0,1 1)", 4326]


def test_st_m_point_from_text():
    mp = StMPointFromText("MULTIPOINT(0 0,1 1)")
    assert str(mp) == "ST_MPOINTFROMTEXT(%s)"
    assert mp.args == ["MULTIPOINT(0 0,1 1)"]

    mp_srid = StMPointFromText("MULTIPOINT(0 0,1 1)", 4326)
    assert str(mp_srid) == "ST_MPOINTFROMTEXT(%s, %s)"
    assert mp_srid.args == ["MULTIPOINT(0 0,1 1)", 4326]


def test_multi_point_from_text():
    mp = MultiPointFromText("MULTIPOINT(0 0,1 1)")
    assert str(mp) == "MULTIPOINTFROMTEXT(%s)"
    assert mp.args == ["MULTIPOINT(0 0,1 1)"]


def test_m_point_from_text():
    mp = MPointFromText("MULTIPOINT(0 0,1 1)")
    assert str(mp) == "MPOINTFROMTEXT(%s)"
    assert mp.args == ["MULTIPOINT(0 0,1 1)"]


# ---------------------------------------------------------------------------
# WKT constructors: ST_MultiLineStringFromText and synonyms
# ---------------------------------------------------------------------------


def test_st_multi_line_string_from_text():
    mls = StMultiLineStringFromText("MULTILINESTRING((0 0,1 1))")
    assert str(mls) == "ST_MULTILINESTRINGFROMTEXT(%s)"
    assert mls.args == ["MULTILINESTRING((0 0,1 1))"]

    mls_srid = StMultiLineStringFromText("MULTILINESTRING((0 0,1 1))", 4326)
    assert str(mls_srid) == "ST_MULTILINESTRINGFROMTEXT(%s, %s)"
    assert mls_srid.args == ["MULTILINESTRING((0 0,1 1))", 4326]


def test_st_m_line_from_text():
    mls = StMLineFromText("MULTILINESTRING((0 0,1 1))")
    assert str(mls) == "ST_MLINEFROMTEXT(%s)"
    assert mls.args == ["MULTILINESTRING((0 0,1 1))"]

    mls_srid = StMLineFromText("MULTILINESTRING((0 0,1 1))", 4326)
    assert str(mls_srid) == "ST_MLINEFROMTEXT(%s, %s)"
    assert mls_srid.args == ["MULTILINESTRING((0 0,1 1))", 4326]


def test_multi_line_string_from_text():
    mls = MultiLineStringFromText("MULTILINESTRING((0 0,1 1))")
    assert str(mls) == "MULTILINESTRINGFROMTEXT(%s)"
    assert mls.args == ["MULTILINESTRING((0 0,1 1))"]


def test_m_line_from_text():
    mls = MLineFromText("MULTILINESTRING((0 0,1 1))")
    assert str(mls) == "MLINEFROMTEXT(%s)"
    assert mls.args == ["MULTILINESTRING((0 0,1 1))"]


# ---------------------------------------------------------------------------
# WKT constructors: ST_MultiPolygonFromText and synonyms
# ---------------------------------------------------------------------------


def test_st_multi_polygon_from_text():
    mpoly = StMultiPolygonFromText("MULTIPOLYGON(((0 0,0 1,1 1,0 0)))")
    assert str(mpoly) == "ST_MULTIPOLYGONFROMTEXT(%s)"
    assert mpoly.args == ["MULTIPOLYGON(((0 0,0 1,1 1,0 0)))"]

    mpoly_srid = StMultiPolygonFromText("MULTIPOLYGON(((0 0,0 1,1 1,0 0)))", 4326)
    assert str(mpoly_srid) == "ST_MULTIPOLYGONFROMTEXT(%s, %s)"
    assert mpoly_srid.args == ["MULTIPOLYGON(((0 0,0 1,1 1,0 0)))", 4326]


def test_st_m_poly_from_text():
    mpoly = StMPolyFromText("MULTIPOLYGON(((0 0,0 1,1 1,0 0)))")
    assert str(mpoly) == "ST_MPOLYFROMTEXT(%s)"
    assert mpoly.args == ["MULTIPOLYGON(((0 0,0 1,1 1,0 0)))"]

    mpoly_srid = StMPolyFromText("MULTIPOLYGON(((0 0,0 1,1 1,0 0)))", 4326)
    assert str(mpoly_srid) == "ST_MPOLYFROMTEXT(%s, %s)"
    assert mpoly_srid.args == ["MULTIPOLYGON(((0 0,0 1,1 1,0 0)))", 4326]


def test_multi_polygon_from_text():
    mpoly = MultiPolygonFromText("MULTIPOLYGON(((0 0,0 1,1 1,0 0)))")
    assert str(mpoly) == "MULTIPOLYGONFROMTEXT(%s)"
    assert mpoly.args == ["MULTIPOLYGON(((0 0,0 1,1 1,0 0)))"]


def test_m_poly_from_text():
    mpoly = MPolyFromText("MULTIPOLYGON(((0 0,0 1,1 1,0 0)))")
    assert str(mpoly) == "MPOLYFROMTEXT(%s)"
    assert mpoly.args == ["MULTIPOLYGON(((0 0,0 1,1 1,0 0)))"]


# ---------------------------------------------------------------------------
# WKT constructors: ST_GeomCollFromText and synonyms
# ---------------------------------------------------------------------------


def test_st_geom_coll_from_text():
    gc = StGeomCollFromText("GEOMETRYCOLLECTION(POINT(0 0))")
    assert str(gc) == "ST_GEOMCOLLFROMTEXT(%s)"
    assert gc.args == ["GEOMETRYCOLLECTION(POINT(0 0))"]

    gc_srid = StGeomCollFromText("GEOMETRYCOLLECTION(POINT(0 0))", 4326)
    assert str(gc_srid) == "ST_GEOMCOLLFROMTEXT(%s, %s)"
    assert gc_srid.args == ["GEOMETRYCOLLECTION(POINT(0 0))", 4326]


def test_st_geometry_collection_from_text():
    gc = StGeometryCollectionFromText("GEOMETRYCOLLECTION(POINT(0 0))")
    assert str(gc) == "ST_GEOMETRYCOLLECTIONFROMTEXT(%s)"
    assert gc.args == ["GEOMETRYCOLLECTION(POINT(0 0))"]

    gc_srid = StGeometryCollectionFromText("GEOMETRYCOLLECTION(POINT(0 0))", 4326)
    assert str(gc_srid) == "ST_GEOMETRYCOLLECTIONFROMTEXT(%s, %s)"
    assert gc_srid.args == ["GEOMETRYCOLLECTION(POINT(0 0))", 4326]


def test_geom_coll_from_text():
    gc = GeomCollFromText("GEOMETRYCOLLECTION(POINT(0 0))")
    assert str(gc) == "GEOMCOLLFROMTEXT(%s)"
    assert gc.args == ["GEOMETRYCOLLECTION(POINT(0 0))"]


def test_geometry_collection_from_text():
    gc = GeometryCollectionFromText("GEOMETRYCOLLECTION(POINT(0 0))")
    assert str(gc) == "GEOMETRYCOLLECTIONFROMTEXT(%s)"
    assert gc.args == ["GEOMETRYCOLLECTION(POINT(0 0))"]


# ---------------------------------------------------------------------------
# WKB constructors: ST_GeomFromWKB and synonyms
# ---------------------------------------------------------------------------


def test_st_geom_from_wkb():
    g = StGeomFromWkb(b"\x00\x01")
    assert str(g) == "ST_GEOMFROMWKB(%s)"
    assert g.args == [b"\x00\x01"]

    g_srid = StGeomFromWkb(b"\x00\x01", 4326)
    assert str(g_srid) == "ST_GEOMFROMWKB(%s, %s)"
    assert g_srid.args == [b"\x00\x01", 4326]

    g_stmt = StGeomFromWkb(Raw("%s", b"\x00\x01"), 4326)
    assert str(g_stmt) == "ST_GEOMFROMWKB(%s, %s)"
    assert g_stmt.args == [b"\x00\x01", 4326]


def test_st_geometry_from_wkb():
    g = StGeometryFromWkb(b"\x00\x01")
    assert str(g) == "ST_GEOMETRYFROMWKB(%s)"
    assert g.args == [b"\x00\x01"]

    g_srid = StGeometryFromWkb(b"\x00\x01", 4326)
    assert str(g_srid) == "ST_GEOMETRYFROMWKB(%s, %s)"
    assert g_srid.args == [b"\x00\x01", 4326]


def test_geom_from_wkb():
    g = GeomFromWkb(b"\x00\x01")
    assert str(g) == "GEOMFROMWKB(%s)"
    assert g.args == [b"\x00\x01"]


def test_geometry_from_wkb():
    g = GeometryFromWkb(b"\x00\x01")
    assert str(g) == "GEOMETRYFROMWKB(%s)"
    assert g.args == [b"\x00\x01"]


# ---------------------------------------------------------------------------
# WKB constructors: ST_PointFromWKB and synonyms
# ---------------------------------------------------------------------------


def test_st_point_from_wkb():
    p = StPointFromWkb(b"\x00\x01")
    assert str(p) == "ST_POINTFROMWKB(%s)"
    assert p.args == [b"\x00\x01"]

    p_srid = StPointFromWkb(b"\x00\x01", 4326)
    assert str(p_srid) == "ST_POINTFROMWKB(%s, %s)"
    assert p_srid.args == [b"\x00\x01", 4326]


def test_point_from_wkb():
    p = PointFromWkb(b"\x00\x01")
    assert str(p) == "POINTFROMWKB(%s)"
    assert p.args == [b"\x00\x01"]

    p_srid = PointFromWkb(b"\x00\x01", 4326)
    assert str(p_srid) == "POINTFROMWKB(%s, %s)"
    assert p_srid.args == [b"\x00\x01", 4326]


# ---------------------------------------------------------------------------
# WKB constructors: ST_LineFromWKB and synonyms
# ---------------------------------------------------------------------------


def test_st_line_from_wkb():
    line = StLineFromWkb(b"\x00\x01")
    assert str(line) == "ST_LINEFROMWKB(%s)"
    assert line.args == [b"\x00\x01"]

    line_srid = StLineFromWkb(b"\x00\x01", 4326)
    assert str(line_srid) == "ST_LINEFROMWKB(%s, %s)"
    assert line_srid.args == [b"\x00\x01", 4326]


def test_st_line_string_from_wkb():
    line = StLineStringFromWkb(b"\x00\x01")
    assert str(line) == "ST_LINESTRINGFROMWKB(%s)"
    assert line.args == [b"\x00\x01"]

    line_srid = StLineStringFromWkb(b"\x00\x01", 4326)
    assert str(line_srid) == "ST_LINESTRINGFROMWKB(%s, %s)"
    assert line_srid.args == [b"\x00\x01", 4326]


def test_line_from_wkb():
    line = LineFromWkb(b"\x00\x01")
    assert str(line) == "LINEFROMWKB(%s)"
    assert line.args == [b"\x00\x01"]


def test_line_string_from_wkb():
    line = LineStringFromWkb(b"\x00\x01")
    assert str(line) == "LINESTRINGFROMWKB(%s)"
    assert line.args == [b"\x00\x01"]


# ---------------------------------------------------------------------------
# WKB constructors: ST_PolyFromWKB and synonyms
# ---------------------------------------------------------------------------


def test_st_poly_from_wkb():
    poly = StPolyFromWkb(b"\x00\x01")
    assert str(poly) == "ST_POLYFROMWKB(%s)"
    assert poly.args == [b"\x00\x01"]

    poly_srid = StPolyFromWkb(b"\x00\x01", 4326)
    assert str(poly_srid) == "ST_POLYFROMWKB(%s, %s)"
    assert poly_srid.args == [b"\x00\x01", 4326]


def test_st_polygon_from_wkb():
    poly = StPolygonFromWkb(b"\x00\x01")
    assert str(poly) == "ST_POLYGONFROMWKB(%s)"
    assert poly.args == [b"\x00\x01"]

    poly_srid = StPolygonFromWkb(b"\x00\x01", 4326)
    assert str(poly_srid) == "ST_POLYGONFROMWKB(%s, %s)"
    assert poly_srid.args == [b"\x00\x01", 4326]


def test_poly_from_wkb():
    poly = PolyFromWkb(b"\x00\x01")
    assert str(poly) == "POLYFROMWKB(%s)"
    assert poly.args == [b"\x00\x01"]


def test_polygon_from_wkb():
    poly = PolygonFromWkb(b"\x00\x01")
    assert str(poly) == "POLYGONFROMWKB(%s)"
    assert poly.args == [b"\x00\x01"]


# ---------------------------------------------------------------------------
# WKB constructors: ST_MultiPointFromWKB and synonyms
# ---------------------------------------------------------------------------


def test_st_multi_point_from_wkb():
    mp = StMultiPointFromWkb(b"\x00\x01")
    assert str(mp) == "ST_MULTIPOINTFROMWKB(%s)"
    assert mp.args == [b"\x00\x01"]

    mp_srid = StMultiPointFromWkb(b"\x00\x01", 4326)
    assert str(mp_srid) == "ST_MULTIPOINTFROMWKB(%s, %s)"
    assert mp_srid.args == [b"\x00\x01", 4326]


def test_st_m_point_from_wkb():
    mp = StMPointFromWkb(b"\x00\x01")
    assert str(mp) == "ST_MPOINTFROMWKB(%s)"
    assert mp.args == [b"\x00\x01"]

    mp_srid = StMPointFromWkb(b"\x00\x01", 4326)
    assert str(mp_srid) == "ST_MPOINTFROMWKB(%s, %s)"
    assert mp_srid.args == [b"\x00\x01", 4326]


def test_multi_point_from_wkb():
    mp = MultiPointFromWkb(b"\x00\x01")
    assert str(mp) == "MULTIPOINTFROMWKB(%s)"
    assert mp.args == [b"\x00\x01"]


def test_m_point_from_wkb():
    mp = MPointFromWkb(b"\x00\x01")
    assert str(mp) == "MPOINTFROMWKB(%s)"
    assert mp.args == [b"\x00\x01"]


# ---------------------------------------------------------------------------
# WKB constructors: ST_MultiLineStringFromWKB and synonyms
# ---------------------------------------------------------------------------


def test_st_multi_line_string_from_wkb():
    mls = StMultiLineStringFromWkb(b"\x00\x01")
    assert str(mls) == "ST_MULTILINESTRINGFROMWKB(%s)"
    assert mls.args == [b"\x00\x01"]

    mls_srid = StMultiLineStringFromWkb(b"\x00\x01", 4326)
    assert str(mls_srid) == "ST_MULTILINESTRINGFROMWKB(%s, %s)"
    assert mls_srid.args == [b"\x00\x01", 4326]


def test_st_m_line_from_wkb():
    mls = StMLineFromWkb(b"\x00\x01")
    assert str(mls) == "ST_MLINEFROMWKB(%s)"
    assert mls.args == [b"\x00\x01"]

    mls_srid = StMLineFromWkb(b"\x00\x01", 4326)
    assert str(mls_srid) == "ST_MLINEFROMWKB(%s, %s)"
    assert mls_srid.args == [b"\x00\x01", 4326]


def test_multi_line_string_from_wkb():
    mls = MultiLineStringFromWkb(b"\x00\x01")
    assert str(mls) == "MULTILINESTRINGFROMWKB(%s)"
    assert mls.args == [b"\x00\x01"]


def test_m_line_from_wkb():
    mls = MLineFromWkb(b"\x00\x01")
    assert str(mls) == "MLINEFROMWKB(%s)"
    assert mls.args == [b"\x00\x01"]


# ---------------------------------------------------------------------------
# WKB constructors: ST_MultiPolygonFromWKB and synonyms
# ---------------------------------------------------------------------------


def test_st_multi_polygon_from_wkb():
    mpoly = StMultiPolygonFromWkb(b"\x00\x01")
    assert str(mpoly) == "ST_MULTIPOLYGONFROMWKB(%s)"
    assert mpoly.args == [b"\x00\x01"]

    mpoly_srid = StMultiPolygonFromWkb(b"\x00\x01", 4326)
    assert str(mpoly_srid) == "ST_MULTIPOLYGONFROMWKB(%s, %s)"
    assert mpoly_srid.args == [b"\x00\x01", 4326]


def test_st_m_poly_from_wkb():
    mpoly = StMPolyFromWkb(b"\x00\x01")
    assert str(mpoly) == "ST_MPOLYFROMWKB(%s)"
    assert mpoly.args == [b"\x00\x01"]

    mpoly_srid = StMPolyFromWkb(b"\x00\x01", 4326)
    assert str(mpoly_srid) == "ST_MPOLYFROMWKB(%s, %s)"
    assert mpoly_srid.args == [b"\x00\x01", 4326]


def test_multi_polygon_from_wkb():
    mpoly = MultiPolygonFromWkb(b"\x00\x01")
    assert str(mpoly) == "MULTIPOLYGONFROMWKB(%s)"
    assert mpoly.args == [b"\x00\x01"]


def test_m_poly_from_wkb():
    mpoly = MPolyFromWkb(b"\x00\x01")
    assert str(mpoly) == "MPOLYFROMWKB(%s)"
    assert mpoly.args == [b"\x00\x01"]


# ---------------------------------------------------------------------------
# WKB constructors: ST_GeomCollFromWKB and synonyms
# ---------------------------------------------------------------------------


def test_st_geom_coll_from_wkb():
    gc = StGeomCollFromWkb(b"\x00\x01")
    assert str(gc) == "ST_GEOMCOLLFROMWKB(%s)"
    assert gc.args == [b"\x00\x01"]

    gc_srid = StGeomCollFromWkb(b"\x00\x01", 4326)
    assert str(gc_srid) == "ST_GEOMCOLLFROMWKB(%s, %s)"
    assert gc_srid.args == [b"\x00\x01", 4326]


def test_st_geometry_collection_from_wkb():
    gc = StGeometryCollectionFromWkb(b"\x00\x01")
    assert str(gc) == "ST_GEOMETRYCOLLECTIONFROMWKB(%s)"
    assert gc.args == [b"\x00\x01"]

    gc_srid = StGeometryCollectionFromWkb(b"\x00\x01", 4326)
    assert str(gc_srid) == "ST_GEOMETRYCOLLECTIONFROMWKB(%s, %s)"
    assert gc_srid.args == [b"\x00\x01", 4326]


def test_geom_coll_from_wkb():
    gc = GeomCollFromWkb(b"\x00\x01")
    assert str(gc) == "GEOMCOLLFROMWKB(%s)"
    assert gc.args == [b"\x00\x01"]


def test_geometry_collection_from_wkb():
    gc = GeometryCollectionFromWkb(b"\x00\x01")
    assert str(gc) == "GEOMETRYCOLLECTIONFROMWKB(%s)"
    assert gc.args == [b"\x00\x01"]


# ---------------------------------------------------------------------------
# GeoJSON / GeoHash constructors
# ---------------------------------------------------------------------------


def test_st_geom_from_geojson():
    g = StGeomFromGeoJson('{"type": "Point", "coordinates": [5.3, 15.0]}')
    assert str(g) == "ST_GEOMFROMGEOJSON(%s)"
    assert g.args == ['{"type": "Point", "coordinates": [5.3, 15.0]}']

    g_opt = StGeomFromGeoJson('{"type": "Point", "coordinates": [5.3, 15.0]}', 2)
    assert str(g_opt) == "ST_GEOMFROMGEOJSON(%s, %s)"
    assert g_opt.args == ['{"type": "Point", "coordinates": [5.3, 15.0]}', 2]

    # srid given without option: option is bound as NULL, not omitted.
    g_srid = StGeomFromGeoJson('{"type": "Point", "coordinates": [5.3, 15.0]}', srid=4326)
    assert str(g_srid) == "ST_GEOMFROMGEOJSON(%s, %s, %s)"
    assert g_srid.args == ['{"type": "Point", "coordinates": [5.3, 15.0]}', None, 4326]

    # srid given together with option.
    g_opt_srid = StGeomFromGeoJson('{"type": "Point", "coordinates": [5.3, 15.0]}', 2, 4326)
    assert str(g_opt_srid) == "ST_GEOMFROMGEOJSON(%s, %s, %s)"
    assert g_opt_srid.args == ['{"type": "Point", "coordinates": [5.3, 15.0]}', 2, 4326]

    g_stmt = StGeomFromGeoJson(Raw("%s", '{"type": "Point", "coordinates": [5.3, 15.0]}'))
    assert str(g_stmt) == "ST_GEOMFROMGEOJSON(%s)"
    assert g_stmt.args == ['{"type": "Point", "coordinates": [5.3, 15.0]}']


def test_st_point_from_geohash():
    p = StPointFromGeoHash("s00twy01mtw037m", 0)
    assert str(p) == "ST_POINTFROMGEOHASH(%s, %s)"
    assert p.args == ["s00twy01mtw037m", 0]

    p_stmt = StPointFromGeoHash(Raw("%s", "s00twy01mtw037m"), 4326)
    assert str(p_stmt) == "ST_POINTFROMGEOHASH(%s, %s)"
    assert p_stmt.args == ["s00twy01mtw037m", 4326]


def test_point_from_geohash():
    p = PointFromGeoHash("s00twy01mtw037m", 4326)
    assert str(p) == "POINTFROMGEOHASH(%s, %s)"
    assert p.args == ["s00twy01mtw037m", 4326]


# ---------------------------------------------------------------------------
# srid=0 must still render (locks in the `is not None` check rather than truthiness).
# ---------------------------------------------------------------------------


def test_st_geom_from_text_srid_zero():
    g = StGeomFromText("POINT(1 1)", 0)
    assert str(g) == "ST_GEOMFROMTEXT(%s, %s)"
    assert g.args == ["POINT(1 1)", 0]


def test_st_geom_from_wkb_srid_zero():
    g = StGeomFromWkb(b"\x00\x01", 0)
    assert str(g) == "ST_GEOMFROMWKB(%s, %s)"
    assert g.args == [b"\x00\x01", 0]


# ---------------------------------------------------------------------------
# Composition with Select / Update
# ---------------------------------------------------------------------------


def test_geometry_functions_compose_in_select():
    sel = Select("id", "name", table="places", where=Eq(Column("location"), StGeomFromText("POINT(1 1)", 4326)))
    assert str(sel) == "SELECT `id`, `name` FROM `places` WHERE `location` = ST_GEOMFROMTEXT(%s, %s)"
    assert sel.args == ["POINT(1 1)", 4326]


def test_geometry_functions_compose_in_update():
    # StGeomFromText takes WKT text, not a geometry value - a Point() result would be invalid on a real server
    # (ERROR 4079). Use a column holding WKT text instead.
    upd = Update("places", set={"location": StGeomFromText(Column("wkt"), 4326)}, where=Eq("id", 1))
    assert str(upd) == "UPDATE `places` SET `location` = ST_GEOMFROMTEXT(`wkt`, %s) WHERE `id` = %s"
    assert upd.args == [4326, 1]


def test_geometry_functions_compose_in_insert():
    ins = Insert.into("places")("location").values((Point(1, 2),))
    assert str(ins) == "INSERT INTO `places` (`location`) VALUES (POINT(%s, %s))"
    assert ins.args == [1, 2]


# ---------------------------------------------------------------------------
# Dialect propagation: constructors must not render SQL (or resolve the placeholder) at construction time, only
# lazily in __str__ / args - otherwise an explicit dialect on the enclosing statement would be ignored.
# ---------------------------------------------------------------------------


def test_geometry_functions_respect_explicit_dialect():
    # A Statement argument (Column) and a value argument (srid), with the optional SRID given.
    g = StGeomFromText(Column("t.wkt"), 4326)
    sel = Select(g, table="t", dialect=SQLiteDialect())
    assert str(sel) == "SELECT ST_GEOMFROMTEXT(`t`.`wkt`, ?) FROM `t`"
    assert sel.args == [4326]

    # A structure constructor with a Statement argument and a value argument.
    p = Point(Column("t.lon"), 1)
    sel2 = Select(p, table="t", dialect=SQLiteDialect())
    assert str(sel2) == "SELECT POINT(`t`.`lon`, ?) FROM `t`"
    assert sel2.args == [1]

    # The very same instances still render with the default (MySQL/MariaDB) dialect when not wrapped in a
    # SQLite-dialect statement - proving no dialect was baked in at construction time.
    assert str(g) == "ST_GEOMFROMTEXT(`t`.`wkt`, %s)"
    assert str(p) == "POINT(`t`.`lon`, %s)"
