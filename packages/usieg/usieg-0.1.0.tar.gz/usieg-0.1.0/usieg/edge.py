from pathlib import Path
from typing import Tuple, Union
import pandas as pd
import numpy as np

from usieg.formatter.rttm import read_rttm, rttm_to_seconds
from dataclasses import dataclass


@dataclass
class EdgeEror:
    avg_error: float
    successful: int
    failed: int
    total: int
    errors: np.ndarray


def hungarian_algorithm(cost_matrix):
    """
    实现匈牙利算法（Kuhn-Munkres算法）来解决加权二分图的最小权匹配问题。

    参数：
    - cost_matrix: 方阵代价矩阵，形状为 (n, n)

    返回：
    - assignments: 列表，包含每个匹配的 (行索引, 列索引)
    """
    m = cost_matrix.copy()
    n = m.shape[0]

    # Step 1: 行减
    for i in range(n):
        m[i] -= m[i].min()

    # Step 2: 列减
    for j in range(n):
        m[:, j] -= m[:, j].min()

    # 初始化标记
    zero_mask = m == 0
    row_covered = np.zeros(n, dtype=bool)
    col_covered = np.zeros(n, dtype=bool)
    starred_zeros = np.zeros_like(m, dtype=bool)
    primed_zeros = np.zeros_like(m, dtype=bool)

    # Step 3: 标记初始的星号零
    for i in range(n):
        for j in range(n):
            if zero_mask[i, j] and not row_covered[i] and not col_covered[j]:
                starred_zeros[i, j] = True
                row_covered[i] = True
                col_covered[j] = True

    row_covered[:] = False
    col_covered[:] = False

    while True:
        # Step 4: 覆盖每列中有星号零的列
        for j in range(n):
            if starred_zeros[:, j].any():
                col_covered[j] = True

        # 检查是否已找到完美匹配
        if col_covered.sum() >= n:
            break

        # Step 5: 寻找未覆盖的零，进行标记
        while True:
            zero_positions = np.argwhere(
                (zero_mask) & (~row_covered[:, None]) & (~col_covered)
            )
            if zero_positions.size == 0:
                # Step 6: 调整矩阵
                min_uncovered = m[~row_covered[:, None], ~col_covered].min()
                m[~row_covered[:, None], ~col_covered] -= min_uncovered
                m[row_covered[:, None], col_covered] += min_uncovered
                zero_mask = m == 0
            else:
                row, col = zero_positions[0]
                primed_zeros[row, col] = True
                star_col = np.argwhere(starred_zeros[row]).flatten()
                if star_col.size == 0:
                    # Step 7: 构造交替零序列并调整星号零
                    path = [(row, col)]
                    while True:
                        star_row = np.argwhere(starred_zeros[:, col]).flatten()
                        if star_row.size == 0:
                            break
                        row = star_row[0]
                        path.append((row, col))
                        col = np.argwhere(primed_zeros[row]).flatten()[0]
                        path.append((row, col))
                    for r, c in path:
                        starred_zeros[r, c] = not starred_zeros[r, c]
                    primed_zeros[:] = False
                    row_covered[:] = False
                    col_covered[:] = False
                    break
                else:
                    row_covered[row] = True
                    col_covered[star_col[0]] = False

    # 最终分配
    assignments = []
    for i in range(n):
        j = np.argwhere(starred_zeros[i]).flatten()
        if j.size > 0:
            assignments.append((i, j[0]))
    return assignments


