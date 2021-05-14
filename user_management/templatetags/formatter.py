from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter(name="format_label")
@stringfilter
def format_label(value):

    if value == "date_of_birth":
        return "DOB"
    if value == "date_of_joining":
        return "Joining"

    if "_" not in value:
        return value.capitalize()

    if value == "exp_first_order":
        return "Expected 1st order"

    if "SD" in value:
        value = value.replace("SD", "Secure-deposit")

    if "_" in value:
        value = " ".join([x.capitalize() for x in value.split("_")])
    return value

# print(format_label("SD_receipt_code"))
