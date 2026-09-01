import re

from django.core.exceptions import ValidationError


PHONE_PATTERN = re.compile(r'^0\d{9}$')
NIN_PATTERN = re.compile(r'^[A-Za-z0-9]{5,20}$')


def clean_text(value, label, min_length=1, max_length=80):
    text = (value or '').strip()
    if not text:
        raise ValidationError(f'{label} is required.')
    if len(text) < min_length:
        raise ValidationError(f'{label} is too short.')
    if len(text) > max_length:
        raise ValidationError(f'{label} is too long.')
    return text


def clean_full_name(value, label='Full name'):
    name = clean_text(value, label, min_length=3, max_length=80)
    if len(name.split()) < 2:
        raise ValidationError('Enter a first name and a last name.')
    return name


def clean_ug_phone(value):
    phone = (value or '').strip().replace(' ', '').replace('-', '')
    if not phone:
        raise ValidationError('Enter a phone number.')
    if not PHONE_PATTERN.match(phone):
        raise ValidationError('Enter a valid Ugandan phone number, for example 0772123456.')
    return phone


def clean_email_address(value):
    email = clean_text(value, 'Email', min_length=5, max_length=80).lower()
    return email


def clean_nin(value):
    nin = clean_text(value, 'NIN', min_length=5, max_length=20).upper()
    if not NIN_PATTERN.match(nin):
        raise ValidationError('Enter a valid NIN using letters and numbers only.')
    return nin
