import pytest

from sqlfactory import Aliased, Column, Eq, PostgreSQLDialect, Raw, Select, SQLiteDialect, Update
from sqlfactory.func.spatial import (
    Area,
    AsBinary,
    AsText,
    AsWkb,
    AsWkt,
    Boundary,
    Buffer,
    Centroid,
    Contains,
    ConvexHull,
    CoveredBy,
    Crosses,
    Dimension,
    Disjoint,
    EndPoint,
    Envelope,
    Equals,
    ExteriorRing,
    GeoHash,
    GeometryN,
    GeometryType,
    GLength,
    InteriorRingN,
    Intersects,
    IsClosed,
    IsEmpty,
    IsRing,
    IsSimple,
    IsValid,
    LatFromGeoHash,
    LongFromGeoHash,
    MbrContains,
    MbrCoveredBy,
    MbrDisjoint,
    MbrEqual,
    MbrEquals,
    MbrIntersects,
    MbrOverlaps,
    MbrTouches,
    MbrWithin,
    NumGeometries,
    NumInteriorRings,
    NumPoints,
    Overlaps,
    PointN,
    PointOnSurface,
    Simplify,
    Srid,
    StArea,
    StartPoint,
    StAsBinary,
    StAsGeoJson,
    StAsText,
    StAsWkb,
    StAsWkt,
    StBoundary,
    StBuffer,
    StCentroid,
    StCollect,
    StContains,
    StConvexHull,
    StCoveredBy,
    StCrosses,
    StDifference,
    StDimension,
    StDisjoint,
    StDistance,
    StDistanceSphere,
    StEndPoint,
    StEnvelope,
    StEquals,
    StExteriorRing,
    StGeoHash,
    StGeometryN,
    StGeometryType,
    StInteriorRingN,
    StIntersection,
    StIntersects,
    StIsClosed,
    StIsEmpty,
    StIsRing,
    StIsSimple,
    StIsValid,
    StLatFromGeoHash,
    StLength,
    StLongFromGeoHash,
    StNumGeometries,
    StNumInteriorRings,
    StNumPoints,
    StOverlaps,
    StPointN,
    StPointOnSurface,
    StRelate,
    StSimplify,
    StSrid,
    StStartPoint,
    StSymDifference,
    StTouches,
    StUnion,
    StValidate,
    StWithin,
    StX,
    StY,
    Touches,
    Validate,
    Within,
    X,
    Y,
)

# ---------------------------------------------------------------------------
# Relations
# ---------------------------------------------------------------------------


def test_st_contains():
    f = StContains(Column("g1"), Column("g2"))
    assert str(f) == "ST_CONTAINS(`g1`, `g2`)"
    assert f.args == []


def test_contains_alias():
    f = Contains(Column("g1"), Column("g2"))
    assert str(f) == "CONTAINS(`g1`, `g2`)"
    assert f.args == []


def test_st_crosses():
    f = StCrosses(Column("g1"), Column("g2"))
    assert str(f) == "ST_CROSSES(`g1`, `g2`)"
    assert f.args == []


def test_crosses_alias():
    f = Crosses(Column("g1"), Column("g2"))
    assert str(f) == "CROSSES(`g1`, `g2`)"
    assert f.args == []


def test_st_disjoint():
    f = StDisjoint(Column("g1"), Column("g2"))
    assert str(f) == "ST_DISJOINT(`g1`, `g2`)"
    assert f.args == []


def test_disjoint_alias():
    f = Disjoint(Column("g1"), Column("g2"))
    assert str(f) == "DISJOINT(`g1`, `g2`)"
    assert f.args == []


def test_st_equals():
    f = StEquals(Column("g1"), Column("g2"))
    assert str(f) == "ST_EQUALS(`g1`, `g2`)"
    assert f.args == []


def test_equals_alias():
    f = Equals(Column("g1"), Column("g2"))
    assert str(f) == "EQUALS(`g1`, `g2`)"
    assert f.args == []


def test_st_intersects():
    f = StIntersects(Column("g1"), Column("g2"))
    assert str(f) == "ST_INTERSECTS(`g1`, `g2`)"
    assert f.args == []


def test_intersects_alias():
    f = Intersects(Column("g1"), Column("g2"))
    assert str(f) == "INTERSECTS(`g1`, `g2`)"
    assert f.args == []


