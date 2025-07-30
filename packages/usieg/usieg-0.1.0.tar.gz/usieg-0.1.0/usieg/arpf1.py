from pathlib import Path
from typing import Union, List

import numpy as np

from usieg.formatter.audition import seconds_to_mask
from usieg.formatter.rttm import read_rttm, rttm_to_seconds


def get_TFPN(model_mask: np.ndarray, label_mask: np.ndarray):
    # Ensure that both masks are boolean type
    model_mask = model_mask.astype(bool)
    label_mask = label_mask.astype(bool)
    # True Positive (TP): model predicted True and label is True
    TP = np.sum(np.logical_and(model_mask, label_mask))
    # True Negative (TN): model predicted False and label is False
    TN = np.sum(np.logical_and(np.logical_not(model_mask), np.logical_not(label_mask)))
    # False Positive (FP): model predicted True but label is False
    FP = np.sum(np.logical_and(model_mask, np.logical_not(label_mask)))
    # False Negative (FN): model predicted False but label is True
    FN = np.sum(np.logical_and(np.logical_not(model_mask), label_mask))

    return TP, FP, TN, FN


def TFPN_to_ARPF1(TP, FP, TN, FN):
    # Accuracy (A): (TP + TN) / (TP + TN + FP + FN)
    A = float((TP + TN) / (TP + TN + FP + FN))
    A = round(A, 4)
    # Recall (R): TP / (TP + FN)
    R = float(TP / (TP + FN)) if (TP + FN) > 0 else 0.0
    R = round(R, 4)
    # Precision (P): TP / (TP + FP)
    P = float(TP / (TP + FP)) if (TP + FP) > 0 else 0.0
    P = round(P, 4)
    # F1 Score (F1): 2 * (P * R) / (P + R)
    F1 = float(2 * (P * R) / (P + R)) if (P + R) > 0 else 0.0
    F1 = round(F1, 4)

    return A, R, P, F1


def get_ARPF1(model_mask: np.ndarray, label_mask: np.ndarray):
    TP, FP, TN, FN = get_TFPN(model_mask, label_mask)

    return TFPN_to_ARPF1(TP, FP, TN, FN)


def from_rttm(
    model_rttm_path: List[Union[str, Path]],
    label_rttm_path: List[Union[str, Path]],
    sr: int = 16000,
):
    # 读取，按文件名文组
    if isinstance(label_rttm_path, str):
        label_rttm_path = Path(label_rttm_path)
    if isinstance(model_rttm_path, str):
        model_rttm_path = Path(model_rttm_path)
    model_dfs = read_rttm(model_rttm_path)
    label_dfs = read_rttm(label_rttm_path)

    results = []
    signal_lens = []
    results_tfpn = {
        "TP": 0,
        "FP": 0,
        "TN": 0,
        "FN": 0,
    }
    for model_df, label_df in zip(model_dfs, label_dfs):
        label_starts, label_durations = rttm_to_seconds(label_df)
        model_starts, model_durations = rttm_to_seconds(model_df)
        signal_length = int(max(label_df["end"].max(),model_df["end"].max())* sr)
        signal_lens.append(signal_length)
        label_mask = seconds_to_mask(label_starts, label_durations, signal_length, sr)
        model_mask = seconds_to_mask(model_starts, model_durations, signal_length, sr)
        tp, fp, tn, fn = get_TFPN(model_mask, label_mask)
        results_tfpn["TP"] += tp
        results_tfpn["FP"] += fp
        results_tfpn["TN"] += tn
        results_tfpn["FN"] += fn
        result = TFPN_to_ARPF1(tp, fp, tn, fn)
        results.append(
            {
                "Path": Path(label_df["file"].iloc[0]).name,
                "A": result[0],
                "R": result[1],
                "P": result[2],
                "F1": result[3],
                "LEN": signal_length/sr,
            }
        )
    total_result = TFPN_to_ARPF1(
        results_tfpn["TP"],
        results_tfpn["FP"],
        results_tfpn["TN"],
        results_tfpn["FN"],
    )
    results.append(
        {
            "Path": "<Total>",
            "A": total_result[0],
            "R": total_result[1],
            "P": total_result[2],
            "F1": total_result[3],
            "LEN": sum(signal_lens)/sr,
        }
    )
    return results
    # return get_ARPF1(model_mask, label_mask)
