from typing import Dict
from django.core.paginator import EmptyPage
from rest_framework.exceptions import ValidationError


def responsedata(status, message, data=None):
    if status:
        return {"status": status, "message": message, "data": data}
    else:
        return {
            "status": status,
            "message": message,
        }


def paginate(data, paginator, pagenumber):
    """
    This method to create the paginated results in list API views.
    """

    if int(pagenumber) > paginator.num_pages:
        raise ValidationError("Not enough pages", code=404)
    try:
        previous_page_number = paginator.page(
            pagenumber).previous_page_number()
    except EmptyPage:
        previous_page_number = None
    try:
        next_page_number = paginator.page(pagenumber).next_page_number()
    except EmptyPage:
        next_page_number = None

    return {
        'pagination': {
            'previous_page': previous_page_number,
            'is_previous_page': paginator.page(pagenumber).has_previous(),
            'next_page': next_page_number,
            'is_next_page': paginator.page(pagenumber).has_next(),
            'start_index': paginator.page(pagenumber).start_index(),
            'end_index': paginator.page(pagenumber).end_index(),
            'total_entries': paginator.count,
            'total_pages': paginator.num_pages,
            'page': int(pagenumber)
        },
        'results': data
    }


def url_validator(value):
    """A custom method to validate any website url """

    import re
    regex = re.compile(
        r'^https?://|www\.|https?://www\.'  # http:// or https:// or www.
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  #domain...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$',
        re.IGNORECASE)
    if value and not regex.match(value):
        raise AssertionError("Please enter a valid website URL")
    return value


def stringify_error_message(message: Dict) -> str:
    _str = ""
    for key in message:
        _str += "\n".join(f"{key}-{msg}" for msg in message[key]) + "\n "

    return _str.rstrip()