def test_st_overlaps():
    f = StOverlaps(Column("g1"), Column("g2"))
    assert str(f) == "ST_OVERLAPS(`g1`, `g2`)"
    assert f.args == []


def test_overlaps_alias():
    f = Overlaps(Column("g1"), Column("g2"))
    assert str(f) == "OVERLAPS(`g1`, `g2`)"
    assert f.args == []


def test_st_touches():
    f = StTouches(Column("g1"), Column("g2"))
    assert str(f) == "ST_TOUCHES(`g1`, `g2`)"
    assert f.args == []


def test_touches_alias():
    f = Touches(Column("g1"), Column("g2"))
    assert str(f) == "TOUCHES(`g1`, `g2`)"
    assert f.args == []


def test_st_within():
    f = StWithin(Column("g1"), Column("g2"))
    assert str(f) == "ST_WITHIN(`g1`, `g2`)"
    assert f.args == []


def test_within_alias():
    f = Within(Column("g1"), Column("g2"))
    assert str(f) == "WITHIN(`g1`, `g2`)"
    assert f.args == []


def test_st_relate():
    f = StRelate(Column("g1"), Column("g2"), "T*F**FFF*")
    assert str(f) == "ST_RELATE(`g1`, `g2`, %s)"
    assert f.args == ["T*F**FFF*"]


def test_st_covered_by():
    f = StCoveredBy(Column("g1"), Column("g2"))
    assert str(f) == "ST_COVEREDBY(`g1`, `g2`)"
    assert f.args == []


def test_covered_by_alias():
    f = CoveredBy(Column("g1"), Column("g2"))
    assert str(f) == "COVEREDBY(`g1`, `g2`)"
    assert f.args == []


# ---------------------------------------------------------------------------
# MBR relations
# ---------------------------------------------------------------------------


def test_mbr_contains():
    f = MbrContains(Column("g1"), Column("g2"))
    assert str(f) == "MBRCONTAINS(`g1`, `g2`)"
    assert f.args == []


def test_mbr_covered_by():
    f = MbrCoveredBy(Column("g1"), Column("g2"))
    assert str(f) == "MBRCOVEREDBY(`g1`, `g2`)"
    assert f.args == []


def test_mbr_disjoint():
    f = MbrDisjoint(Column("g1"), Column("g2"))
    assert str(f) == "MBRDISJOINT(`g1`, `g2`)"
    assert f.args == []


def test_mbr_equal():
    f = MbrEqual(Column("g1"), Column("g2"))
    assert str(f) == "MBREQUAL(`g1`, `g2`)"
    assert f.args == []


def test_mbr_equals_alias():
    f = MbrEquals(Column("g1"), Column("g2"))
    assert str(f) == "MBREQUALS(`g1`, `g2`)"
    assert f.args == []


def test_mbr_intersects():
    f = MbrIntersects(Column("g1"), Column("g2"))
    assert str(f) == "MBRINTERSECTS(`g1`, `g2`)"
    assert f.args == []


def test_mbr_overlaps():
    f = MbrOverlaps(Column("g1"), Column("g2"))
    assert str(f) == "MBROVERLAPS(`g1`, `g2`)"
    assert f.args == []


def test_mbr_touches():
    f = MbrTouches(Column("g1"), Column("g2"))
    assert str(f) == "MBRTOUCHES(`g1`, `g2`)"
    assert f.args == []


def test_mbr_within():
    f = MbrWithin(Column("g1"), Column("g2"))
    assert str(f) == "MBRWITHIN(`g1`, `g2`)"
    assert f.args == []


# ---------------------------------------------------------------------------
# Measurement
# ---------------------------------------------------------------------------


def test_st_distance():
    f = StDistance(Column("g1"), Column("g2"))
    assert str(f) == "ST_DISTANCE(`g1`, `g2`)"
    assert f.args == []


def test_st_distance_sphere_without_radius():
    f = StDistanceSphere(Column("g1"), Column("g2"))
    assert str(f) == "ST_DISTANCE_SPHERE(`g1`, `g2`)"
    assert f.args == []


def test_st_distance_sphere_with_radius():
    f = StDistanceSphere(Column("g1"), Column("g2"), 6378000)
    assert str(f) == "ST_DISTANCE_SPHERE(`g1`, `g2`, %s)"
    assert f.args == [6378000]


