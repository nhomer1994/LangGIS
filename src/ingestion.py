import osmnx as ox
import os

def fetch_and_save_parks(
    place="Edinburgh, Scotland, UK",
    tags={"leisure": "park"},
    out_path="../data/edinburgh_parks_sample.parquet",
    file_format="parquet"
):
    print(f"Fetching parks for {place}")
    parks_gdf = ox.features_from_place(place, tags=tags)
    print(f"Fetched {len(parks_gdf)} parks.")

    directory = os.path.dirname(out_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    if file_format == "parquet":
        parks_gdf.to_parquet(out_path)
        print(f"Saved parks Parquet to {out_path}")
    elif file_format == "geojson":
        parks_gdf.to_file(out_path, driver="GeoJSON")
        print(f"Saved parks GeoJSON to {out_path}")
    else:
        raise ValueError("Unsupported file format: choose 'parquet' or 'geojson'")
    return parks_gdf

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fetch and save OSM parks for a place.")
    parser.add_argument("--place", type=str, default="Edinburgh, Scotland, UK")
    parser.add_argument("--out", type=str, default="../data/edinburgh_parks_sample.parquet")
    parser.add_argument("--format", type=str, choices=["parquet", "geojson"], default="parquet")
    args = parser.parse_args()
    fetch_and_save_parks(place=args.place, out_path=args.out, file_format=args.format)

