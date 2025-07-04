from pyspark.sql import SparkSession
from sedona.register.geo_registrator import SedonaRegistrator
from sedona.sql.types import GeometryType

def load_parks_parquet(parquet_path):
    spark = SparkSession.builder \
        .appName("SpatialQueries") \
        .getOrCreate()
    SedonaRegistrator.registerAll(spark)
    # Load parquet to Spark DataFrame
    df = spark.read.parquet(parquet_path)
    # Register as temp table for SQL queries
    df.createOrReplaceTempView("parks")
    return spark, df

def filter_parks_by_area(spark, min_area_ha=5):
    # 1 hectare = 10,000 m²
    query = f"""
        SELECT *, ST_Area(ST_GeomFromWKT(geometry)) as area_m2
        FROM parks
    """
    parks_with_area = spark.sql(query)
    parks_filtered = parks_with_area.filter(parks_with_area.area_m2 >= min_area_ha * 10_000)
    return parks_filtered

def parks_within_radius(spark, center_lat, center_lon, radius_km=2):
    # The parks geometries are assumed to be in WGS84 (degrees)
    # We'll buffer the reference point and filter for intersection.
    buffer_wkt = f"ST_Buffer(ST_Point({center_lon}, {center_lat}), {radius_km/110.574})"
    # (1 degree ≈ 110.574 km latitude; for more accuracy, reproject to meters!)
    query = f"""
        SELECT *
        FROM parks
        WHERE ST_Intersects(ST_GeomFromWKT(geometry), {buffer_wkt})
    """
    return spark.sql(query)