def test_st_length():
    f = StLength(Column("ls"))
    assert str(f) == "ST_LENGTH(`ls`)"
    assert f.args == []


def test_glength_alias():
    f = GLength(Column("ls"))
    assert str(f) == "GLENGTH(`ls`)"
    assert f.args == []


def test_st_area():
    f = StArea(Column("poly"))
    assert str(f) == "ST_AREA(`poly`)"
    assert f.args == []


def test_area_alias():
    f = Area(Column("poly"))
    assert str(f) == "AREA(`poly`)"
    assert f.args == []


# ---------------------------------------------------------------------------
# Accessors / properties
# ---------------------------------------------------------------------------


def test_st_x_getter():
    f = StX(Column("p"))
    assert str(f) == "ST_X(`p`)"
    assert f.args == []


def test_x_alias_getter():
    f = X(Column("p"))
    assert str(f) == "X(`p`)"
    assert f.args == []


def test_st_y_getter():
    f = StY(Column("p"))
    assert str(f) == "ST_Y(`p`)"
    assert f.args == []


def test_y_alias_getter():
    f = Y(Column("p"))
    assert str(f) == "Y(`p`)"
    assert f.args == []


def test_st_srid_getter():
    f = StSrid(Column("g"))
    assert str(f) == "ST_SRID(`g`)"
    assert f.args == []


def test_srid_alias_getter():
    f = Srid(Column("g"))
    assert str(f) == "SRID(`g`)"
    assert f.args == []


def test_st_dimension():
    f = StDimension(Column("g"))
    assert str(f) == "ST_DIMENSION(`g`)"
    assert f.args == []


def test_dimension_alias():
    f = Dimension(Column("g"))
    assert str(f) == "DIMENSION(`g`)"
    assert f.args == []


def test_st_geometry_type():
    f = StGeometryType(Column("g"))
    assert str(f) == "ST_GEOMETRYTYPE(`g`)"
    assert f.args == []


def test_geometry_type_alias():
    f = GeometryType(Column("g"))
    assert str(f) == "GEOMETRYTYPE(`g`)"
    assert f.args == []


def test_st_is_empty():
    f = StIsEmpty(Column("g"))
    assert str(f) == "ST_ISEMPTY(`g`)"
    assert f.args == []


def test_is_empty_alias():
    f = IsEmpty(Column("g"))
    assert str(f) == "ISEMPTY(`g`)"
    assert f.args == []


def test_st_is_simple():
    f = StIsSimple(Column("g"))
    assert str(f) == "ST_ISSIMPLE(`g`)"
    assert f.args == []


def test_is_simple_alias():
    f = IsSimple(Column("g"))
    assert str(f) == "ISSIMPLE(`g`)"
    assert f.args == []


def test_st_is_closed():
    f = StIsClosed(Column("ls"))
    assert str(f) == "ST_ISCLOSED(`ls`)"
    assert f.args == []


def test_is_closed_alias():
    f = IsClosed(Column("ls"))
    assert str(f) == "ISCLOSED(`ls`)"
    assert f.args == []


def test_st_is_ring():
    f = StIsRing(Column("ls"))
    assert str(f) == "ST_ISRING(`ls`)"
    assert f.args == []


def test_is_ring_alias():
    f = IsRing(Column("ls"))
    assert str(f) == "ISRING(`ls`)"
    assert f.args == []


def test_st_is_valid():
    f = StIsValid(Column("g"))
    assert str(f) == "ST_ISVALID(`g`)"
    assert f.args == []


def test_is_valid_alias():
    f = IsValid(Column("g"))
    assert str(f) == "ISVALID(`g`)"
    assert f.args == []


def test_st_num_points():
    f = StNumPoints(Column("ls"))
    assert str(f) == "ST_NUMPOINTS(`ls`)"
    assert f.args == []


def test_num_points_alias():
    f = NumPoints(Column("ls"))
    assert str(f) == "NUMPOINTS(`ls`)"
    assert f.args == []


def test_st_point_n():
    f = StPointN(Column("ls"), 2)
    assert str(f) == "ST_POINTN(`ls`, %s)"
    assert f.args == [2]


def test_point_n_alias():
    f = PointN(Column("ls"), 2)
    assert str(f) == "POINTN(`ls`, %s)"
    assert f.args == [2]


