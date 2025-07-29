import re
import numpy as np
import geopandas as gpd
from netCDF4 import Dataset, date2num, num2date
import time
from datetime import datetime, timedelta
import pandas as pd
import pint
import xarray as xr
import contextlib
import tempfile
from ..configs.config import FS

# please don't remove the following line although it seems not used
import pint_xarray  # noqa

from hydroutils.hydro_time import calculate_utc_offset


def creatspinc(value, data_vars, lats, lons, starttime, filename, resolution):
    gridspi = Dataset(filename, "w", format="NETCDF4")

    # dimensions
    gridspi.createDimension("time", value[0].shape[0])
    gridspi.createDimension("lat", value[0].shape[2])  # len(lat)
    gridspi.createDimension("lon", value[0].shape[1])

    # Create coordinate variables for dimensions
    times = gridspi.createVariable("time", np.float64, ("time",))
    latitudes = gridspi.createVariable("lat", np.float32, ("lat",))
    longitudes = gridspi.createVariable("lon", np.float32, ("lon",))

    # Create the actual variable
    for var, attr in data_vars.items():
        gridspi.createVariable(
            var,
            np.float32,
            (
                "time",
                "lon",
                "lat",
            ),
        )

    # Global Attributes
    gridspi.description = "var"
    gridspi.history = f"Created {time.ctime(time.time())}"
    gridspi.source = "netCDF4 python module tutorial"

    # Variable Attributes
    latitudes.units = "degree_north"
    longitudes.units = "degree_east"
    times.units = "days since 1970-01-01 00:00:00"
    times.calendar = "gregorian"

    # data
    latitudes[:] = lats
    longitudes[:] = lons

    # Fill in times
    dates = []
    if resolution == "daily":
        for n in range(value[0].shape[0]):
            dates.append(starttime + n)
        times[:] = dates[:]

    elif resolution == "6-hourly":
        # for n in range(value[0].shape[0]):
        #     dates.append(starttime + (n+1) * np.timedelta64(6, 'h'))

        for n in range(value[0].shape[0]):
            dates.append(starttime + (n + 1) * timedelta(hours=6))

        times[:] = date2num(dates, units=times.units, calendar=times.calendar)
        # print 'time values (in units %s): ' % times.units +'\n', times[:]
        dates = num2date(times[:], units=times.units, calendar=times.calendar)

    # Fill in values
    i = 0
    for var, attr in data_vars.items():
        gridspi.variables[var].long_name = attr["long_name"]
        gridspi.variables[var].units = attr["units"]
        gridspi.variables[var][:] = value[i][:]
        i = i + 1

    gridspi.close()


