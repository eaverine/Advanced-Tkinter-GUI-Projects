

def get_time_in_minutes_seconds(time_in_seconds):
    minutes = int(time_in_seconds / 60)
    seconds = int(time_in_seconds % 60)
    return (minutes, seconds)

def truncate_text(text, truncate_length):
    truncate_length_plus_two = truncate_length + 2
    return (text[:truncate_length_plus_two] + '..') if len(text) > truncate_length else text
