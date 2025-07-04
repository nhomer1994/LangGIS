import os
import osmnx as ox

def fetch_and_save_parks(
    place="Edinburgh, Scotland, UK",
    tags={"leisure": "park"},
    out_path="../data/edinburgh_parks_sample.geojson"
):
    """
    Fetch parks as OSM polygons using OSMnx, and save to GeoJSON.
    Creates directory if it doesn't exist.

    Parameters
    ----------
    place : str
        Place name to search for parks (default: Edinburgh, Scotland, UK)
    tags : dict
        Tags to request from OSM (default: {'leisure': 'park'})
    out_path : str
        Destination GeoJSON path (default: '../data/edinburgh_parks_sample.geojson')
    """
    print(f"Fetching parks for {place}")
    parks_gdf = ox.features_from_place(place, tags=tags)
    print(f"Fetched {len(parks_gdf)} parks.")

    # Ensure output directory exists
    directory = os.path.dirname(out_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    parks_gdf.to_file(out_path, driver="GeoJSON")
    print(f"Saved parks GeoJSON to {out_path}")
    return parks_gdf

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fetch and save OSM parks for a place.")
    parser.add_argument("--place", type=str, default="Edinburgh, Scotland, UK")
    parser.add_argument("--out", type=str, default="../data/edinburgh_parks_sample.geojson")
    args = parser.parse_args()
    fetch_and_save_parks(place=args.place, out_path=args.out)

