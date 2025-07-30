def format_time(seconds: float, output_format: str = None) -> str:
    if seconds < 0:
        raise ValueError("Seconds cannot be negative.")
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    if output_format == "hour":
        return f"{seconds / 3600:.2f} hours"
    elif output_format == "minute":
        return f"{seconds / 60:.2f} minutes"
    elif output_format == "hms":
        return f"{hours}h {minutes}m {secs:.2f}s"
    # Default behavior: choose the appropriate unit based on duration
    if seconds >= 3600:
        return f"{hours:.2f} hours"
    elif seconds >= 60:
        return f"{minutes:.2f} minutes"
    else:
        return f"{secs:.2f} seconds"