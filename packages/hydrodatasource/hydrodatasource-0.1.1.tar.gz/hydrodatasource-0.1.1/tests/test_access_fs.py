import geopandas as gpd
import pandas as pd
import numpy as np
import xarray as xr
import hydrodatasource.configs.config as conf
from hydrodatasource.reader import access_fs


def test_read_spec():
    # access_fs.spec_path("st_rain_c.csv")
    mean_forcing_nc = access_fs.spec_path(
        "basins-origin/hour_data/1h/mean_data/mean_data_forcing/mean_forcing_CHN_21401550.nc",
        head="minio",
    )
    print(mean_forcing_nc)


def test_read_shp():
    watershed = gpd.read_file(
        conf.FS.open(
            "s3://basins-origin/basin_shapefiles/basin_USA_camels_01411300.zip"
        )
    )
    print(watershed)

    all_watershed = gpd.read_file(conf.FS.open("s3://basins-origin/basins_shp.zip"))
    print(all_watershed)


def test_read_BA():
    basin = HydroBasins(data_path="./")  # 该路径只是为了实例化该类，测试时可随意指定
    attr = basin.read_BA_xrdataset(
        gage_id_lst=["21401550"], var_lst=["all"], path="basins-origin/attributes.nc"
    )
    print(attr.compute())

    all_attr = access_fs.spec_path(
        "basins-origin/attributes.nc",
        head="minio",
    )
    print(all_attr.compute())


def test_read_zz_stations_ts():
    # 读取csv文件
    zz_stations = access_fs.spec_path(
        "stations-origin/zz_stations/hour_data/1h/zz_CHN_songliao_10800100.csv",
        head="minio",
    )
    print(zz_stations)


def test_read_stations_shp():
    zz_stations_gdf = _extracted_from_test_read_stations_shp_3(
        "s3://stations-origin/stations_list/zz_stations.zip",
        "zz_stations 站点列表如下:",
    )
    pp_stations_gdf = _extracted_from_test_read_stations_shp_3(
        "s3://stations-origin/stations_list/pp_stations.zip",
        "pp_stations 站点列表如下:",
    )
    zq_stations_gdf = _extracted_from_test_read_stations_shp_3(
        "s3://stations-origin/stations_list/zq_stations.zip",
        "zq_stations 站点列表如下:",
    )
    return zz_stations_gdf, pp_stations_gdf, zq_stations_gdf


# TODO Rename this here and in `test_read_stations_shp`
def _extracted_from_test_read_stations_shp_3(arg0, arg1):
    # 读取zip中的shpfiles文件
    result = gpd.read_file(conf.FS.open(arg0))
    print(arg1)
    print(result)
    return result


def test_read_stations_list():
    zz_stations_df = _extracted_from_test_read_stations_list_3(
        "s3://stations-origin/stations_list/zz_stations.csv",
        "zz_stations 站点列表如下:",
    )
    pp_stations_df = _extracted_from_test_read_stations_list_3(
        "s3://stations-origin/stations_list/pp_stations.csv",
        "pp_stations 站点列表如下:",
    )
    zq_stations_df = _extracted_from_test_read_stations_list_3(
        "s3://stations-origin/stations_list/zq_stations.csv",
        "zq_stations 站点列表如下:",
    )
    return zz_stations_df, pp_stations_df, zq_stations_df


# TODO Rename this here and in `test_read_stations_list`
def _extracted_from_test_read_stations_list_3(arg0, arg1):
    # 读取csv文件
    result = pd.read_csv(arg0, storage_options=conf.MINIO_PARAM, index_col=False)
    print(arg1)
    print(result)
    return result


def test_read_zqstations_ts():
    return pd.read_csv(
        "s3://stations-origin/zq_stations/zq_CHN_songliao_10310500.csv",
        storage_options=conf.MINIO_PARAM,
    )


def test_read_reservoirs_info():
    dams_gdf = gpd.read_file(conf.FS.open("s3://reservoirs-origin/dams.zip"))
    rsvrs_gdf = gpd.read_file(conf.FS.open("s3://reservoirs-origin/rsvrs_shp.zip"))
    return dams_gdf, rsvrs_gdf


