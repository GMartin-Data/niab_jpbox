from typing import Optional


def convert_jp_dates(date: str) -> str:
    """Convert JpBox's dates to 'YYYY-MM-DD' format"""
    date = date.split("/")
    return "-".join(reversed(date))


def convert_duration(duration: str) -> Optional[int]:
    """Convert a duration string to its minutes counterpart"""
    if duration is None or not duration.endswith("min"):
        return None
    duration = duration.split()
    hours = int(duration[0].replace("h", ""))
    minutes = int(duration[1].replace("min", ""))
    return (60 * hours + minutes)
