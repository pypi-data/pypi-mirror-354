"""
Author: liutiaxqabs 1498093445@qq.com
Date: 2024-04-19 14:00:16
LastEditors: Wenyu Ouyang
LastEditTime: 2025-01-07 21:06:53
FilePath: \hydrodatasource\hydrodatasource\cleaner\streamflow_cleaner.py
Description: clean streamflow (reservoir inflow) using moving average methods
"""

import numpy as np
import pandas as pd
from scipy.fft import fft, fftfreq, ifft
from scipy.optimize import curve_fit
from scipy.signal import butter, cwt, filtfilt, morlet

from hydrodatasource.cleaner.cleaner import Cleaner


class StreamflowCleaner(Cleaner):
    def __init__(
        self,
        data_folder,
        window_size=14,
        stride=1,
        cutoff_frequency=0.035,
        time_step=1.0,
        iterations=3,
        sampling_rate=1.0,
        order=5,
        cwt_row=2,
        *args,
        **kwargs,
    ):
        self.window_size = window_size
        self.stride = stride
        self.cutoff_frequency = cutoff_frequency
        self.time_step = time_step
        self.iterations = iterations
        self.sampling_rate = sampling_rate
        self.order = order
        self.cwt_row = cwt_row
        super().__init__(data_folder, *args, **kwargs)

    def data_balanced(self, origin_data, transform_data):
        """
        对一维流量数据进行总量平衡变换。
        :origin_data: 原始一维流量数据。
        :transform_data: 平滑转换后的一维流量数据。
        """
        # Calculate the flow balance factor and keep the total volume consistent
        streamflow_data_before = np.sum(origin_data)
        streamflow_data_after = np.sum(transform_data)
        scaling_factor = streamflow_data_before / streamflow_data_after
        balanced_data = transform_data * scaling_factor

        print(f"Total flow (before smoothing): {streamflow_data_before}")
        print(f"Total flow (after smoothing): {np.sum(balanced_data)}")
        return balanced_data

    def moving_average(self, streamflow_data):
        """
        对流量数据应用滑动平均进行平滑处理，并保持流量总量平衡。
        :param streamflow_data: 输入的流量数据数组
        :return: 平滑处理后的流量数据
        """
        # 将流量数据转换为 pandas Series
        streamflow_series = streamflow_data

        # 应用中心滑动平均
        smoothed_series = streamflow_series.rolling(
            window=self.window_size, center=True
        ).mean()

        # 填充由于滚动窗口导致的起始和结束的 NaN 值
        smoothed_series.bfill(inplace=True)  # 用后面的值填充前面的 NaN
        smoothed_series.ffill(inplace=True)  # 用前面的值填充后面的 NaN

        # 将平滑数据中的负值置为0
        smoothed_series[smoothed_series < 0] = 0

        # 将结果转换回 numpy 数组
        smoothed_data = smoothed_series

        return self.data_balanced(streamflow_data, smoothed_data)

    def kalman_filter(self, streamflow_data):
        """
        对流量数据应用卡尔曼滤波进行平滑处理，并保持流量总量平衡。
        :param streamflow_data: 原始流量数据
        """
        A = np.array([[1]])
        H = np.array([[1]])
        Q = np.array([[0.01]])
        R = np.array([[0.01]])
        X_estimated = np.array([streamflow_data[0]])
        P_estimated = np.eye(1) * 0.01
        estimated_states = []

        for measurement in streamflow_data:
            # predict
            X_predicted = A.dot(X_estimated)
            P_predicted = A.dot(P_estimated).dot(A.T) + Q

            # update
            measurement_residual = measurement - H.dot(X_predicted)
            S = H.dot(P_predicted).dot(H.T) + R
            K = P_predicted.dot(H.T).dot(np.linalg.inv(S))  # kalman gain
            X_estimated = X_predicted + K.dot(measurement_residual)
            P_estimated = P_predicted - K.dot(H).dot(P_predicted)
            estimated_states.append(X_estimated.item())

        estimated_states = np.array(estimated_states)

        # Apply non-negative constraints
        estimated_states[estimated_states < 0] = 0
        return self.data_balanced(streamflow_data, estimated_states)

    def adjust_window(self, window):
        if window.count() == 0:
            return np.nan  # 如果窗口内全是NaN，则返回NaN
        adjusted_window = window.copy()
        return adjusted_window.mean()  # 返回窗口的平均值或其他适当的聚合值

    def rolling_with_stride(self, df, func):
        # 初始化与原始 DataFrame 长度相同的 NaN 序列
        results = pd.Series(np.nan, index=df.index)
        # 遍历数据，步长为stride
        for i in range(0, len(df) - self.window_size + 1, self.stride):
            window = df[i : i + self.window_size]
            result = func(window)
            # 计算窗口中心的索引
            center_index = i + self.window_size // 2
            # 仅在中心索引处填充结果
            results.iloc[center_index] = result

        return results

    def moving_average_difference(self, streamflow_data):
        """
        对流量数据应用滑动平均差算法进行平滑处理，并保持流量总量平衡。
        :window_size: 滑动窗口的大小
        """
        streamflow_data_series = pd.Series(streamflow_data)
        # Calculate the forward moving average（MU）
        forward_ma = streamflow_data_series.rolling(
            window=self.window_size, min_periods=1
        ).mean()

        # Calculate the backward moving average（MD）
        backward_ma = (
            streamflow_data_series.iloc[::-1]
            .rolling(window=self.window_size, min_periods=1)
            .mean()
            .iloc[::-1]
        )

        # Calculate the difference between the forward and backward sliding averages
        ma_difference = abs(forward_ma - backward_ma)

        # Apply non-negative constraints
        ma_difference[ma_difference < 0] = 0
        return self.data_balanced(streamflow_data, ma_difference.to_numpy())

    def quadratic_function(self, x, a, b, c):
        return a * x**2 + b * x + c

    def robust_fitting(self, streamflow_data, k=1.5):
        """
        对流量数据应用抗差修正算法进行平滑处理，并保持流量总量平衡。
        默认采用二次曲线进行拟合优化，该算法处理性能较差
        """
        time_steps = np.arange(len(streamflow_data))
        params, _ = curve_fit(self.quadratic_function, time_steps, streamflow_data)
        smoothed_streamflow = self.quadratic_function(time_steps, *params)
        residuals = streamflow_data - smoothed_streamflow
        m = len(streamflow_data)
        sigma = np.sqrt(np.sum(residuals**2) / (m - 1))

        for _ in range(10):
            weights = np.where(
                np.abs(residuals) <= k * sigma, 1, k * sigma / np.abs(residuals)
            )
            sigma = np.sqrt(np.sum(weights * residuals**2) / (m - 1))

        corrected_streamflow = (
            weights * streamflow_data + (1 - weights) * smoothed_streamflow
        )
        corrected_streamflow[corrected_streamflow < 0] = 0
        return self.data_balanced(streamflow_data, corrected_streamflow)

    def lowpass_filter(self, streamflow_data):
        """
        对一维流量数据应用调整后的低通滤波器。
        :cutoff_frequency: 低通滤波器的截止频率。
        :sampling_rate: 数据的采样率。
        :order: 滤波器的阶数，默认为5。
        """

        def apply_low_pass_filter(signal, cutoff_frequency, sampling_rate, order=5):
            nyquist_frequency = 0.5 * sampling_rate
            normalized_cutoff = cutoff_frequency / nyquist_frequency
            b, a = butter(order, normalized_cutoff, btype="low", analog=False)
            filtered_signal = filtfilt(b, a, signal)
            return filtered_signal

        # Apply a low-pass filter
        low_pass_filtered_signal = apply_low_pass_filter(
            streamflow_data, self.cutoff_frequency, self.sampling_rate, self.order
        )

        # Apply non-negative constraints
        low_pass_filtered_signal[low_pass_filtered_signal < 0] = 0

        return self.data_balanced(streamflow_data, low_pass_filtered_signal)

    def FFT(self, streamflow_data):
        """
        对流量数据进行迭代的傅里叶滤波处理，包括非负值调整和流量总量调整。
        :cutoff_frequency: 傅里叶滤波的截止频率。
        :time_step: 数据采样间隔。
        :iterations: 迭代次数。
        """
        current_signal = streamflow_data.to_numpy().copy()

        for _ in range(self.iterations):
            n = len(current_signal)
            yf = fft(current_signal)
            xf = fftfreq(n, d=self.time_step)

            # Applied frequency filtering
            yf[np.abs(xf) > self.cutoff_frequency] = 0

            # FFT and take the real part
            filtered_signal = ifft(yf).real

            # Apply non-negative constraints
            filtered_signal[filtered_signal < 0] = 0

            # Adjust the total flow to match the original flow
            current_signal = self.data_balanced(streamflow_data, filtered_signal)

        return current_signal

    def wavelet(self, streamflow_data):
        """
        对一维流量数据进行小波变换分析前后拓展数据以减少边缘失真，然后调整总流量。
        :cwt_row: 小波变换中使用的特定宽度。
        """
        streamflow_data_array = streamflow_data.to_numpy().copy()
        # Expand the data edge by 24 lines on each side
        extended_data = np.concatenate(
            [
                np.full(
                    24, streamflow_data_array[0]
                ),  # Expand the first 24 lines with the first element
                streamflow_data,
                np.full(
                    24, streamflow_data_array[-1]
                ),  # Expand the last 24 lines with the last element
            ]
        )
        widths = np.arange(1, 31)
        # Wavelet transform by Morlet wavelet directly
        extended_cwt = cwt(extended_data, morlet, widths)
        scaled_cwtmatr = np.abs(extended_cwt)

        # Select a specific width for analysis (can be briefly understood as selecting a cutoff frequency)
        cwt_row_extended = scaled_cwtmatr[self.cwt_row, :]

        # Remove the extended part
        adjusted_cwt_row = cwt_row_extended[24:-24]
        adjusted_cwt_row[adjusted_cwt_row < 0] = 0
        return self.data_balanced(streamflow_data, adjusted_cwt_row)

    def adaptive_moving_average(
        self,
        streamflow_data,
        threshold=100,
        initial_window=168,
        min_window=24,
        max_window=360,
        decay_factor=2,
    ):
        # 确保输入是 pandas Series
        if not isinstance(streamflow_data, pd.Series):
            raise ValueError("输入的数据必须是 pandas Series")

        # 创建一个与原始数据长度相同的Series
        smoothed_data = pd.Series(index=streamflow_data.index, dtype=float)
        current_window = initial_window

        for i, date in enumerate(streamflow_data.index):
            # 获取当前处理节点的值
            current_value = streamflow_data[date]

            # 调整窗口大小
            if current_value >= threshold:
                current_window = max(min_window, current_window // decay_factor)
            else:
                current_window = min(max_window, current_window * decay_factor)

            half_window = current_window // 2

            # 计算窗口的起始和结束时间，处理边界情况
            if i < half_window:
                start_date = streamflow_data.index[0]
            else:
                start_date = date - pd.DateOffset(hours=half_window)

            if i + half_window >= len(streamflow_data):
                end_date = streamflow_data.index[-1]
            else:
                end_date = date + pd.DateOffset(hours=half_window)

            # 计算窗口内的平均值
            try:
                window_data = streamflow_data[start_date:end_date]
            except KeyError:
                print("WTF")
            smoothed_value = window_data.mean()
            smoothed_data.loc[date] = smoothed_value

        return smoothed_data

    # 使用中心滑动平均处理洪水期间数据
    def update_flood_periods_with_moving_average(
        self, combined_df, flow_division, window_size=1, columns=None
    ):
        for _, row in flow_division.iterrows():
            start_time = row["BEGINNING_FLOW"]
            end_time = row["END_FLOW"]
            mask = (combined_df.index >= start_time) & (combined_df.index <= end_time)
            combined_df.loc[mask, columns] = self.moving_average(
                combined_df.loc[mask, "INQ"], window_size
            )
        return combined_df

    def EMA(self, streamflow_data):
        # 访问时间序列
        df = self.origin_df.copy()

        # streamflow_data数据是插补过的
        df["INQQ"] = np.nan
        df["INQQ"] = streamflow_data

        # 将 'TM' 列转换为日期时间格式
        df["TM"] = pd.to_datetime(df["TM"], errors="coerce")

        # 设置 'TM' 列为索引
        df.set_index("TM", inplace=True)

        # 去重索引，保留最后一个
        df = df[~df.index.duplicated(keep="last")]

        # 分段处理
        # 计算不同窗口的滑动平均
        df["INQA"] = self.adaptive_moving_average(
            df["INQQ"], threshold=200, initial_window=24, min_window=6, max_window=48
        )
        df["INQB"] = self.adaptive_moving_average(
            df["INQQ"], threshold=200, initial_window=168, min_window=48, max_window=336
        )

        # 创建新的INQQ列，根据月份替换数据
        df["INQC"] = np.where(
            df.index.month.isin([5, 6, 7, 8, 9, 10]), df["INQA"], df["INQB"]
        )

        # 处理场次洪水部分
        # flow_division_path = 'biliu_flow_division.csv'  # 洪水场次数据文件路径
        # flow_division = pd.read_csv(flow_division_path)
        # flow_division['BEGINNING_FLOW'] = pd.to_datetime(flow_division['BEGINNING_FLOW'])
        # flow_division['END_FLOW'] = pd.to_datetime(flow_division['END_FLOW'])

        # 更新洪水期间的 INQ 数据
        # df['INQD'] =df['INQC']
        # df = self.update_flood_periods_with_moving_average(df, flow_division,columns = 'INQC', window_size=1)
        # 合并滑动平均结果到 EMA 列
        df["EMA"] = df["INQC"]

        # 进行总量平衡
        df["EMA"] = self.data_balanced(streamflow_data, df["EMA"])

        return df["EMA"]

    def ewma(self, streamflow):
        # 计算 EWMA，指定平滑系数 alpha
        ewma_data = streamflow.ewm(alpha=0.7).mean()
        return self.data_balanced(streamflow, ewma_data)

    def anomaly_process(self, methods=None):
        super().anomaly_process(methods)
        if "INQ" not in self.origin_df.columns:
            if "q" in self.origin_df.columns:
                self.origin_df = self.origin_df.rename(columns={"q": "INQ"})
            elif "inq" in self.origin_df.columns:
                self.origin_df = self.origin_df.rename(columns={"inq": "INQ"})
        self.origin_df["INQ"] = pd.to_numeric(self.origin_df["INQ"], errors="coerce")
        if "TM" not in self.origin_df.columns and "tm" in self.origin_df.columns:
            self.origin_df = self.origin_df.rename(columns={"tm": "TM"})
        self.origin_df["TM"] = pd.to_datetime(self.origin_df["TM"], errors="coerce")
        self.origin_df = self.origin_df.sort_values(by="TM")
        streamflow_data = self.origin_df["INQ"].copy()
        # 使用插值填充缺失值
        streamflow_data = streamflow_data.interpolate().fillna(0)

        for method in methods:
            if method == "moving_average":
                streamflow_data = self.moving_average(streamflow_data=streamflow_data)
            elif method == "kalman":
                streamflow_data = self.kalman_filter(streamflow_data=streamflow_data)
            elif method == "moving_average_diff":
                streamflow_data = self.moving_average_difference(
                    streamflow_data=streamflow_data
                )
            elif method == "robfit":
                streamflow_data = self.robust_fitting(streamflow_data=streamflow_data)
            elif method == "lowpass":
                streamflow_data = self.lowpass_filter(streamflow_data=streamflow_data)
            elif method == "FFT":
                streamflow_data = self.FFT(streamflow_data=streamflow_data)
            elif method == "wavelet":
                streamflow_data = self.wavelet(streamflow_data=streamflow_data)
            elif method == "rolling_mean":
                streamflow_data = self.rolling_with_stride(
                    df=streamflow_data, func=self.adjust_window
                )
                # 确保索引一致
                streamflow_data.index = self.origin_df["INQ"].index
                streamflow_data.fillna(self.origin_df["INQ"], inplace=True)
            elif method == "EMA":
                streamflow_data = self.EMA(streamflow_data=streamflow_data)
                streamflow_data.index = self.origin_df["INQ"].index
            elif method == "ewma":
                streamflow_data = self.ewma(streamflow_data=streamflow_data)

            else:
                print("please check your method name")

        # 新增一列进行存储
        self.processed_df[methods[0]] = streamflow_data

        # 去除提前插补的缺失值
        self.processed_df[methods[0]][self.origin_df["INQ"].isna()] = np.nan