def test_st_start_point():
    f = StStartPoint(Column("ls"))
    assert str(f) == "ST_STARTPOINT(`ls`)"
    assert f.args == []


def test_start_point_alias():
    f = StartPoint(Column("ls"))
    assert str(f) == "STARTPOINT(`ls`)"
    assert f.args == []


def test_st_end_point():
    f = StEndPoint(Column("ls"))
    assert str(f) == "ST_ENDPOINT(`ls`)"
    assert f.args == []


def test_end_point_alias():
    f = EndPoint(Column("ls"))
    assert str(f) == "ENDPOINT(`ls`)"
    assert f.args == []


def test_st_exterior_ring():
    f = StExteriorRing(Column("poly"))
    assert str(f) == "ST_EXTERIORRING(`poly`)"
    assert f.args == []


def test_exterior_ring_alias():
    f = ExteriorRing(Column("poly"))
    assert str(f) == "EXTERIORRING(`poly`)"
    assert f.args == []


def test_st_interior_ring_n():
    f = StInteriorRingN(Column("poly"), 1)
    assert str(f) == "ST_INTERIORRINGN(`poly`, %s)"
    assert f.args == [1]


def test_interior_ring_n_alias():
    f = InteriorRingN(Column("poly"), 1)
    assert str(f) == "INTERIORRINGN(`poly`, %s)"
    assert f.args == [1]


def test_st_num_interior_rings():
    f = StNumInteriorRings(Column("poly"))
    assert str(f) == "ST_NUMINTERIORRINGS(`poly`)"
    assert f.args == []


def test_num_interior_rings_alias():
    f = NumInteriorRings(Column("poly"))
    assert str(f) == "NUMINTERIORRINGS(`poly`)"
    assert f.args == []


def test_st_num_geometries():
    f = StNumGeometries(Column("gc"))
    assert str(f) == "ST_NUMGEOMETRIES(`gc`)"
    assert f.args == []


def test_num_geometries_alias():
    f = NumGeometries(Column("gc"))
    assert str(f) == "NUMGEOMETRIES(`gc`)"
    assert f.args == []


def test_st_geometry_n():
    f = StGeometryN(Column("gc"), 2)
    assert str(f) == "ST_GEOMETRYN(`gc`, %s)"
    assert f.args == [2]


def test_geometry_n_alias():
    f = GeometryN(Column("gc"), 2)
    assert str(f) == "GEOMETRYN(`gc`, %s)"
    assert f.args == [2]


def test_st_envelope():
    f = StEnvelope(Column("g"))
    assert str(f) == "ST_ENVELOPE(`g`)"
    assert f.args == []


def test_envelope_alias():
    f = Envelope(Column("g"))
    assert str(f) == "ENVELOPE(`g`)"
    assert f.args == []


def test_st_boundary():
    f = StBoundary(Column("g"))
    assert str(f) == "ST_BOUNDARY(`g`)"
    assert f.args == []


def test_boundary_alias():
    f = Boundary(Column("g"))
    assert str(f) == "BOUNDARY(`g`)"
    assert f.args == []


def test_st_centroid():
    f = StCentroid(Column("poly"))
    assert str(f) == "ST_CENTROID(`poly`)"
    assert f.args == []


def test_centroid_alias():
    f = Centroid(Column("poly"))
    assert str(f) == "CENTROID(`poly`)"
    assert f.args == []


def test_st_point_on_surface():
    f = StPointOnSurface(Column("poly"))
    assert str(f) == "ST_POINTONSURFACE(`poly`)"
    assert f.args == []


def test_point_on_surface_alias():
    f = PointOnSurface(Column("poly"))
    assert str(f) == "POINTONSURFACE(`poly`)"
    assert f.args == []


# ---------------------------------------------------------------------------
# Operations
# ---------------------------------------------------------------------------


def test_st_buffer():
    f = StBuffer(Column("g"), 10)
    assert str(f) == "ST_BUFFER(`g`, %s)"
    assert f.args == [10]


def test_buffer_alias():
    f = Buffer(Column("g"), 10)
    assert str(f) == "BUFFER(`g`, %s)"
    assert f.args == [10]


def test_st_convex_hull():
    f = StConvexHull(Column("g"))
    assert str(f) == "ST_CONVEXHULL(`g`)"
    assert f.args == []


