from django import template

register = template.Library()

@register.filter
def add_space_if_decimal(value):
    """
    Formats a number with spaces as thousand separators and limits to two decimal places.
    Returns '-' if the value is None or invalid.
    """
    if value in [None, "", "-"]:  # Handle None or empty values
        return "-"
    try:
        # Format the number with two decimal places and space separators
        return "{:,.2f}".format(float(value)).replace(",", " ")
    except (ValueError, TypeError):
        return "-"


@register.filter
def add_space_if_decimal_zero(value):
    """
    Formats a number with spaces as thousand separators and limits to two decimal places.
    Returns '-' if the value is None or invalid.
    """
    if value in [None, "", "-"]:  # Handle None or empty values
        return "-"
    try:
        # Format the number with two decimal places and space separators
        return "{:,.0f}".format(float(value)).replace(",", " ")
    except (ValueError, TypeError):
        return "-"
