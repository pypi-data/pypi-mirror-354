from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
import xarray as xr
import geopandas as gpd


def _load_points(path: str | Path, date_col: Optional[str] = None) -> pd.DataFrame:
    """Load point coordinates from various file formats."""
    file_path = Path(path)
    ext = file_path.suffix.lower()
    if ext in {".shp", ".geojson", ".json"}:
        if gpd is None:
            raise ImportError("geopandas is required to read shapefiles or GeoJSON")
        gdf = gpd.read_file(file_path)
        df = pd.DataFrame({"lon": gdf.geometry.x, "lat": gdf.geometry.y})
        for col in gdf.columns:
            if col != "geometry":
                df[col] = gdf[col]
    elif ext == ".csv":
        df = pd.read_csv(file_path)
        if "lon" not in df.columns:
            if "longitude" in df.columns:
                df["lon"] = df["longitude"]
            else:
                raise ValueError("CSV must contain 'lon' or 'longitude' column")
        if "lat" not in df.columns:
            if "latitude" in df.columns:
                df["lat"] = df["latitude"]
            else:
                raise ValueError("CSV must contain 'lat' or 'latitude' column")
    else:
        raise ValueError(f"Unsupported point file format: {ext}")

    if date_col and date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col])
    return df


def extract_point_values(
    netcdf_path: str | Path,
    points_path: str | Path,
    variable: str,
    *,
    days_back: int = 7,
    date_col: Optional[str] = None,
    output_path: Optional[str | Path] = None,
) -> pd.DataFrame:
    """Extract averaged values at point locations from a netCDF dataset.

    Parameters
    ----------
    netcdf_path:
        Path to the input netCDF file.
    points_path:
        Path to point data (CSV, shapefile or GeoJSON).
    variable:
        Name of the variable in the netCDF dataset to extract.
    days_back:
        Number of days to average backwards from the provided date.
    date_col:
        Optional column in the point file containing the date.
    output_path:
        Optional path to write results. If suffix is ``.json`` a JSON file is
        written, otherwise a CSV file is created.
    """
    ds = xr.open_dataset(netcdf_path)
    if variable not in ds:
        raise ValueError(f"Variable '{variable}' not found in dataset")

    points_df = _load_points(points_path, date_col)
    results = []
    for _, row in points_df.iterrows():
        lon = float(row["lon"])
        lat = float(row["lat"])
        data = ds[variable]
        if date_col and pd.notna(row.get(date_col)):
            end_date = pd.to_datetime(row[date_col])
            start_date = end_date - pd.Timedelta(days=days_back)
            data = data.sel(time=slice(start_date, end_date))
        value = (
            data.sel(lon=lon, lat=lat, method="nearest")
            .mean()
            .item()
        )
        out_row = row.drop("geometry", errors="ignore").to_dict()
        out_row["value"] = value
        results.append(out_row)

    out_df = pd.DataFrame(results)
    if output_path:
        out_file = Path(output_path)
        if out_file.suffix.lower() == ".json":
            out_df.to_json(out_file, orient="records", lines=True)
        else:
            out_df.to_csv(out_file, index=False)
    return out_df
