import random
import string
from django.utils.text import slugify


def random_letters(k=5):
    return ''.join(random.choices(string.ascii_lowercase+string.digits, k=k))

def slugfy_new(string):
    return slugify(string) + '-' + random_letters()