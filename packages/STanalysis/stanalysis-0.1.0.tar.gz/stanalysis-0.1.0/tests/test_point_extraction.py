import numpy as np
import pandas as pd
import xarray as xr

from STanalysis import extract_point_values


def test_extract_point_values(tmp_path):
    times = pd.date_range("2024-01-01", periods=5)
    lats = [0.0, 1.0]
    lons = [0.0, 1.0]
    data = np.arange(len(times) * len(lats) * len(lons)).reshape(
        len(times), len(lats), len(lons)
    )
    ds = xr.Dataset(
        {"var": (("time", "lat", "lon"), data)},
        coords={"time": times, "lat": lats, "lon": lons},
    )
    nc_path = tmp_path / "data.nc"
    ds.to_netcdf(nc_path)

    df = pd.DataFrame({"lon": [0.1], "lat": [0.9], "date": [times[-1]]})
    points_path = tmp_path / "points.csv"
    df.to_csv(points_path, index=False)

    result = extract_point_values(nc_path, points_path, variable="var", days_back=2, date_col="date")
    assert "value" in result.columns
    assert len(result) == 1