def test_convex_hull_alias():
    f = ConvexHull(Column("g"))
    assert str(f) == "CONVEXHULL(`g`)"
    assert f.args == []


def test_st_difference():
    f = StDifference(Column("g1"), Column("g2"))
    assert str(f) == "ST_DIFFERENCE(`g1`, `g2`)"
    assert f.args == []


def test_st_intersection():
    f = StIntersection(Column("g1"), Column("g2"))
    assert str(f) == "ST_INTERSECTION(`g1`, `g2`)"
    assert f.args == []


def test_st_sym_difference():
    f = StSymDifference(Column("g1"), Column("g2"))
    assert str(f) == "ST_SYMDIFFERENCE(`g1`, `g2`)"
    assert f.args == []


def test_st_union():
    f = StUnion(Column("g1"), Column("g2"))
    assert str(f) == "ST_UNION(`g1`, `g2`)"
    assert f.args == []


def test_st_simplify():
    f = StSimplify(Column("g"), 0.5)
    assert str(f) == "ST_SIMPLIFY(`g`, %s)"
    assert f.args == [0.5]


def test_simplify_alias():
    f = Simplify(Column("g"), 0.5)
    assert str(f) == "SIMPLIFY(`g`, %s)"
    assert f.args == [0.5]


def test_st_validate():
    f = StValidate(Column("g"))
    assert str(f) == "ST_VALIDATE(`g`)"
    assert f.args == []


def test_validate_alias():
    f = Validate(Column("g"))
    assert str(f) == "VALIDATE(`g`)"
    assert f.args == []


def test_st_collect_with_column():
    f = StCollect(Column("geom"))
    assert str(f) == "ST_COLLECT(`geom`)"
    assert f.args == []


def test_st_collect_wraps_plain_string_as_column():
    f = StCollect("geom")
    assert str(f) == "ST_COLLECT(`geom`)"
    assert f.args == []


def test_st_collect_as_window_function():
    f = StCollect(Column("geom")).over(partition_by=["category"])
    assert str(f) == "ST_COLLECT(`geom`) OVER (PARTITION BY `category`)"
    assert f.args == []


def test_st_collect_distinct():
    f = StCollect(Column("geom"), distinct=True)
    assert str(f) == "ST_COLLECT(DISTINCT `geom`)"
    assert f.args == []


def test_st_collect_distinct_as_window_function():
    f = StCollect(Column("geom"), distinct=True).over(partition_by=["category"])
    assert str(f) == "ST_COLLECT(DISTINCT `geom`) OVER (PARTITION BY `category`)"
    assert f.args == []


def test_st_collect_distinct_under_sqlite_dialect():
    f = StCollect(Column("geom"), distinct=True)

    with SQLiteDialect():
        assert str(f) == "ST_COLLECT(DISTINCT `geom`)"
        assert f.args == []


def test_st_collect_distinct_under_postgresql_dialect():
    f = StCollect(Column("geom"), distinct=True)

    with PostgreSQLDialect():
        assert str(f) == 'ST_COLLECT(DISTINCT "geom")'
        assert f.args == []


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def test_st_as_text():
    f = StAsText(Column("g"))
    assert str(f) == "ST_ASTEXT(`g`)"
    assert f.args == []


def test_as_text_alias():
    f = AsText(Column("g"))
    assert str(f) == "ASTEXT(`g`)"
    assert f.args == []


def test_st_as_wkt_alias():
    f = StAsWkt(Column("g"))
    assert str(f) == "ST_ASWKT(`g`)"
    assert f.args == []


def test_as_wkt_alias():
    f = AsWkt(Column("g"))
    assert str(f) == "ASWKT(`g`)"
    assert f.args == []


def test_st_as_binary():
    f = StAsBinary(Column("g"))
    assert str(f) == "ST_ASBINARY(`g`)"
    assert f.args == []


def test_as_binary_alias():
    f = AsBinary(Column("g"))
    assert str(f) == "ASBINARY(`g`)"
    assert f.args == []


def test_st_as_wkb_alias():
    f = StAsWkb(Column("g"))
    assert str(f) == "ST_ASWKB(`g`)"
    assert f.args == []


def test_as_wkb_alias():
    f = AsWkb(Column("g"))
    assert str(f) == "ASWKB(`g`)"
    assert f.args == []


