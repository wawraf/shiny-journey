from datetime import datetime


def timestamp(date):
    if is_unix(date):
        return {
            "unix": int(_temp_date.timestamp()),
            "natural": _temp_date.strftime('%d %B %Y')
        }
    elif is_natural(date):
        return {
            "unix": int(_temp_date.timestamp()),
            "natural": _temp_date.strftime("%d %B %Y")
        }
    else:
        return {
            "unix": None,
            "natural": None
        }

def is_unix(date):
    try:
        global _temp_date
        _temp_date = int(date)
        _temp_date = datetime.fromtimestamp(_temp_date)
        return True
    except:
        return False

def is_natural(date):
    try:
        global _temp_date
        _temp_date = datetime.strptime(date, '%B %d, %Y')
        _temp_date.timestamp()
        return True
    except:
        return False


def parse_header(request):
    return {
        "ip"        : request.headers.get("X-Forwarded-For"),
        "language"  : request.headers.get('Accept-Language'),
        "software"  : request.headers.get('User-Agent')
    }