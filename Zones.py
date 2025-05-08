import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# Load Citi Bike station data
stations_df = pd.read_csv("citibike_stations.csv")

# Optional: clean column names of whitespace, if needed
stations_df.columns = stations_df.columns.str.strip()

# Convert to GeoDataFrame using correct latitude and longitude columns
stations_gdf = gpd.GeoDataFrame(
    stations_df,
    geometry=[Point(lon, lat) for lon, lat in zip(stations_df['start_lng'], stations_df['start_lat'])],
    crs="EPSG:4326"  # WGS84: standard lat/lon
)

# Load your polygon zones from GeoJSON
zones_gdf = gpd.read_file("nyc_zones.geojson").to_crs("EPSG:4326")

# Spatial join: assign each station to a zone if it falls within a polygon
stations_with_zones = gpd.sjoin(stations_gdf, zones_gdf, how="left", predicate="within")

# Fill in missing zone names with a default value like "0"
stations_with_zones['zone_name'] = stations_with_zones['zone_name'].fillna("0")

# Optional: drop the spatial join index column
stations_with_zones = stations_with_zones.drop(columns=["index_right"], errors="ignore")

# Save result to CSV — include desired fields and assigned zone
stations_with_zones[['start_station_id', 'start_station_name', 'zone_name']].to_csv(
    "station_zone_mapping.csv", index=False
)
