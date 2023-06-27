import math

def format_stopwatch(total_seconds):

    total_minutes = math.floor(total_seconds/60)
    total_hours = math.floor(total_minutes/60)

    days = int(math.floor(total_hours/24))
    hours = int(total_hours - days*24)
    minutes = int(total_minutes - total_hours*60)
    seconds = int(total_seconds - total_minutes*60)

    if days > 0:
        return "{:d}.{:02d}:{:02d}:{:02d}".format(days, hours, minutes, seconds)
    else:
        return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)