from datetime import datetime


def unix_to_date(timestamp, timezone=7200):
    timestamp += timezone
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')