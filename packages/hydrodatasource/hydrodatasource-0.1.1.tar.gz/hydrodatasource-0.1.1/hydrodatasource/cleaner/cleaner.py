"""
Author: liutiaxqabs 1498093445@qq.com
Date: 2024-04-19 13:58:31
LastEditors: Wenyu Ouyang
LastEditTime: 2025-01-15 11:21:50
FilePath: \hydrodatasource\hydrodatasource\cleaner\cleaner.py
Description: 
    cleaner/
    │
    ├── __init__.py
    ├── cleaner.py          # 包含 Cleaner 基类
    ├── rainfall_cleaner.py # 包含 RainfallCleaner 类
    ├── rsvr_inflow_cleaner.py # 包含 ReservoirInflowBacktrack 类
    ├── streamflow_cleaner.py # 包含 StreamflowCleaner 类
    └── waterlevel_cleaner.py # 包含 WaterlevelCleaner 类
"""


class Cleaner:
    def __init__(self, data_folder, *args, **kwargs):
        self.data_path = data_folder
        self.read_data()

    def read_data(self):
        # 读取数据并存储在origin_df中
        pass

    def save_data(self, data, output_path):
        # 保存数据到CSV
        pass

    def anomaly_process(self, methods=None):
        if methods is None:
            methods = []
        # 如果有特定流程，可以在这里添加
        pass
