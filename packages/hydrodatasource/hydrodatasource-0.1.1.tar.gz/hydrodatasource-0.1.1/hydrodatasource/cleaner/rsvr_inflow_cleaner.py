"""
Author: liutiaxqabs 1498093445@qq.com
Date: 2024-04-19 14:00:16
LastEditors: Wenyu Ouyang
LastEditTime: 2025-01-16 16:28:02
FilePath: \hydrodatasource\hydrodatasource\cleaner\rsvr_inflow_cleaner.py
Description: calculate streamflow from reservoir timeseries data
"""

import collections
import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.optimize import curve_fit

from hydroutils.hydro_log import hydro_logger
from hydrodatasource.configs.table_name import RSVR_TS_TABLE_COLS
from hydrodatasource.cleaner.cleaner import Cleaner


@hydro_logger
class ReservoirInflowBacktrack(Cleaner):
    def __init__(self, data_folder, output_folder):
        """
        Back-calculating inflow of reservior

        Parameters
        ----------
        data_folder : str
            the folder of reservoir data
        output_folder : _type_
            where we put inflow data
        """
        self.data_folder = data_folder
        self.output_folder = output_folder
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        self.data_source_description = self.set_data_source_describe()
        self._check_file_format()
        self.rsvr_info = self.read_rsvr_info()

    def set_data_source_describe(self):
        data_source_dir = self.data_folder
        # we must have a file to provide the reservoir basic information
        rsvr_idname_file = os.path.join(data_source_dir, "rsvr_stcd_stnm.xlsx")
        rsvr_charact_waterlevel_file = os.path.join(
            data_source_dir, "rsvr_charact_waterlevel.csv"
        )
        # all files in data_source_dir other than rsvr_idname_file and rsvr_charact_waterlevel_file
        rsvr_inflow_files = [
            os.path.join(data_source_dir, f)
            for f in os.listdir(data_source_dir)
            if f not in {"rsvr_stcd_stnm.xlsx", "rsvr_charact_waterlevel.csv"}
        ]
        # sort these files -- list
        rsvr_inflow_files.sort()
        return collections.OrderedDict(
            RSVR_IDNAME_FILE=rsvr_idname_file,
            RSVR_CHARACT_WATERLEVEL_FILE=rsvr_charact_waterlevel_file,
            RSVR_INFLOW_FILES=rsvr_inflow_files,
        )

    def _check_file_format(self):
        """
        Check if the files in the given folder match the specified format.

        Raises
        ----------
        ValueError
            If a file name does not match the specified format, an error is raised with the specific file name.
        """
        self.logger.info(
            "Please make sure the data is in the right format. We are checking now ..."
        )
        rsvr_idname_file = self.data_source_description["RSVR_IDNAME_FILE"]
        rsvr_charact_waterlevel_file = self.data_source_description[
            "RSVR_CHARACT_WATERLEVEL_FILE"
        ]
        if not os.path.exists(rsvr_idname_file) or not os.path.exists(
            rsvr_charact_waterlevel_file
        ):
            raise FileNotFoundError(
                f"{rsvr_idname_file} or {rsvr_charact_waterlevel_file} not found. please provide them both. If you don't have them, please contact the data provider or the author of this code."
            )
        pattern = re.compile(r".+_rsvr_data\.csv$")
        for file_path in self.data_source_description["RSVR_INFLOW_FILES"]:
            if not pattern.match(file_path):
                raise ValueError(f"File name does not match the format: {file_path}")
            try:
                df = pd.read_csv(file_path, dtype={"STCD": str})
                # if all rows length is less than 2, we will not process this file and raise an error to inform the user delete it
                # if most RZ values are NaN, we will not process this file and raise an error to inform the user delete it
                # we think at least 72 values (maybe 3 days) should exist
                if len(df) < 72 or df["RZ"].isna().sum() > len(df) - 72:
                    raise ValueError(
                        f"There are too few values in the file: {file_path}, hence it is useless. Please manually delete it."
                    )
            except Exception as e:
                raise ValueError(f"Unable to read file: {file_path}, error: {e}") from e

            if any(column not in df.columns for column in RSVR_TS_TABLE_COLS):
                raise ValueError(
                    f"File content does not match the format: {file_path}, missing columns: {set(RSVR_TS_TABLE_COLS) - set(df.columns)}"
                )
        self.logger.info("All files are in the right format.")

    def read_rsvr_info(self):
        rsvr_idname_file = self.data_source_description["RSVR_IDNAME_FILE"]
        rsvr_info = pd.read_excel(rsvr_idname_file, dtype={"STCD": str})
        # check if it has two columns: STCD and STNM
        if "STCD" not in rsvr_info.columns or "STNM" not in rsvr_info.columns:
            raise ValueError(
                "rsvr_stcd_stnm.xlsx should have two columns: STCD and STNM"
            )
        # sort by STCD, and reindex
        rsvr_info = rsvr_info.sort_values(by="STCD").reset_index(drop=True)
        # read the reservoir characteristic water level data
        rsvr_charact_waterlevel_file = self.data_source_description[
            "RSVR_CHARACT_WATERLEVEL_FILE"
        ]
        rsvr_charact_waterlevel = pd.read_csv(
            rsvr_charact_waterlevel_file, dtype={"STCD": str}
        )
        # find the NORMZ, DDZ, ... in rsvr_charact_waterlevel of STCD in rsvr_info
        rsvr_info = rsvr_info.merge(rsvr_charact_waterlevel, on="STCD", how="left")
        # if a rsvr has no inflow file, we will remove it and not process it
        rsvr_info = rsvr_info[
            rsvr_info["STCD"].isin(
                [
                    os.path.basename(f).split("_")[0]
                    for f in self.data_source_description["RSVR_INFLOW_FILES"]
                ]
            )
        ]
        # assert if STCD is sorted
        assert rsvr_info["STCD"].tolist() == sorted(rsvr_info["STCD"].tolist())
        self.logger.info(
            "Reservoir information read successfully. Note we only process the reservoirs with inflow data."
        )
        # update the rsvr inflow files, later we only process these reservoirs
        rsvr_info["RSVR_INFLOW_FILES"] = [
            os.path.join(self.data_folder, f"{stcd}_rsvr_data.csv")
            for stcd in rsvr_info["STCD"]
        ]
        # check if each STCD row has same name in RSVR_INFLOW_FILES
        assert all(
            rsvr_info.loc[i, "STCD"] in rsvr_info.loc[i, "RSVR_INFLOW_FILES"]
            for i in rsvr_info.index
        )
        # Assert that used waterlevel and storage columns are numeric
        for col in ["DDZ", "NORMZ", "DSFLZ", "DDCP", "TTCP"]:
            assert np.issubdtype(
                rsvr_info[col].dtype, np.number
            ), f"Column {col} is not of numeric type"
        return rsvr_info

    def _rsvr_rolling_window_abrupt_abnormal_rm(
        self, df, var_col="RZ", threshold=50, window_size=5
    ):
        """
        Detect and remove abnormal reservoir water level data using a rolling window.

        Parameters
        ----------
        df : pd.DataFrame
            The DataFrame containing the reservoir data.
        var_col : str
            the column to check, by default "RZ"
        threshold: float
            the threshold to remove the abnormal data
        window_size : int
            The size of the rolling window.

        Returns
        -------
        pd.DataFrame
            The DataFrame with an additional column indicating abnormal data.
        """

        # Calculate the median of the rolling window
        df["median"] = df[var_col].rolling(window=window_size, center=True).median()
        # Calculate the difference between the current value and the median
        df["diff_median"] = abs(df[var_col] - df["median"])
        # Mark as abnormal if the difference exceeds the threshold
        df["set_nan"] = df["diff_median"] > threshold
        # Set abnormal values to NaN
        df.loc[df["set_nan"], var_col] = np.nan
        return df

    def _rsvr_conservative_abrupt_abnormal_rm(self, df, var_col="RZ", threshold=10):
        """TODO: this method is not right, need to be fixed

        Parameters
        ----------
        df : pd.DataFrame
            the data
        var_col : str
            the column to check, by default "RZ"
        threshold: float
            the threshold to remove the abnormal data
        """
        df["diff_prev"] = abs(df[var_col] - df[var_col].shift(1))
        # 计算与后一行的差异
        df["diff_next"] = abs(df[var_col] - df[var_col].shift(-1))
        # 标记需要设置为 NaN 的行, | is too strict and may delete some normal data; & is too loose and may keep some abnormal data
        # df["set_nan"] = (df["diff_prev"] > threshold) | (df["diff_next"] > threshold)
        df["set_nan"] = (df["diff_prev"] > threshold) & (df["diff_next"] > threshold)
        # 如果与前一行和后一行的差异超过threshold，则设置为 NaN
        df.loc[df["set_nan"], var_col] = np.nan
        return df

    def _save_fitted_zw_curve(self, df, quadratic_fit_curve_coeff, output_folder):
        """Save a plot of the RZ and W points along with the fitted curve so that
        the relationship between RZ and W can be visualized and verified

        Parameters
        ----------
        df : pd.DataFrame
            _description_
        quadratic_fit_curve_coeff : _type_
            a list of coefficients of the quadratic fit curve
        output_folder : _type_
            _description_
        """
        plt.figure(figsize=(14, 7))
        plt.scatter(df["RZ"], df["W"], label="Data Points")
        # to plot w_fit = a * rz^2 + b * rz + c, we need to set some x values and calculate the y values
        rz_range = np.linspace(df["RZ"].min(), df["RZ"].max(), 100)
        w_fit = (
            quadratic_fit_curve_coeff[0] * rz_range**2
            + quadratic_fit_curve_coeff[1] * rz_range
            + quadratic_fit_curve_coeff[2]
        )
        plt.plot(rz_range, w_fit, color="red", label="Fitted Curve")
        plt.xlabel("RZ (m)")
        plt.ylabel("W (10$^6$ m$^3$)")
        plt.legend()
        plt.title("RZ vs W with Fitted Curve")
        plot_path = os.path.join(output_folder, "fit_zw_curve.png")
        plt.savefig(plot_path)

    def _plot_var_before_after_clean(
        self,
        df_origin,
        df,
        plot_column,
        plot_path,
        label_orginal="Original Reservoir Storage",
        label_cleaned="Cleaned Reservoir Storage",
        ylab="Reservoir Storage (10^6 m^3)",
        title="Reservoir Storage Analysis with Outliers Removed",
    ):
        """Plot the original and cleaned Reservoir Storage data for comparison

        Parameters
        ----------
        df_origin : str
            the original data
        df : pd.DataFrame
            the cleaned data
        plot_path : str
            where to save the plot
        plot_column: str
            the column to show; note same name for df and df_origin
        """
        plt.figure(figsize=(14, 7))

        # 绘制原始数据
        plt.plot(
            df_origin.index,
            df_origin[plot_column],
            label=label_orginal,
            color="blue",
            linestyle="--",
        )

        # 绘制清洗后的数据
        plt.scatter(
            df.index,
            df[plot_column],
            label=label_cleaned,
            color="red",
        )

        plt.xlabel("Time")
        plt.ylabel(ylab)
        plt.title(title)
        plt.legend()

        # 保存图像到与CSV文件相同的目录
        plt.savefig(plot_path)

    def _rsvr_valuerange_abnormal_rm(self, df, var_col, range):
        """Remove abnormal reservoir data based on a range of values

        Parameters
        ----------
        df : pd.DataFrame
            _description_
        var_col : str
            the column to check
        range : list
            [lower_bound, upper_bound]

        Returns
        -------
        pd.DataFrame
            the cleaned data
        """
        lower_bound, upper_bound = range

        if lower_bound is not None and not np.isnan(lower_bound):
            df["set_nan_lower"] = df[var_col] < lower_bound
        else:
            df["set_nan_lower"] = False

        if upper_bound is not None and not np.isnan(upper_bound):
            df["set_nan_upper"] = df[var_col] > upper_bound
        else:
            df["set_nan_upper"] = False

        df["set_nan"] = df["set_nan_lower"] | df["set_nan_upper"]
        df.loc[df["set_nan"], var_col] = np.nan

        # 删除临时列
        df = df.drop(columns=["set_nan_lower", "set_nan_upper"])
        return df

    def clean_w(
        self,
        rsvr_id,
        file_path,
        output_folder,
        fit_method="quadratic",
        zw_curve_std_times=3.0,
        remove_zw_outliers=False,
    ):
        """
        Remove abnormal reservoir capacity data

        Parameters
        ----------
        rsvr_id : str
            The ID of the reservoir
        file_path : str
            Path to the input file
        output_folder : str
            Path to the output folder
        fit_method : str, optional
            z-w curve fitting method, by default "quadratic"
            TODO: MORE METHODS need to be supported; power is also need to be debugged
        zw_curve_std_times: float, optional
            the times of standard deviation to remove outliers, by default 3
        remove_zw_outliers: bool, optional
            whether to remove outliers for z-w curve fitting, by default False

        Returns
        -------
        str
            Path to the cleaned data file
        """
        data = self._read_rsvrinflow_csv_file(file_path)

        rsvr_info = self.rsvr_info[self.rsvr_info["STCD"] == rsvr_id]

        def _not_reasonable_value(the_value):
            return the_value is None or the_value < 0 or np.isnan(the_value)

        # remove abnormal reservoir water level data
        rsvr_dead_waterlevel = rsvr_info["DDZ"].values[0]
        rsvr_normal_waterlevel = rsvr_info["NORMZ"].values[0]
        rsvr_desighflood_waterlevel = rsvr_info["DSFLZ"].values[0]
        rz_threshold = rsvr_normal_waterlevel - rsvr_dead_waterlevel
        if _not_reasonable_value(rsvr_normal_waterlevel) and not _not_reasonable_value(
            rsvr_desighflood_waterlevel
        ):
            rz_threshold = rsvr_desighflood_waterlevel - rsvr_dead_waterlevel
        if _not_reasonable_value(rz_threshold):
            rz_threshold = 50
        if _not_reasonable_value(rsvr_dead_waterlevel):
            # to avoid negative and very small values
            rsvr_dead_waterlevel = 1
        if _not_reasonable_value(rsvr_desighflood_waterlevel):
            # no such level data, so we have to set it with normal level
            rsvr_desighflood_waterlevel = rsvr_normal_waterlevel
        rz_range = [rsvr_dead_waterlevel, rsvr_desighflood_waterlevel]
        data = self._rsvr_conservative_abrupt_abnormal_rm(
            data, "RZ", threshold=rz_threshold
        )
        data = self._rsvr_valuerange_abnormal_rm(data, "RZ", range=rz_range)

        # remove abnormal reservoir storage data
        rsvr_dead_storage = rsvr_info["DDCP"].values[0]
        rsvr_total_storage = rsvr_info["TTCP"].values[0]
        w_threshold = rsvr_total_storage - rsvr_dead_storage
        if _not_reasonable_value(w_threshold):
            # 100 means 0.1 billion m^3 difference between the current value and the median
            w_threshold = 100
        if _not_reasonable_value(rsvr_dead_storage):
            # to avoid negative and very small values
            rsvr_dead_storage = 0.001
        w_range = [rsvr_dead_storage, rsvr_total_storage]
        data = self._rsvr_conservative_abrupt_abnormal_rm(
            data, "W", threshold=w_threshold
        )
        data = self._rsvr_valuerange_abnormal_rm(data, "W", range=w_range)

        # set valuerange abnormal rm for outflow, outflow cannot be negative
        data = self._rsvr_valuerange_abnormal_rm(data, "OTQ", range=[0, None])

        # for row of ["RZ", "W", "OTQ"], if any value is NaN meaning set_nan is True, we set both "RZ", "W", "OTQ" in the row to NaN
        data.loc[data["set_nan"], "RZ"] = np.nan
        data.loc[data["set_nan"], "W"] = np.nan
        data.loc[data["set_nan"], "OTQ"] = np.nan

        # 输出被设置为 NaN 的行
        self.logger.debug(data[data["set_nan"]])

        # 保存被设置为 NaN 的行到 CSV 文件
        data[data["set_nan"]].to_csv(
            os.path.join(output_folder, "库容异常的数据行.csv"), index=False
        )
        valid_data = data.dropna(subset=["RZ", "W"])
        valid_data, coefficients = fit_zw_curve(
            valid_data,
            x_col="RZ",
            y_col="W",
            method=fit_method,
            threshold=zw_curve_std_times,
        )
        # recover rows with NaN values for valid data
        # Get the dropped rows, NOTE some rows may be dropped in fit_zw_curve
        dropped_rows = data[~data.index.isin(valid_data.index)]
        # Set 'RZ' and 'W' columns to NaN in the dropped rows
        dropped_rows["RZ"] = np.nan
        dropped_rows["W"] = np.nan
        # Combine valid_data and dropped_rows
        combined_data = pd.concat([valid_data, dropped_rows]).sort_index()
        self.logger.info(
            f"For {rsvr_id}, removed {len(data.dropna(subset=['RZ', 'W'])) - len(valid_data)} outliers for z-w curve fitting."
        )
        if remove_zw_outliers:
            # we will remove the outliers for z-w curve fitting and only use the valid data
            data = combined_data
        # Plot RZ and W points along with the fitted curve
        self._save_fitted_zw_curve(data, coefficients, output_folder)
        # 根据拟合的多项式关系更新 W 列
        if fit_method == "quadratic":
            data["W"] = np.polyval(coefficients, data["RZ"])
        elif fit_method == "power":
            data["W"] = _func_abcd_power(data["RZ"], *coefficients)
        else:
            raise ValueError(f"Unsupported fit method: {fit_method}")

        cleaned_path = os.path.join(output_folder, "去除库容异常的数据.csv")
        data["TM"] = data.index.strftime("%Y-%m-%d %H:%M:%S")
        original_data = self._read_rsvrinflow_csv_file(file_path)
        plot_path = os.path.join(output_folder, "rsvr_w_clean.png")
        data.to_csv(cleaned_path, index=False)
        self._plot_var_before_after_clean(original_data, data, "W", plot_path)
        return cleaned_path

    def back_calculation(self, rsvr_id, clean_w_path, original_file, output_folder):
        """Back-calculate inflow from reservoir storage data
        NOTE: each time has three columns: I Q W -- I is the inflow, Q is the outflow, W is the reservoir storage
        Generally, in sql database, a time means the end of previous time period
        For example, a hourly database, 13:00 means 12:00-13:00 period because the data is GOT at 13:00 (we cannot observe future)
        Hence, for this function, W means the storage at the end of the time period, I and Q means the inflow and outflow of the time period
        So we need to use W of the previous time as the initial water storage of the time period.
        Hence, I1 = Q1 + (W1 - W0)


        Parameters
        ----------
        rsvr_id : str
            The ID of the reservoir
        data_path : str
            the path to the cleaned_w_data file
        original_file: str
            the path to the original file
        output_folder : str
            where to save the back calculated data

        Returns
        -------
        str
            the path to the result file
        """
        data = self._read_rsvrinflow_csv_file(clean_w_path)
        # diff means the difference between this time and the previous time -- the first will be 0 as fillna(0)
        data["Time_Diff"] = data.index.diff().total_seconds().fillna(0)
        data["INQ_ACC"] = data["OTQ"] + (10**6 * (data["W"].diff() / data["Time_Diff"]))
        data["INQ"] = data["INQ_ACC"]
        # data["Month"] = data["TM"].dt.month
        self.logger.debug(data)
        back_calc_path = os.path.join(output_folder, f"{rsvr_id}_径流直接反推数据.csv")
        # index trans to column
        data["TM"] = data.index.strftime("%Y-%m-%d %H:%M:%S")
        data[RSVR_TS_TABLE_COLS].to_csv(back_calc_path, index=False)
        # plot the inflow data and compare with the original data
        original_data = self._read_rsvrinflow_csv_file(original_file)
        self._plot_var_before_after_clean(
            original_data,
            data,
            "INQ",
            os.path.join(output_folder, "inflow_comparison.png"),
            label_orginal="Original Inflow",
            label_cleaned="Back-calculated Inflow",
            ylab="Inflow (m^3/s)",
            title="Inflow Analysis with Back-calculation",
        )
        return back_calc_path

    def delete_negative_inq(
        self,
        rsvr_id,
        inflow_data_path,
        original_file,
        output_folder,
        negative_deal_window=7,
        negative_deal_stride=4,
    ):
        """remove negative inflow values with a rolling window
        the negative value will be adjusted to positvie ones to make the total inflow consistent
        for example,  1, -1, 1, -1 will be adjusted to 0, 0, 0, 0 so that wate balance is kept
        but note that as the window has stride, maybe the final few values will not be adjusted

        Parameters
        ----------
        rsvr_id : str
            the id of the reservoir
        inflow_data_path : str
            the data file after back_calculation
        original_file : str
            the original file
        output_folder : str
            where to save the data
        negative_deal_window : int, optional
            the window to deal with negative values, by default 7
        negative_deal_stride : int, optional
            the stride of window, by default 4

        Returns
        -------
        str
            the path to the result file
        """
        # 读取CSV文件到DataFrame
        df = self._read_rsvrinflow_csv_file(inflow_data_path)

        self.logger.debug(df["INQ"].sum())

        def adjust_window(window):
            """adjust window for delete negative inflow values

            Parameters
            ----------
            window : pd.Series
                the data in the window

            Returns
            -------
            _type_
                _description_
            """
            if window.count() == 0:
                return window  # 如果窗口内全是NaN，返回原窗口

            # 移除负值
            positive_values = window[window > 0]
            negative_values = window[window < 0]

            # 计算正负值的总和
            pos_sum = positive_values.sum()
            neg_sum = abs(negative_values.sum())  # 负值的绝对值和

            # 计算需要调整的比例
            if pos_sum > 0:
                adjust_factor = neg_sum / pos_sum
                # 调整正值
                adjusted_values = positive_values - (positive_values * adjust_factor)
            else:
                adjusted_values = positive_values  # 如果没有正值可用于调整，保持原样

            # 更新窗口的值
            window[window > 0] = adjusted_values
            window[window <= 0] = 0

            return window

        def rolling_with_stride(df, column, window_size, stride, func):
            # 遍历数据，步长为stride
            for i in range(0, len(df) - window_size + 1, stride):
                window_indices = range(i, i + window_size)
                df.loc[df.index[window_indices], column] = func(
                    df.loc[df.index[window_indices], column]
                )

        # 应用滚动窗口函数，这里设置步幅为4，窗口大小为7
        rolling_with_stride(
            df,
            "INQ",
            window_size=negative_deal_window,
            stride=negative_deal_stride,
            func=adjust_window,
        )
        path = os.path.join(output_folder, f"{rsvr_id}_水量平衡后的日尺度反推数据.csv")

        df["TM"] = df.index.strftime("%Y-%m-%d %H:%M:%S")
        df[RSVR_TS_TABLE_COLS].to_csv(path, index=False)
        # plot the inflow data and compare with the original data
        original_data = self._read_rsvrinflow_csv_file(original_file)
        self._plot_var_before_after_clean(
            original_data,
            df,
            "INQ",
            os.path.join(output_folder, "inflow_comparison_after_negative.png"),
            label_orginal="Original Inflow",
            label_cleaned="Inflow After Negative Removal",
            ylab="Inflow (m^3/s)",
            title="Inflow Analysis with Negative Removal",
        )
        return path

    def _read_rsvrinflow_csv_file(self, the_csv_data_path):
        """read reservoir inflow data from csv file
        set TM datetime and make it index and check if the columns are numeric

        Parameters
        ----------
        the_csv_data_path : str
            path to the csv file

        Returns
        -------
        pd.DataFrame
            the data
        """
        df = pd.read_csv(the_csv_data_path, dtype={"STCD": str})
        for col in ["RZ", "INQ", "W", "OTQ"]:
            assert np.issubdtype(
                df[col].dtype, np.number
            ), f"Column {col} is not of numeric type"
        # 将'TM'列转换为日期时间格式并设置为索引
        df["TM"] = pd.to_datetime(df["TM"])

        # 设置调整后的时间为索引
        df = df.set_index("TM")
        return df

    def insert_inq(self, rsvr_id, inflow_data_path, original_file, output_folder):
        """make inflow data as hourly data as original data is not strictly hourly data
        and insert inq with linear interpolation

        Parameters
        ----------
        rsvr_id : str
            the id of the reservoir
        inflow_data_path : str
            the data file after delete negative inflow values
        original_file : str
            the original file
        output_folder : str
            where to save the data

        Returns
        -------
        str
            the path to the result file
        """
        # 读取CSV文件到DataFrame
        _df = self._read_rsvrinflow_csv_file(inflow_data_path)

        # 生成从开始日期到结束日期的完整时间序列，按小时
        date_range = pd.date_range(start=_df.index.min(), end=_df.index.max(), freq="h")
        complete_df = pd.DataFrame(index=date_range)

        # Perform a full outer join of the original data with the complete time series table, so that some sub-hourly data could still be saved here
        df_join = complete_df.join(_df, how="outer")

        # deal with numeric columns
        numeric_cols = df_join.select_dtypes(include=[np.number]).columns
        numeric_df = df_join[numeric_cols].resample("h").mean()

        # deal with non-numeric columns
        non_numeric_cols = df_join.select_dtypes(exclude=[np.number]).columns
        non_numeric_df = df_join[non_numeric_cols].resample("H").first()

        # 合并数值列和非数值列
        df = pd.concat([numeric_df, non_numeric_df], axis=1)

        # Ensure INQ values are not less than 0 -- mainly for final few values as previous steps may not adjust them
        df["INQ"] = df["INQ"].where(df["INQ"] >= 0, np.nan)

        # 使用线性插值
        # 插值前检查连续缺失是否超过7天（7*24小时）
        df_ = linear_interpolate_wthresh(df)

        result_path = os.path.join(output_folder, f"{rsvr_id}_rsvr_data.csv")

        self.logger.debug("水量平衡的小时尺度滑动平均反推数据：输出行名称")
        self.logger.debug(df_.columns)
        df_["TM"] = df_.index.strftime("%Y-%m-%d %H:%M:%S")
        df_[RSVR_TS_TABLE_COLS].to_csv(result_path, index=False)
        # plot the inflow data and compare with the original data
        original_data = self._read_rsvrinflow_csv_file(original_file)
        self._plot_var_before_after_clean(
            original_data,
            df_,
            "INQ",
            os.path.join(output_folder, "inflow_comparison_after_interpolation.png"),
            label_orginal="Original Inflow",
            label_cleaned="Inflow After Interpolation",
            ylab="Inflow (m^3/s)",
            title="Inflow Analysis with Interpolation",
        )
        return result_path

    def rsvr_inflow_clean(self, **kwargs):
        """
        The reservoir inflow data cleaning pipeline

        Parameters
        ----------
        zw_curve_std_times : float
            the times of standard deviation to remove outliers, by default 3.0
        remove_zw_outliers : bool
            whether to remove outliers for z-w curve fitting, by default False
        """
        rsvr_info = self.rsvr_info
        zw_curve_std_times = kwargs.get("zw_curve_std_times", 3.0)
        remove_zw_outliers = kwargs.get("remove_zw_outliers", False)
        # save info file into output folder so that later we can simply read cleaned data
        rsvr_info.to_csv(os.path.join(self.output_folder, "rsvr_info.csv"), index=False)
        for i, rsvr_id in tqdm(enumerate(rsvr_info["STCD"].values)):
            file_path = rsvr_info["RSVR_INFLOW_FILES"].iloc[i]
            # Process each file step by step
            self.process_backtract_1rsvr(
                rsvr_id, file_path, zw_curve_std_times, remove_zw_outliers
            )

    def process_backtract_1rsvr(
        self, rsvr_id, file_path, zw_curve_std_times, remove_zw_outliers
    ):
        output_folder = os.path.join(self.output_folder, rsvr_id)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        cleaned_data_file = self.clean_w(
            rsvr_id,
            file_path,
            output_folder,
            zw_curve_std_times=zw_curve_std_times,
            remove_zw_outliers=remove_zw_outliers,
        )
        # 公式计算反推
        back_data_file = self.back_calculation(
            rsvr_id, cleaned_data_file, file_path, output_folder
        )
        # 去除反推异常值
        nonegative_data_file = self.delete_negative_inq(
            rsvr_id, back_data_file, file_path, output_folder
        )
        # 插值平衡
        self.insert_inq(rsvr_id, nonegative_data_file, file_path, output_folder)
        # release memory for plot after each basin
        plt.close("all")


