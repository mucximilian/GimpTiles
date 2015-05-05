﻿SELECT 
	ROW_NUMBER() OVER () AS id,
	get_scaled_svg_polygon(
		ST_Union(way),
		1271912.15067,
		6134530.14206,
		1281696.09029,
		6124746.20243,
		256
	) AS svg
FROM (
	SELECT
		*
	FROM planet_osm_polygon
	WHERE ST_Intersects (
		way, 
		get_tile_bbox(
			1271912.15067,
			6134530.14206,
			1281696.09029,
			6124746.20243,
			256,
			12
		) 
	)
	AND ST_Area(way) > ((((1281696.09029-1271912.15067)/(256/2))*2)^2)
) t
WHERE
	landuse='forest' OR leisure='park'