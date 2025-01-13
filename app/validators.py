from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

VALID_TLDS = ["com", "net", "org", "edu", "gov", "io", "dev", "co", "us", "eu"]

def validate_domain(domain):
    domain_elements = domain.split(".")
    if len(domain_elements) == 2:
        if domain_elements[-1] in VALID_TLDS:
            return True

    raise ValidationError("Invalid domain")