def linear_interpolate_wthresh(df, column="INQ", threshold=168):
    """linear interpolation for inflow data with a threshod

    Parameters
    ----------
    df : pd.DataFrame
        pandas DataFrame containing the inflow data
    column : str, optional
        the chosen column, by default "INQ"
    threshold : int, optional
        under this threshold we interpolate, by default 168,
        if the missing data is larger than 7 days, we didn't interpolate it

    Returns
    -------
    pd.DataFrame
        DataFrame with interpolated values
    """
    # Calculate the gap lengths of missing values
    mask = df[column].isna()
    gap_lengths = []
    gap_length = 0
    for is_na in mask:
        if is_na:
            gap_length += 1
        else:
            if gap_length > 0:
                gap_lengths.extend([gap_length] * gap_length)
                gap_length = 0
            gap_lengths.append(0)
    if gap_length > 0:
        gap_lengths.extend([gap_length] * gap_length)

    # Convert gap lengths to Series
    gap_lengths = pd.Series(gap_lengths, index=df.index)
    # Only interpolate missing values with gaps less than the threshold, and set limit_direction to 'both' to ensure extrapolation
    df.loc[mask & (gap_lengths <= threshold), column] = df[column].interpolate(
        limit_direction="both"
    )

    return df


def _func_abcd_power(x, a, b, c, d):
    return a * x**b + c * x + d


