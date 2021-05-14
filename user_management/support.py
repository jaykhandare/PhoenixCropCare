"""
    These functions support view functions and are kept here to keep views.py clean.
"""

from user_management.models import User_Profile, Dealer_Profile
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User



# used to differentiate among employees and authorized dealers
def is_staff(request):
    # returns True if user is an employee
    if request.user.username[-3:] == "404":
        return False
    return True


# this creates initial empty profile for employee
def initiate_user_profile(username):
    try:
        User_Profile.objects.create(username=username)
    except Exception as e:
        print(e)
        return False
    else:
        print("user profile added: {}".format(username))
        return True


# returns ordered list of fields to be sent through template with or without data
def get_dealer_ordered_list(firm_name=None, managed_by=None):
    ordered_list = [
        ['code', ""], ['auth_number', ""],
        ['first_name', ""], ['last_name', ""],
        ['firm_name', ""], ['pd_open_date', ""],
        ['address', ""], ['city', ""],
        ['taluka', ""], ['district', ""],
        ['state', ""], ['pin_code', ""],
        ['contact', ""], ['email', ""],
        ['pan_number', ""], ['GST_number', ""],
        ['seed_license', ""], ['pesticide_license', ""],
        ['fertilizer_license', ""], ['SD_receipt_code', ""],
        ['SD_expected', ""], ['SD_deposited', ""],
        ['SD_receipt_date', ""], ['SD_payment_type', ""],
        ['exp_first_order', ""], ['managed_by', managed_by],
        ['agreement_done', ""], ['gift_sent', ""],
        ['authorized', ""]]

    if firm_name is None:
        return ordered_list
    else:
        try:
            dealer_obj = Dealer_Profile.objects.get(firm_name=firm_name)
        except Exception as e:
            print(e)
            return None

        ordered_list[0][1] = dealer_obj.code
        ordered_list[1][1] = dealer_obj.auth_number
        ordered_list[2][1] = dealer_obj.first_name
        ordered_list[3][1] = dealer_obj.last_name
        ordered_list[4][1] = dealer_obj.firm_name
        ordered_list[5][1] = dealer_obj.pd_open_date
        ordered_list[6][1] = dealer_obj.address
        ordered_list[7][1] = dealer_obj.city
        ordered_list[8][1] = dealer_obj.taluka
        ordered_list[9][1] = dealer_obj.district
        ordered_list[10][1] = dealer_obj.state
        ordered_list[11][1] = dealer_obj.pin_code
        ordered_list[12][1] = dealer_obj.contact
        ordered_list[13][1] = dealer_obj.email
        ordered_list[14][1] = dealer_obj.pan_number
        ordered_list[15][1] = dealer_obj.GST_number
        ordered_list[16][1] = dealer_obj.seed_license
        ordered_list[17][1] = dealer_obj.pesticide_license
        ordered_list[18][1] = dealer_obj.fertilizer_license
        ordered_list[19][1] = dealer_obj.SD_receipt_code
        ordered_list[20][1] = dealer_obj.SD_expected
        ordered_list[21][1] = dealer_obj.SD_deposited
        ordered_list[22][1] = dealer_obj.SD_receipt_date
        ordered_list[23][1] = dealer_obj.SD_payment_type
        ordered_list[24][1] = dealer_obj.exp_first_order
        ordered_list[25][1] = dealer_obj.managed_by
        ordered_list[26][1] = dealer_obj.agreement_done
        ordered_list[27][1] = dealer_obj.gift_sent
        ordered_list[28][1] = dealer_obj.authorized
        return ordered_list


# dealer profile data is huge and needs to be added as per availability
# this function save the data and send appropriate response
def save_data_and_respond(request=None, data=None, processing_type=None):
    if data is None or request is None:
        print("incorrect method call in the code.")
        print("Something wrong, I can feel it.")
        return render(request, "custom_templates/page-500.html")
    """
    # this weird logic is used to avoid following scenario errors
        dealer(firm_name) is already edited and saved, but user hits refresh button
        so it send a GET request with firm_name set to old firm_name
        in objects.get, this is not found, so goes to except
        there tries to create a new object with new firm_name which is already there in db
        firm_name is unique so fails there and thows UNIQUE constraint failed error to user

    # this needs to be taken care of later
    """
    msg = "Dealer details updated"
    try:
        dealer_obj = Dealer_Profile.objects.get(
            firm_name=data['old_firm_name'])
    except Exception as e:
        try:
            dealer_obj = Dealer_Profile.objects.create(
                firm_name=data['firm_name'])
        except Exception as e:
            dealer_obj = Dealer_Profile.objects.get(
                firm_name=data['firm_name'])
        else:
            msg = "Dealer details added"

    if data['pd_open_date']:
        dealer_obj.pd_open_date = data['pd_open_date']
    if data['SD_receipt_date']:
        dealer_obj.SD_receipt_date = data['SD_receipt_date']

    dealer_obj.firm_name = data['firm_name']
    dealer_obj.code = data['code']
    dealer_obj.auth_number = data['auth_number']
    dealer_obj.first_name = data['first_name']
    dealer_obj.last_name = data['last_name']
    dealer_obj.address = data['address']
    dealer_obj.city = data['city']
    dealer_obj.taluka = data['taluka']
    dealer_obj.district = data['district']
    dealer_obj.state = data['state']
    dealer_obj.pin_code = data['pin_code']
    dealer_obj.contact = data['contact']
    dealer_obj.email = data['email']
    dealer_obj.pan_number = data['pan_number']
    dealer_obj.GST_number = data['GST_number']
    dealer_obj.seed_license = data['seed_license']
    dealer_obj.pesticide_license = data['pesticide_license']
    dealer_obj.fertilizer_license = data['fertilizer_license']
    dealer_obj.SD_receipt_code = data['SD_receipt_code']
    dealer_obj.SD_expected = data['SD_expected']
    dealer_obj.SD_deposited = data['SD_deposited']
    dealer_obj.SD_payment_type = data['SD_payment_type']
    dealer_obj.exp_first_order = data['exp_first_order']
    dealer_obj.managed_by = data['managed_by']
    dealer_obj.agreement_done = data['agreement_done']
    dealer_obj.gift_sent = data['gift_sent']
    dealer_obj.authorized = data['authorized']

    try:
        dealer_obj.save()
    except Exception as e:
        print("Exception: ", e)
        return render(request, "custom_templates/page-500.html")
    else:
        if data['authorized'] in ["True", "1", 1, True]:
            # create an user profile for dealer if he's authorized
            if not create_dealer_user_profile(data):
                return render(request, "custom_templates/page-500.html")

        return render(request, "dealers/basic_form.html", {"msg": msg})


# used to create a basic user profile when the dealer is authorized
def create_dealer_user_profile(data):
    username = data['first_name'].lower(
    )[0] + data['last_name'].lower() + "404"
    try:
        User.objects.create(username=username,
                            password=make_password(username))
    except Exception as e:
        print(e)
        return False
    return True
