### 14.16.1 Spatial Function Reference

The following table lists each spatial function and provides a
short description of each one.

**Table 14.21 Spatial Functions**

| Name | Description | Introduced |
| --- | --- | --- |
| [`GeomCollection()`](gis-mysql-specific-functions.md#function_geomcollection) | Construct geometry collection from geometries |  |
| [`GeometryCollection()`](gis-mysql-specific-functions.md#function_geometrycollection) | Construct geometry collection from geometries |  |
| [`LineString()`](gis-mysql-specific-functions.md#function_linestring) | Construct LineString from Point values |  |
| [`MBRContains()`](spatial-relation-functions-mbr.md#function_mbrcontains) | Whether MBR of one geometry contains MBR of another |  |
| [`MBRCoveredBy()`](spatial-relation-functions-mbr.md#function_mbrcoveredby) | Whether one MBR is covered by another |  |
| [`MBRCovers()`](spatial-relation-functions-mbr.md#function_mbrcovers) | Whether one MBR covers another |  |
| [`MBRDisjoint()`](spatial-relation-functions-mbr.md#function_mbrdisjoint) | Whether MBRs of two geometries are disjoint |  |
| [`MBREquals()`](spatial-relation-functions-mbr.md#function_mbrequals) | Whether MBRs of two geometries are equal |  |
| [`MBRIntersects()`](spatial-relation-functions-mbr.md#function_mbrintersects) | Whether MBRs of two geometries intersect |  |
| [`MBROverlaps()`](spatial-relation-functions-mbr.md#function_mbroverlaps) | Whether MBRs of two geometries overlap |  |
| [`MBRTouches()`](spatial-relation-functions-mbr.md#function_mbrtouches) | Whether MBRs of two geometries touch |  |
| [`MBRWithin()`](spatial-relation-functions-mbr.md#function_mbrwithin) | Whether MBR of one geometry is within MBR of another |  |
| [`MultiLineString()`](gis-mysql-specific-functions.md#function_multilinestring) | Contruct MultiLineString from LineString values |  |
| [`MultiPoint()`](gis-mysql-specific-functions.md#function_multipoint) | Construct MultiPoint from Point values |  |
| [`MultiPolygon()`](gis-mysql-specific-functions.md#function_multipolygon) | Construct MultiPolygon from Polygon values |  |
| [`Point()`](gis-mysql-specific-functions.md#function_point) | Construct Point from coordinates |  |
| [`Polygon()`](gis-mysql-specific-functions.md#function_polygon) | Construct Polygon from LineString arguments |  |
| [`ST_Area()`](gis-polygon-property-functions.md#function_st-area) | Return Polygon or MultiPolygon area |  |
| [`ST_AsBinary()`, `ST_AsWKB()`](gis-format-conversion-functions.md#function_st-asbinary) | Convert from internal geometry format to WKB |  |
| [`ST_AsGeoJSON()`](spatial-geojson-functions.md#function_st-asgeojson) | Generate GeoJSON object from geometry |  |
| [`ST_AsText()`, `ST_AsWKT()`](gis-format-conversion-functions.md#function_st-astext) | Convert from internal geometry format to WKT |  |
| [`ST_Buffer()`](spatial-operator-functions.md#function_st-buffer) | Return geometry of points within given distance from geometry |  |
| [`ST_Buffer_Strategy()`](spatial-operator-functions.md#function_st-buffer-strategy) | Produce strategy option for ST\_Buffer() |  |
| [`ST_Centroid()`](gis-polygon-property-functions.md#function_st-centroid) | Return centroid as a point |  |
| [`ST_Collect()`](spatial-aggregate-functions.md#function_st-collect) | Aggregate spatial values into collection | 8.0.24 |
| [`ST_Contains()`](spatial-relation-functions-object-shapes.md#function_st-contains) | Whether one geometry contains another |  |
| [`ST_ConvexHull()`](spatial-operator-functions.md#function_st-convexhull) | Return convex hull of geometry |  |
| [`ST_Crosses()`](spatial-relation-functions-object-shapes.md#function_st-crosses) | Whether one geometry crosses another |  |
| [`ST_Difference()`](spatial-operator-functions.md#function_st-difference) | Return point set difference of two geometries |  |
| [`ST_Dimension()`](gis-general-property-functions.md#function_st-dimension) | Dimension of geometry |  |
| [`ST_Disjoint()`](spatial-relation-functions-object-shapes.md#function_st-disjoint) | Whether one geometry is disjoint from another |  |
| [`ST_Distance()`](spatial-relation-functions-object-shapes.md#function_st-distance) | The distance of one geometry from another |  |
| [`ST_Distance_Sphere()`](spatial-convenience-functions.md#function_st-distance-sphere) | Minimum distance on earth between two geometries |  |
| [`ST_EndPoint()`](gis-linestring-property-functions.md#function_st-endpoint) | End Point of LineString |  |
| [`ST_Envelope()`](gis-general-property-functions.md#function_st-envelope) | Return MBR of geometry |  |
| [`ST_Equals()`](spatial-relation-functions-object-shapes.md#function_st-equals) | Whether one geometry is equal to another |  |
| [`ST_ExteriorRing()`](gis-polygon-property-functions.md#function_st-exteriorring) | Return exterior ring of Polygon |  |
| [`ST_FrechetDistance()`](spatial-relation-functions-object-shapes.md#function_st-frechetdistance) | The discrete Fréchet distance of one geometry from another | 8.0.23 |
| [`ST_GeoHash()`](spatial-geohash-functions.md#function_st-geohash) | Produce a geohash value |  |
| [`ST_GeomCollFromText()`, `ST_GeometryCollectionFromText()`, `ST_GeomCollFromTxt()`](gis-wkt-functions.md#function_st-geomcollfromtext) | Return geometry collection from WKT |  |
| [`ST_GeomCollFromWKB()`, `ST_GeometryCollectionFromWKB()`](gis-wkb-functions.md#function_st-geomcollfromwkb) | Return geometry collection from WKB |  |
| [`ST_GeometryN()`](gis-geometrycollection-property-functions.md#function_st-geometryn) | Return N-th geometry from geometry collection |  |
| [`ST_GeometryType()`](gis-general-property-functions.md#function_st-geometrytype) | Return name of geometry type |  |
| [`ST_GeomFromGeoJSON()`](spatial-geojson-functions.md#function_st-geomfromgeojson) | Generate geometry from GeoJSON object |  |
| [`ST_GeomFromText()`, `ST_GeometryFromText()`](gis-wkt-functions.md#function_st-geomfromtext) | Return geometry from WKT |  |
| [`ST_GeomFromWKB()`, `ST_GeometryFromWKB()`](gis-wkb-functions.md#function_st-geomfromwkb) | Return geometry from WKB |  |
| [`ST_HausdorffDistance()`](spatial-relation-functions-object-shapes.md#function_st-hausdorffdistance) | The discrete Hausdorff distance of one geometry from another | 8.0.23 |
| [`ST_InteriorRingN()`](gis-polygon-property-functions.md#function_st-interiorringn) | Return N-th interior ring of Polygon |  |
| [`ST_Intersection()`](spatial-operator-functions.md#function_st-intersection) | Return point set intersection of two geometries |  |
| [`ST_Intersects()`](spatial-relation-functions-object-shapes.md#function_st-intersects) | Whether one geometry intersects another |  |
| [`ST_IsClosed()`](gis-linestring-property-functions.md#function_st-isclosed) | Whether a geometry is closed and simple |  |
| [`ST_IsEmpty()`](gis-general-property-functions.md#function_st-isempty) | Whether a geometry is empty |  |
| [`ST_IsSimple()`](gis-general-property-functions.md#function_st-issimple) | Whether a geometry is simple |  |
| [`ST_IsValid()`](spatial-convenience-functions.md#function_st-isvalid) | Whether a geometry is valid |  |
| [`ST_LatFromGeoHash()`](spatial-geohash-functions.md#function_st-latfromgeohash) | Return latitude from geohash value |  |
| [`ST_Latitude()`](gis-point-property-functions.md#function_st-latitude) | Return latitude of Point | 8.0.12 |
| [`ST_Length()`](gis-linestring-property-functions.md#function_st-length) | Return length of LineString |  |
| [`ST_LineFromText()`, `ST_LineStringFromText()`](gis-wkt-functions.md#function_st-linefromtext) | Construct LineString from WKT |  |
| [`ST_LineFromWKB()`, `ST_LineStringFromWKB()`](gis-wkb-functions.md#function_st-linefromwkb) | Construct LineString from WKB |  |
| [`ST_LineInterpolatePoint()`](spatial-operator-functions.md#function_st-lineinterpolatepoint) | The point a given percentage along a LineString | 8.0.24 |
| [`ST_LineInterpolatePoints()`](spatial-operator-functions.md#function_st-lineinterpolatepoints) | The points a given percentage along a LineString | 8.0.24 |
| [`ST_LongFromGeoHash()`](spatial-geohash-functions.md#function_st-longfromgeohash) | Return longitude from geohash value |  |
| [`ST_Longitude()`](gis-point-property-functions.md#function_st-longitude) | Return longitude of Point | 8.0.12 |
| [`ST_MakeEnvelope()`](spatial-convenience-functions.md#function_st-makeenvelope) | Rectangle around two points |  |
| [`ST_MLineFromText()`, `ST_MultiLineStringFromText()`](gis-wkt-functions.md#function_st-mlinefromtext) | Construct MultiLineString from WKT |  |
| [`ST_MLineFromWKB()`, `ST_MultiLineStringFromWKB()`](gis-wkb-functions.md#function_st-mlinefromwkb) | Construct MultiLineString from WKB |  |
| [`ST_MPointFromText()`, `ST_MultiPointFromText()`](gis-wkt-functions.md#function_st-mpointfromtext) | Construct MultiPoint from WKT |  |
| [`ST_MPointFromWKB()`, `ST_MultiPointFromWKB()`](gis-wkb-functions.md#function_st-mpointfromwkb) | Construct MultiPoint from WKB |  |
| [`ST_MPolyFromText()`, `ST_MultiPolygonFromText()`](gis-wkt-functions.md#function_st-mpolyfromtext) | Construct MultiPolygon from WKT |  |
| [`ST_MPolyFromWKB()`, `ST_MultiPolygonFromWKB()`](gis-wkb-functions.md#function_st-mpolyfromwkb) | Construct MultiPolygon from WKB |  |
| [`ST_NumGeometries()`](gis-geometrycollection-property-functions.md#function_st-numgeometries) | Return number of geometries in geometry collection |  |
| [`ST_NumInteriorRing()`, `ST_NumInteriorRings()`](gis-polygon-property-functions.md#function_st-numinteriorrings) | Return number of interior rings in Polygon |  |
| [`ST_NumPoints()`](gis-linestring-property-functions.md#function_st-numpoints) | Return number of points in LineString |  |
| [`ST_Overlaps()`](spatial-relation-functions-object-shapes.md#function_st-overlaps) | Whether one geometry overlaps another |  |
| [`ST_PointAtDistance()`](spatial-operator-functions.md#function_st-pointatdistance) | The point a given distance along a LineString | 8.0.24 |
| [`ST_PointFromGeoHash()`](spatial-geohash-functions.md#function_st-pointfromgeohash) | Convert geohash value to POINT value |  |
| [`ST_PointFromText()`](gis-wkt-functions.md#function_st-pointfromtext) | Construct Point from WKT |  |
| [`ST_PointFromWKB()`](gis-wkb-functions.md#function_st-pointfromwkb) | Construct Point from WKB |  |
| [`ST_PointN()`](gis-linestring-property-functions.md#function_st-pointn) | Return N-th point from LineString |  |
| [`ST_PolyFromText()`, `ST_PolygonFromText()`](gis-wkt-functions.md#function_st-polyfromtext) | Construct Polygon from WKT |  |
| [`ST_PolyFromWKB()`, `ST_PolygonFromWKB()`](gis-wkb-functions.md#function_st-polyfromwkb) | Construct Polygon from WKB |  |
| [`ST_Simplify()`](spatial-convenience-functions.md#function_st-simplify) | Return simplified geometry |  |
| [`ST_SRID()`](gis-general-property-functions.md#function_st-srid) | Return spatial reference system ID for geometry |  |
| [`ST_StartPoint()`](gis-linestring-property-functions.md#function_st-startpoint) | Start Point of LineString |  |
| [`ST_SwapXY()`](gis-format-conversion-functions.md#function_st-swapxy) | Return argument with X/Y coordinates swapped |  |
| [`ST_SymDifference()`](spatial-operator-functions.md#function_st-symdifference) | Return point set symmetric difference of two geometries |  |
| [`ST_Touches()`](spatial-relation-functions-object-shapes.md#function_st-touches) | Whether one geometry touches another |  |
| [`ST_Transform()`](spatial-operator-functions.md#function_st-transform) | Transform coordinates of geometry | 8.0.13 |
| [`ST_Union()`](spatial-operator-functions.md#function_st-union) | Return point set union of two geometries |  |
| [`ST_Validate()`](spatial-convenience-functions.md#function_st-validate) | Return validated geometry |  |
| [`ST_Within()`](spatial-relation-functions-object-shapes.md#function_st-within) | Whether one geometry is within another |  |
| [`ST_X()`](gis-point-property-functions.md#function_st-x) | Return X coordinate of Point |  |
| [`ST_Y()`](gis-point-property-functions.md#function_st-y) | Return Y coordinate of Point |  |