def fit_zw_curve(df, x_col, y_col, method="quadratic", threshold=3.0):
    """Fit a curve to the data using the specified method.

    Parameters
    ----------
    df : pd.DataFrame
        The data
    x_col : str
        The x column to fit, such as "RZ"
    y_col : str
        The y column to fit, such as "W"
    method : str, optional
        The fitting method, either "quadratic" or "power", by default "quadratic"
    threshold: float, optional
        The threshold for filtering outliers, by default 3 means 3 times of standard deviation

    Returns
    -------
    list
        The filtered df and coefficients of the fit curve
    """

    def calculate_residuals(df, x_col, y_col, coefficients, func=None):
        if func:
            fitted_values = func(df[x_col], *coefficients)
        else:
            fitted_values = np.polyval(coefficients, df[x_col])
        residuals = df[y_col] - fitted_values
        return residuals

    def filter_outliers(df, residuals, threshold=3.0):
        std_threshold = threshold * np.std(residuals)
        return df[np.abs(residuals) < std_threshold]

    if method == "quadratic":
        coefficients = np.polyfit(df[x_col], df[y_col], 2)
        residuals = calculate_residuals(df, x_col, y_col, coefficients)
        df_ = filter_outliers(df, residuals, threshold=threshold)
        coefficients = np.polyfit(df_[x_col], df_[y_col], 2)
        return df_, coefficients

    elif method == "power":
        param_bounds = ([-np.inf, 0, -np.inf, -np.inf], [np.inf, 2, np.inf, np.inf])
        popt, _ = curve_fit(_func_abcd_power, df[x_col], df[y_col], bounds=param_bounds)
        residuals = calculate_residuals(df, x_col, y_col, popt, _func_abcd_power)
        df_ = filter_outliers(df, residuals, threshold=threshold)
        popt, _ = curve_fit(
            _func_abcd_power, df_[x_col], df_[y_col], bounds=param_bounds
        )
        return df_, popt

    else:
        raise ValueError("Invalid method. Choose either 'quadratic' or 'power'.")
