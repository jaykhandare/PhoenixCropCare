"""
    These functions support view functions and are kept here to keep views.py clean.
"""

from core.template_declarations import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render

from user_management.models import Dealer_Profile


# used to differentiate among employees and authorized dealers
def is_employee(request):
    # returns True if user is an employee
    if request.user.username[-3:] == "404" or not request.user.username:
        return False
    return True


# returns ordered list of fields to be sent through template with or without data
def get_dealer_ordered_list(firm_name=None, managed_by=None, dict_input=None):
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

    # empty list
    if managed_by is not None:
        return ordered_list
    # object to list
    elif firm_name is not None:
        try:
            dealer_obj = Dealer_Profile.objects.get(firm_name=firm_name)
        except Exception as e:
            print(e)
            return None
        else:
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
    # dict to list
    elif dict_input is not None:
        ordered_list[0][1] = dict_input.get("code", "")
        ordered_list[1][1] = dict_input.get("auth_number", "")
        ordered_list[2][1] = dict_input.get("first_name", "")
        ordered_list[3][1] = dict_input.get("last_name", "")
        ordered_list[4][1] = dict_input.get("firm_name", "")
        ordered_list[5][1] = dict_input.get("pd_open_date", "")
        ordered_list[6][1] = dict_input.get("address", "")
        ordered_list[7][1] = dict_input.get("city", "")
        ordered_list[8][1] = dict_input.get("taluka", "")
        ordered_list[9][1] = dict_input.get("district", "")
        ordered_list[10][1] = dict_input.get("state", "")
        ordered_list[11][1] = dict_input.get("pin_code", "")
        ordered_list[12][1] = dict_input.get("contact", "")
        ordered_list[13][1] = dict_input.get("email", "")
        ordered_list[14][1] = dict_input.get("pan_number", "")
        ordered_list[15][1] = dict_input.get("GST_number", "")
        ordered_list[16][1] = dict_input.get("seed_license", "")
        ordered_list[17][1] = dict_input.get("pesticide_license", "")
        ordered_list[18][1] = dict_input.get("fertilizer_license", "")
        ordered_list[19][1] = dict_input.get("SD_receipt_code", "")
        ordered_list[20][1] = dict_input.get("SD_expected", "")
        ordered_list[21][1] = dict_input.get("SD_deposited", "")
        ordered_list[22][1] = dict_input.get("SD_receipt_date", "")
        ordered_list[23][1] = dict_input.get("SD_payment_type", "")
        ordered_list[24][1] = dict_input.get("exp_first_order", "")
        ordered_list[25][1] = dict_input.get("managed_by", "")
        ordered_list[26][1] = dict_input.get("agreement_done", "")
        ordered_list[27][1] = dict_input.get("gift_sent", "")
        ordered_list[28][1] = dict_input.get("authorized", "")
    # error case if no input is provided
    else:
        raise ValueError("no input provided to function{}".format(__name__))

    return ordered_list


# dealer profile data is huge and needs to be added as per availability
# this function save the data and send appropriate response
def save_data_and_respond(request=None, data=None, processing_type=None):
    if data is None or request is None:
        print("incorrect method call in the code.")
        print("Something wrong, I can feel it.")
        return render(request, ERROR_500)

    dealer_obj = None
    if processing_type == "ADD":
        try:
            dealer_obj = Dealer_Profile(
                firm_name=data['firm_name'])
        except Exception as e:
            print(e)
            return render(request, ERROR_500)
    elif processing_type == "EDIT":
        try:
            dealer_obj = Dealer_Profile.objects.get(
                firm_name=data['old_firm_name'])
        except Exception as e:
            print(e)
            return render(request, ERROR_500)

    if data.get('pd_open_date', False):
        dealer_obj.pd_open_date = data['pd_open_date']
    if data.get('SD_receipt_date', False):
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
        dealer_obj.full_clean()
        dealer_obj.save()
    except Exception as error_set:
        print("Error: ", error_set)
        err_response = ""
        for error in error_set:
            err_response += error[0] + " : " + error[1][0] + "</br>"
        dealer_data = get_dealer_ordered_list(dict_input=data)
        return render(request, DEALER_REG_EDIT, {"data": dealer_data, "msg": err_response})

    if data['authorized'] in ["True", "1", 1, True] and len(data['first_name']) != 0 and len(data['last_name']) != 0:
        # create an user profile for dealer if he's authorized
        username = data['first_name'].lower(
        )[0] + data['last_name'].lower() + "404"
        try:
            User.objects.get(username=username)
        except:
            try:
                user_obj = User.objects.create(username=username,
                                               password=make_password(
                                                   username),
                                               first_name=data['first_name'],
                                               last_name=data['last_name'])
                user_obj.full_clean()
                user_obj.save()
            except Exception as error_set:
                print("Error: ", error_set)
                err_response = ""
                for error in error_set:
                    err_response += error[0] + " : " + error[1][0] + "</br>"
                dealer_data = get_dealer_ordered_list(dict_input=data)
                return render(request, DEALER_REG_EDIT, {"data": dealer_data, "msg": err_response})

    msg = "Dealer information added" if processing_type == "ADD" else "Dealer information modified"
    return render(request, DEALER_REG_EDIT, {"msg": msg})