def match_edges(labels_indices, vad_indices, threshold=5):
    n_labels = len(labels_indices)
    n_vad = len(vad_indices)
    n = max(n_labels, n_vad)  # 取较大值，构建方阵

    large_value = 1e6  # 一个足够大的值，表示无限大

    # 构建方阵代价矩阵，初始化为 large_value
    cost_matrix = np.full((n, n), large_value)

    # 填充实际的代价
    for i in range(n_labels):
        for j in range(n_vad):
            error = abs(labels_indices[i] - vad_indices[j])
            if error <= threshold:
                cost_matrix[i, j] = error

    # 调用匈牙利算法获取最优匹配
    assignments = hungarian_algorithm(cost_matrix)

    # 准备输出结果
    matched_vad_indices = np.full(n_labels, -1, dtype=int)
    errors = np.full(n_labels, -1, dtype=int)

    for i, j in assignments:
        # 仅处理真实的 labels_indices 和 vad_indices 范围内的匹配
        if i < n_labels and j < n_vad:
            error = abs(labels_indices[i] - vad_indices[j])
            if error <= threshold and cost_matrix[i, j] < large_value:
                matched_vad_indices[i] = vad_indices[j]
                errors[i] = int(error)
            else:
                # 超过阈值或代价过大，不进行匹配
                pass

    return matched_vad_indices, errors


def get_edge_error(
    m_edges: np.ndarray,
    l_edges: np.ndarray,
    sr: int = 16000,
    threshold: float = 0.5,
) -> EdgeEror:
    # 进行匹配
    matched_edges, edge_errors = match_edges(m_edges, l_edges, threshold)
    # 计算匹配成功和失败的数量
    edge_successful = np.sum(edge_errors >= 0)
    edge_failed = len(edge_errors) - edge_successful
    # 总段数（标签）
    total_label_segments = len(l_edges)
    # 计算平均误差（排除匹配失败的）
    edge_errors_clean = edge_errors[edge_errors >= 0]
    edge_avg_error = (
        edge_errors_clean.mean() / sr if len(edge_errors_clean) > 0 else None
    )
    return EdgeEror(
        avg_error=edge_avg_error,
        successful=edge_successful,
        failed=edge_failed,
        total=total_label_segments,
        errors=edge_errors_clean,
    )
    # return edge_errors, edge_successful, edge_failed, total_label_segments, edge_avg_error


def from_rttm(
    model_rttm_path: Union[Path, str],
    label_rttm_path: Union[Path, str],
    sr: int = 16000,
    threshold_s: float = 0.5,
) -> pd.DataFrame:
    # 转换参数

    model_rttm_dfs = read_rttm(Path(model_rttm_path))
    label_rttm_dfs = read_rttm(Path(label_rttm_path))
    threshold = int(threshold_s * sr)
    results = []
    # for model_df in model_rttm_dfs:
    for model_df, label_df in zip(model_rttm_dfs, label_rttm_dfs):
        # 转换为索引
        m_starts, m_durations = rttm_to_seconds(model_df)
        m_starts = np.round(m_starts * sr).astype(int)
        l_starts, l_durations = rttm_to_seconds(label_df)
        l_starts = np.round(l_starts * sr).astype(int)
        # 上升沿误差
        start_result = get_edge_error(m_starts, l_starts, sr, threshold)
        # 计算结束位置的索引
        m_ends = m_starts + m_durations
        m_ends = np.round(m_ends * sr).astype(int)
        l_ends = l_starts + l_durations
        l_ends = np.round(l_ends * sr).astype(int)
        # 下降沿误差
        end_result = get_edge_error(m_ends, l_ends, sr, threshold)
        # result = get_edge_error(model_df, label_df, sr, threshold)
        total_errors = np.concatenate([start_result.errors, end_result.errors])
        total_errors_clean = total_errors[total_errors >= 0]
        total_avg_error = (
            total_errors_clean.mean() / sr if len(total_errors_clean) > 0 else None
        )
        result = {
            "path": Path(label_df["file"].iloc[0]).name,
            "avg_error": total_avg_error,
            "start_avg_error": start_result.avg_error,
            "end_avg_error": end_result.avg_error,
            "s_starts": start_result.successful,
            "f_starts": start_result.failed,
            "starts": start_result.total,
            "s_ends": end_result.successful,
            "f_ends": end_result.failed,
            "ends": end_result.total,
        }
        results.append(result)
    df = pd.DataFrame(results)
    return df
