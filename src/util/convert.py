from datetime import datetime, timezone, timedelta
import re
from typing import Optional

def parse_pdf_date(date_str: str) -> Optional[datetime]:
    """
    PDF形式の日時文字列 (例: D:20250314051247Z00'00') を datetime に変換する。
    """
    if not date_str.startswith('D:'):
        return None

    date_str = date_str[2:]  # 'D:' を取り除く
    # 正規表現で分解
    match = re.match(r"(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})(Z|([+-])(\d{2})'?(\d{2})'?)?", date_str)
    if not match:
        return None

    year, month, day, hour, minute, second, zulu, offset_sign, offset_hour, offset_minute = match.groups()
    dt = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

    if zulu == 'Z':
        return dt.replace(tzinfo=timezone.utc)
    elif offset_sign and offset_hour and offset_minute:
        offset = timedelta(hours=int(offset_hour), minutes=int(offset_minute))
        if offset_sign == '-':
            offset = -offset
        return dt.replace(tzinfo=timezone(offset))
    else:
        return dt  # タイムゾーンなし