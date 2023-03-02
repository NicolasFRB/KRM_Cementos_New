import re


def clean_html(html):
    """Remove html tags from a string"""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', str(html))
    return cleantext
