from functions.models import Taxes


def get_taxes_objects():
    if Taxes.objects.count() == 0:
        Taxes.objects.create(name="SGST", rate=0)
        Taxes.objects.create(name="CGST", rate=0)
        Taxes.objects.create(name="IGST", rate=0)

    return Taxes.objects.all()


def get_tax_variables():
    get_taxes_objects()
    SGST = Taxes.objects.get(name="SGST").rate
    CGST = Taxes.objects.get(name="CGST").rate
    IGST = Taxes.objects.get(name="IGST").rate

    return (SGST, CGST, IGST)
