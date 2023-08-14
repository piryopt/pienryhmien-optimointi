from datetime import datetime, timedelta, timezone

def get_time_helsinki():
    """
    Convert the current time to GMT+3. Pretty sure this is not needed, but might cause problems
    if not implemented.
    """
    now = datetime.now().replace(microsecond=0)
    tz = timezone(timedelta(hours=3))
    helsinki = now.astimezone(tz)
    return helsinki

def time_to_close(time_to_close):
    """
    Check if time now has passed time to close

    Args:
        time_to_close: The date and time when the survey closes
    """
    now = get_time_helsinki()
    tz = timezone(timedelta(hours=3))
    time_to_close = time_to_close.astimezone(tz)
    if time_to_close <= now:
        return True
    return False

