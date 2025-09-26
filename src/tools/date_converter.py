from datetime import datetime, timedelta, timezone


def time_to_close(time_to_close):
    """
    Check if time now has passed time to close

    Args:
        time_to_close: The date and time when the survey closes
    """

    return time_to_close <= datetime.now()


def format_datestring(input_datetime):
    output_format = "%d.%m.%Y %H:%M"
    try:
        return datetime.strftime(input_datetime, output_format)
    except:
        # To prevent crashing in case a non datetime input is given
        return input_datetime
