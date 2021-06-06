def min_to_time_str(minutes):
    hours_remaining = minutes // 60
    min_frac_remaining = int(minutes - hours_remaining * 60.0)
    return f'{hours_remaining:02d}:{min_frac_remaining:02d}'
