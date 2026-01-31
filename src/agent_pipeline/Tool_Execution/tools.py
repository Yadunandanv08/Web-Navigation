import datetime

def get_dateTime():
    """Get the current date and time as a formatted string."""
    return datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

def get_age(birth_date):
    """
    Calculate age from a birth date.

    Args:
        birth_date: The birth date in ISO 8601 format (YYYY-MM-DDTHH:MM:SS).
    """
    if isinstance(birth_date, str):
        birth_date = datetime.datetime.fromisoformat(birth_date)
    today = datetime.datetime.now()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age