def test_read_river_network():
    return gpd.read_file(conf.FS.open("s3://basins-origin/HydroRIVERS_v10_shp.zip"))


def test_read_rsvr_ts():
    return pd.read_csv(
        "s3://reservoirs-origin/rr_stations/zq_CHN_songliao_10310500.csv",
        storage_options=conf.MINIO_PARAM,
    )


def test_read_pp():
    return pd.read_csv(
        "s3://stations-origin/pp_stations/hour_data/1h/pp_CHN_songliao_10951870.csv",
        storage_options=conf.MINIO_PARAM,
    )


def test_read_zz():
    return pd.read_csv(
        "s3://stations-origin/zz_stations/hour_data/1h/zz_CHN_dalianxiaoku_21302120.csv",
        storage_options=conf.MINIO_PARAM,
    )


def test_read_zq():
    return pd.read_csv(
        "s3://stations-origin/zq_stations/hour_data/1h/zq_USA_usgs_01181000.csv",
        storage_options=conf.MINIO_PARAM,
    )


def test_df2ds():
    zq_df = pd.read_csv(
        "s3://stations-origin/zq_stations/hour_data/1h/zq_USA_usgs_01181000.csv",
        storage_options=conf.MINIO_PARAM,
    )
    return xr.Dataset().from_dataframe(zq_df)


def list_csv_files(bucket_name, prefix=""):
    """List paths of all CSV files in the specified S3 bucket."""
    path = f"{bucket_name}/{prefix}" if prefix else bucket_name
    return conf.FS.glob(f"{path}*.csv")


def process_store_csvs(source_bucket, destination_bucket, prefix=""):
    """
    Read CSV files from the source bucket, process them, and store the results in the destination bucket.
    """
    csv_files = list_csv_files(source_bucket, prefix)

    for file_path in csv_files:
        df = read_csv_to_dataframe(file_path)
        df = process_dataframe(df)
        store_dataframe_to_bucket(df, destination_bucket, file_path)


def read_csv_to_df(file_path):
    """Read CSV file from file_path and return as pandas DataFrame."""
    with conf.FS.open(file_path, mode="rb") as csv_file:
        df = pd.read_csv(csv_file, index_col=None)
    return df


def store_dataframe_to_bucket(df, bucket, file_path):
    file_name = file_path.split("/")[-1]
    destination_file_path = f"{bucket}/{file_name}"
    with conf.FS.open(destination_file_path, mode="w") as file:
        df.to_csv(file, index=False)


def test_read_folder():
    source_bucket = "s3://stations-origin/pp_stations/hour_data/1h"
    destination_bucket = "s3://stations-interim/pp_stations/hour_data/1h"
    process_store_csvs(source_bucket, destination_bucket)


def test_read_era5_land_csv():
    era5_land_zarr_files = [
        file
        for file in conf.FS.glob("s3://grids-origin/era5_land/")
        if file.endswith(".zarr")
    ]
    bbox_list = []
    start_time = []
    end_list = []
    res_lon_list = []
    res_lat_list = []
    for i in range(len(era5_land_zarr_files)):
        test_ds_i = xr.open_dataset(conf.FS.open(era5_land_zarr_files[i]))
        bbox = [
            np.min(test_ds_i["longitude"].to_numpy()),
            np.max(test_ds_i["longitude"].to_numpy()),
            np.max(test_ds_i["latitude"].to_numpy()),
            np.min(test_ds_i["latitude"].to_numpy()),
        ]
        bbox_list.append(bbox)
        start_time.append(test_ds_i["time"].to_numpy()[0])
        end_list.append(test_ds_i["time"].to_numpy()[-1])
        lon_res = abs(np.diff(test_ds_i["longitude"].to_numpy())[0])
        res_lon_list.append(lon_res)
        lat_res = abs(np.diff(test_ds_i["latitude"].to_numpy())[0])
        res_lat_list.append(lat_res)
    test_pd = pd.DataFrame(
        {
            "bbox": bbox_list,
            "time_start": start_time,
            "time_end": end_list,
            "res_lon": lon_res,
            "res_lat": lat_res,
            "path": ["s3://" + file for file in era5_land_zarr_files],
        }
    )
    test_pd.to_csv("era5_land_metadata.csv")