def test_st_as_geo_json_without_optional_args():
    f = StAsGeoJson(Column("g"))
    assert str(f) == "ST_ASGEOJSON(`g`)"
    assert f.args == []


def test_st_as_geo_json_with_max_decimals():
    f = StAsGeoJson(Column("g"), 6)
    assert str(f) == "ST_ASGEOJSON(`g`, %s)"
    assert f.args == [6]


def test_st_as_geo_json_with_max_decimals_and_options():
    f = StAsGeoJson(Column("g"), 6, 1)
    assert str(f) == "ST_ASGEOJSON(`g`, %s, %s)"
    assert f.args == [6, 1]


def test_st_as_geo_json_options_without_max_decimals_raises():
    with pytest.raises(ValueError, match="max_decimals"):
        StAsGeoJson(Column("g"), None, 1)


def test_st_geo_hash_point_form():
    f = StGeoHash(Column("p"), 10)
    assert str(f) == "ST_GEOHASH(`p`, %s)"
    assert f.args == [10]


def test_st_geo_hash_lon_lat_form():
    f = StGeoHash(-73.9, 40.7, 10)
    assert str(f) == "ST_GEOHASH(%s, %s, %s)"
    assert f.args == [-73.9, 40.7, 10]


def test_st_geo_hash_lon_lat_form_with_null_max_length():
    f = StGeoHash(-73.9, 40.7, None)
    assert str(f) == "ST_GEOHASH(%s, %s, %s)"
    assert f.args == [-73.9, 40.7, None]


def test_st_geo_hash_wrong_argument_count_raises():
    with pytest.raises(TypeError, match="StGeoHash"):
        StGeoHash(Column("p"))

    with pytest.raises(TypeError, match="StGeoHash"):
        StGeoHash(-73.9, 40.7, 10, "extra")


def test_geo_hash_alias_point_form():
    f = GeoHash(Column("p"), 10)
    assert str(f) == "GEOHASH(`p`, %s)"
    assert f.args == [10]


def test_geo_hash_alias_lon_lat_form():
    f = GeoHash(-73.9, 40.7, 10)
    assert str(f) == "GEOHASH(%s, %s, %s)"
    assert f.args == [-73.9, 40.7, 10]


def test_st_lat_from_geo_hash():
    f = StLatFromGeoHash("u4pruydqqvj")
    assert str(f) == "ST_LATFROMGEOHASH(%s)"
    assert f.args == ["u4pruydqqvj"]


def test_lat_from_geo_hash_alias():
    f = LatFromGeoHash("u4pruydqqvj")
    assert str(f) == "LATFROMGEOHASH(%s)"
    assert f.args == ["u4pruydqqvj"]


def test_st_long_from_geo_hash():
    f = StLongFromGeoHash("u4pruydqqvj")
    assert str(f) == "ST_LONGFROMGEOHASH(%s)"
    assert f.args == ["u4pruydqqvj"]


def test_long_from_geo_hash_alias():
    f = LongFromGeoHash("u4pruydqqvj")
    assert str(f) == "LONGFROMGEOHASH(%s)"
    assert f.args == ["u4pruydqqvj"]


# ---------------------------------------------------------------------------
# Integration with Select / Update
# ---------------------------------------------------------------------------


def test_spatial_functions_in_select():
    q = Select(
        "id",
        Aliased(StDistanceSphere(Column("origin"), Column("destination")), alias="distance_m"),
        table="stores",
        where=Eq(StContains(Column("region"), Column("location")), 1),
    )
    assert str(q) == (
        "SELECT `id`, ST_DISTANCE_SPHERE(`origin`, `destination`) AS `distance_m` "
        "FROM `stores` WHERE ST_CONTAINS(`region`, `location`) = %s"
    )
    assert q.args == [1]


def test_spatial_functions_in_update():
    q = (
        Update("stores", where=Eq(StContains(Column("region"), Raw("POINT(1, 1)")), 1))
        .set("location", StBuffer(Column("location"), 5))
        .set("distance_m", StDistanceSphere(Column("origin"), Column("location")))
    )
    assert str(q) == (
        "UPDATE `stores` SET `location` = ST_BUFFER(`location`, %s), "
        "`distance_m` = ST_DISTANCE_SPHERE(`origin`, `location`) "
        "WHERE ST_CONTAINS(`region`, POINT(1, 1)) = %s"
    )
    assert q.args == [5, 1]
