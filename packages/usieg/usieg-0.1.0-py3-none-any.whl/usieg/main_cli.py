from pathlib import Path

import typer

from usieg.formatter.time_formatter import format_time
from usieg.statistics.audio_len import analyze_dir

app = typer.Typer()



# data_bin = Path("D:\\workspace\\data-bin")


@app.command(name="aulen")
def audio_len(
    input_dir: Path = typer.Argument(..., help="Path to the data-bin directory"),
    output_format: str = typer.Option("hour", help="Output format for the total duration"),
):
    total_len, sr_count, bit_count = analyze_dir(input_dir)
    total_len = format_time(total_len, output_format=output_format)
    print("Total Duration of WAV files (in seconds):", total_len)
    print("\nCount of files by Sampling Rate:")
    for rate, count in sr_count.items():
        print(f"  {rate} Hz: {count} files")
    print("\nCount of files by Bit Depth:")
    for depth, count in bit_count.items():
        print(f"  {depth}: {count} files")

def main():
    app()