def regen_box(bbox, resolution, offset):
    lx = bbox[0]
    rx = bbox[2]
    LLON = np.round(
        int(lx)
        + resolution * int((lx - int(lx)) / resolution + 0.5)
        + offset
        * (int(lx * 10) / 10 + offset - lx)
        / abs(int(lx * 10) // 10 + offset - lx + 0.0000001),
        3,
    )
    RLON = np.round(
        int(rx)
        + resolution * int((rx - int(rx)) / resolution + 0.5)
        - offset
        * (int(rx * 10) / 10 + offset - rx)
        / abs(int(rx * 10) // 10 + offset - rx + 0.0000001),
        3,
    )

    by = bbox[1]
    ty = bbox[3]
    BLAT = np.round(
        int(by)
        + resolution * int((by - int(by)) / resolution + 0.5)
        + offset
        * (int(by * 10) / 10 + offset - by)
        / abs(int(by * 10) // 10 + offset - by + 0.0000001),
        3,
    )
    TLAT = np.round(
        int(ty)
        + resolution * int((ty - int(ty)) / resolution + 0.5)
        - offset
        * (int(ty * 10) / 10 + offset - ty)
        / abs(int(ty * 10) // 10 + offset - ty + 0.0000001),
        3,
    )

    # print(LLON,BLAT,RLON,TLAT)
    return [LLON, BLAT, RLON, TLAT]


def validate(date_text, formatter, error):
    try:
        return datetime.strptime(date_text, formatter)
    except ValueError as e:
        raise ValueError(error) from e


def cf2datetime(ds):
    ds = ds.copy()
    time_tmp1 = ds.indexes["time"]
    attrs = ds.coords["time"].attrs
    time_tmp2 = []
    for i in range(time_tmp1.shape[0]):
        tmp = time_tmp1[i]
        a = str(tmp.year).zfill(4)
        b = str(tmp.month).zfill(2)
        c = str(tmp.day).zfill(2)
        d = str(tmp.hour).zfill(2)
        e = str(tmp.minute).zfill(2)
        f = str(tmp.second).zfill(2)
        time_tmp2.append(np.datetime64(f"{a}-{b}-{c} {d}:{e}:{f}.00000000"))
    ds = ds.assign_coords(time=time_tmp2)
    ds.coords["time"].attrs = attrs

    return ds


def generate_time_intervals(start_date, end_date):
    # Initialize an empty list to store the intervals
    intervals = []

    # Loop over days
    while start_date <= end_date:
        # Loop over the four time intervals in a day
        intervals.extend(
            [start_date.strftime("%Y-%m-%d"), hour] for hour in ["00", "06", "12", "18"]
        )
        # Move to the next day
        start_date += timedelta(days=1)

    return intervals


def _convert_target_unit(target_unit):
    """Convert user-friendly unit to standard unit for internal calculations."""
    if match := re.match(r"mm/(\d+)(h|d)", target_unit):
        num, unit = match.groups()
        return int(num), unit
    return None, None


def streamflow_unit_conv(streamflow, area, target_unit="mm/d", inverse=False):
    """Convert the unit of streamflow data to mm/xx(time) for a basin or inverse.

    Parameters
    ----------
    streamflow: xarray.Dataset, numpy.ndarray, pandas.DataFrame/Series
        Streamflow data of each basin.
    area: xarray.Dataset or pint.Quantity wrapping numpy.ndarray, pandas.DataFrame/Series
        Area of each basin.
    target_unit: str
        The unit to convert to.
    inverse: bool
        If True, convert the unit to m^3/s.
        If False, convert the unit to mm/day or mm/h.

    Returns
    -------
    Converted data in the same type as the input streamflow.
    """
    # Convert the user input unit format
    num, unit = _convert_target_unit(target_unit)
    if unit:
        if unit == "h":
            standard_unit = "mm/h"
            conversion_factor = num
        elif unit == "d":
            standard_unit = "mm/d"
            conversion_factor = num
        else:
            raise ValueError(f"Unsupported unit: {unit}")
    else:
        standard_unit = target_unit
        conversion_factor = 1
    # Regular expression to match units with numbers
    custom_unit_pattern = re.compile(r"mm/(\d+)(h|d)")

    # Function to handle the conversion for numpy and pandas
    def np_pd_conversion(streamflow, area, target_unit, inverse, conversion_factor):
        if not inverse:
            result = (streamflow / area).to(target_unit) * conversion_factor
        else:
            result = (streamflow * area).to(target_unit) / conversion_factor
        return result.magnitude

    # Handle xarray
    if isinstance(streamflow, xr.Dataset) and isinstance(area, xr.Dataset):
        streamflow_units = streamflow[list(streamflow.keys())[0]].attrs.get(
            "units", None
        )
        if not inverse:
            if not (
                custom_unit_pattern.match(target_unit)
                or re.match(r"mm/(?!\d)", target_unit)
            ):
                raise ValueError(
                    "target_unit should be a valid unit like 'mm/d', 'mm/day', 'mm/h', 'mm/hour', 'mm/3h', 'mm/5d'"
                )

            q = streamflow.pint.quantify()
            a = area.pint.quantify()
            r = q[list(q.keys())[0]] / a[list(a.keys())[0]]
            # result = r.pint.to(target_unit).to_dataset(name=list(q.keys())[0])
            result = (r.pint.to(standard_unit) * conversion_factor).to_dataset(
                name=list(q.keys())[0]
            )
            # Manually set the unit attribute to the custom unit
            result_ = result.pint.dequantify()
            result_[list(result_.keys())[0]].attrs["units"] = target_unit
            return result_
        else:
            if streamflow_units:
                if custom_match := custom_unit_pattern.match(streamflow_units):
                    num, unit = custom_match.groups()
                    if unit == "h":
                        standard_unit = "mm/h"
                        conversion_factor = int(num)
                    elif unit == "d":
                        standard_unit = "mm/d"
                        conversion_factor = int(num)
                    # Convert custom unit to standard unit
                    r_ = streamflow / conversion_factor
                    r_[list(r_.keys())[0]].attrs["units"] = standard_unit
                    r = r_.pint.quantify()
                else:
                    r = streamflow.pint.quantify()
            else:
                r = streamflow.pint.quantify()
            if target_unit not in ["m^3/s", "m3/s"]:
                raise ValueError("target_unit should be 'm^3/s'")
            a = area.pint.quantify()
            q = r[list(r.keys())[0]] * a[list(a.keys())[0]]
            result = q.pint.to(target_unit).to_dataset(name=list(r.keys())[0])
            # dequantify to get normal xr_dataset
            return result.pint.dequantify()

    # Handle numpy and pandas
    elif isinstance(streamflow, pint.Quantity) and isinstance(area, pint.Quantity):
        if type(streamflow.magnitude) not in [np.ndarray, pd.DataFrame, pd.Series]:
            raise TypeError(
                "Input streamflow must be xarray.Dataset, or pint.Quantity wrapping numpy.ndarray, or pandas.DataFrame/Series"
            )
        if type(area.magnitude) != type(streamflow.magnitude):
            raise TypeError("streamflow and area must be the same type")
        return np_pd_conversion(
            streamflow, area, standard_unit, inverse, conversion_factor
        )

    else:
        raise TypeError(
            "Input streamflow must be xarray.Dataset, or pint.Quantity wrapping numpy.ndarray, or pandas.DataFrame/Series"
        )


def minio_file_list(minio_folder_url):
    """
    Get all filenames in a specified directory on MinIO.

    Parameters
    ----------
    minio_folder_url : str
        the minio file url, must start with s3://

    Returns
    -------
    folder list
    """
    # Get the list of files in the directory
    try:
        # the minio folder url doesn't have to start with s3://, but we agree that it must
        # start with s3:// to distinguish between local and Minio folder directories.
        files = FS.ls(minio_folder_url)
        return [file.split("/")[-1] for file in files if not file.endswith("/")]
    except Exception as e:
        print(f"Error accessing {minio_folder_url}: {e}")
        return []


def is_minio_folder(minio_url):
    """
    Check if a MinIO folder exists.

    Parameters
    ----------
    minio_url : str
        the minio file url, must start with s3://

    Returns
    -------
    bool
        True if the folder exists, False otherwise

    """
    try:
        if not FS.exists(minio_url):
            raise FileNotFoundError(f"No file or folder found in {minio_url}")
        if minio_url.endswith("/"):
            # If the path ends with '/', treat it as a directory
            return True
        # Try to list objects under this path
        objects = FS.ls(minio_url)
        test_object = "s3://" + objects[0]
        return len(objects) != 1 or test_object != minio_url
    except Exception as e:
        raise NotImplementedError(f"Error accessing {minio_url}: {e}") from e


def calculate_basin_offsets(shp_file_path):
    """
    Calculate the UTC offset for each basin based on the outlet shapefile.

    Parameters:
        shp_file (str): The path to the basin outlet shapefile.

    Returns:
        dict: A dictionary where the keys are the BASIN_ID and the values are the corresponding UTC offsets.
    """
    # read shapefile
    if "s3://" in shp_file_path:
        # related list
        extensions = [".shp", ".shx", ".dbf", ".prj"]

        # create a temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            # download all related files to the temporary directory
            base_name = shp_file_path.rsplit(".", 1)[0]
            extensions = [".shp", ".shx", ".dbf", ".prj"]

            for ext in extensions:
                remote_file = f"{base_name}{ext}"
                local_file = f"{tmpdir}/shp_file{ext}"
                with contextlib.suppress(FileNotFoundError):
                    FS.get(remote_file, local_file)
            gdf = gpd.read_file(f"{tmpdir}/shp_file.shp")

    else:
        # If the file is not on S3 (MinIO), read it directly
        gdf = gpd.read_file(shp_file_path)

    # create an empty dictionary
    basin_offset_dict = {}

    for index, row in gdf.iterrows():
        outlet = row["geometry"]
        # TODO: Only for temp use.
        offset = calculate_utc_offset(
            outlet.y, outlet.x, datetime(2024, 8, 14, 0, 0, 0)
        )
        basin_id = row.get(
            "BASIN_ID", index
        )  # Use the index as the default value if "BASIN_ID" is not found
        basin_offset_dict[basin_id] = offset

    return basin_offset_dict


def cal_area_from_shp(shp):
    gdf_equal_area = shp.to_crs(epsg=6933)
    gdf_equal_area["shp_area"] = gdf_equal_area["geometry"].area / 10**6
    result_df = gdf_equal_area[["BASIN_ID", "shp_area"]]
    result_df.rename(columns={"BASIN_ID": "basin_id"}, inplace=True)
    result_df.sort_values("basin_id", inplace=True)
    return result_df
