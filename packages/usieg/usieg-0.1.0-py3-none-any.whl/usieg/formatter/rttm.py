from pathlib import Path
from typing import Any, Tuple, List

import numpy as np
import pandas as pd


def read_rttm(rttm: Path) -> List[pd.DataFrame]:
    # 读取 RTTM 文件
    df = pd.read_csv(rttm, delimiter=" ", header=None)

    # 为列命名
    df.columns = [
        "type",
        "file",
        "channel",
        "start",
        "duration",
        "NA1",
        "NA2",
        "NA3",
        "NA4",
    ]
    df["end"] = df["start"] + df["duration"]
    # 去除不必要的列 (NA1, NA2, NA3, NA4)
    df = df.drop(columns=["NA1", "NA2", "NA3", "NA4"])

    # 按文件名进行分组
    grouped = df.groupby("file")

    # 按照文件名对分组进行排序，并存储每个文件的 DataFrame
    sorted_files = sorted(grouped, key=lambda x: x[0])

    # 将每个分组的数据存储为一个 DataFrame，并返回一个 DataFrame 列表
    df_list = [group.reset_index(drop=True) for _, group in sorted_files]

    return df_list


def rttm_to_seconds(
    df: pd.DataFrame,
) -> Tuple[np.ndarray, np.ndarray]:

    start_seconds = df["start"].to_numpy()
    duration_seconds = df["duration"].to_numpy()

    return start_seconds, duration_seconds
