import re


def clean_html(html):
    """Remove html tags from a string"""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', str(html))
    return cleantext

def pluralize(count, singular, plural=None):
    """
    Función de python que nos devuelve una cadena formateada en función
    del número introducido y la forma singular/plural del sustantivo que acompaña
    a la cantidad.
    """
    text= f"{count} {singular}" if count==1 else f"{count} {plural or singular + 's'}"
    return text


