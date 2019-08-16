import string
import random

from django.utils.text import slugify
from django.utils.crypto import get_random_string


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug, randstr=random_string_generator(size=4))

        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_class_id_generator(instance, new_class_id=None):
    if new_class_id is not None:
        class_id = new_class_id
    else:
        class_id = get_random_string(
            length=6, allowed_chars='abcdefghijklmnopqrstuv0123456789')
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(class_id=class_id).exists()

    if qs_exists:
        new_class_id = get_random_string(
            length=6, allowed_chars='abcdefghijklmnopqrstuv0123456789')
        return unique_class_id_generator(instance, new_class_id=new_class_id)
    return class_id
