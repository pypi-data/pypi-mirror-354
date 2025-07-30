import os
from collections import defaultdict
from pathlib import Path

import soundfile as sf
from typing import Tuple, Dict
from tqdm import tqdm

def analyze_dir(input_dir: os.PathLike)->Tuple[float, Dict[int, int], Dict[str, int]]:
    # 转换为Path对象
    directory_path = Path(input_dir)
    # 确保目录存在
    assert directory_path.is_dir(), f"The provided directory {input_dir} is not a directory."
    
    total_len = 0.0
    sr_count = defaultdict(int)
    bit_count = defaultdict(int)
    bar = tqdm(
        list(directory_path.rglob("**/*.wav")), 
        desc="Analyzing WAV files")
    # 遍历目录及其子目录
    for wav_file in bar:
        # 获取文件信息
        with sf.SoundFile(wav_file) as sound_file:
            duration = len(sound_file) / sound_file.samplerate
            total_len += duration
            # 统计采样率
            sr_count[sound_file.samplerate] += 1
            # 统计位深度
            bit_depth = sound_file.subtype
            bit_count[bit_depth] += 1
    
    return total_len, sr_count, bit_count

