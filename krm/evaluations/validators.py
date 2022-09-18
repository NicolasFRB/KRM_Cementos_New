from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _


def validate_file_size(value):
    filesize = value.size

    if filesize > 50485760:
        raise ValidationError(_("El tamaño máximo de archivo es de 50MB"))
    else:
        return value
