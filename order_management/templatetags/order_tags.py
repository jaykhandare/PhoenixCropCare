from django import template


register = template.Library()

@register.filter(name="format_report")
def format_report(report):
    report['dealer_code'] = report['dealer_profile']['code']
    report.pop('dealer_profile')
    return report