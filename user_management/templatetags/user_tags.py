from django import template
from django.template.defaultfilters import stringfilter

from django.core.files.storage import FileSystemStorage


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


@register.filter(name="get_profile_picture")
def get_profile_picture(username):
    fs = FileSystemStorage()
    file_name = './users/' + username + '.png'
    if fs.exists(file_name):
        return fs.url(file_name)
    return fs.url('./users/' + 'profilePic' + '.png')
