import math
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


from krm.utils.models import AuditModel

import hashlib
from random import choice


def random_digits(number_digits=6):
    import random
    digits = [i for i in range(0, 10)]
    random_str = ""
    for i in range(number_digits):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])

    return random_str


def md5_generate(n=20, en_md5=True):
    valores = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<=>@#%&+'
    p = ''
    p = p.join([choice(valores) for i in range(n)])
    if en_md5:
        p = hashlib.md5(p.encode()).hexdigest()
    return p


class User(AbstractUser):
    """User model.

    Extend from Django's Abstract User, change the username field
    to email and add some extra fields.
    """
