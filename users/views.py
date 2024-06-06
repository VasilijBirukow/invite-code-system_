import re

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse

from .models import User, InviteCode
from .utils import get_letters_numbers, fill_random


def main_page(request):
    return render(request, 'users/home.html')


def auth_page(request):
    return render(request, 'users/auth.html')


def auth_function(request):
    phone = re.sub(r'[^0-9]', '', str(request.GET.get('phone')))
    is_valid = check_valid(phone)
    if not is_valid:
        return HttpResponse('Номер не корректен', status=400)

    absent_user = check_absent_user(phone)
    if absent_user:
        create_user(phone)

    return HttpResponse(status=200)


def check_valid(phone: str) -> bool:
    if len(phone) != 11:
        return False

    if phone[0] != '7' and phone[0] != '8':
        return False

    return True


def check_absent_user(phone):
    return not User.objects.filter(number=phone).exists()


def create_user(phone):
    generated_code = create_invite_code()

    user = User(number=phone, generated_code=generated_code, applied_code=None)
    user.save()

    return user


def create_invite_code():
    invite_code = InviteCode(code=get_invite_code())
    invite_code.save()

    return invite_code


def get_invite_code() -> str:
    code = generated_invite_code()
    while not absent_invite_code(code):
        code = generated_invite_code()
    return code


def generated_invite_code():
    code = f"rf{fill_random(get_letters_numbers(), 4)}"
    return code


def absent_invite_code(code) -> bool:
    return not InviteCode.objects.filter(code=code).exists()


def profile_page(request):
    phone = request.GET.get('phone')
    return render(request, 'users/profile.html', {'phone': phone})


def get_date_user(request):
    phone = request.GET.get('phone')
    response = get_user_data_dict(phone)
    return JsonResponse(response)


def make_standard_phones(phone_list: list):
    result_list = list()
    for phone in phone_list:
        result_list.append(standard_phone(phone))
    return result_list


def get_user_data_dict(phone):
    user = get_user_by_phone(phone)
    generated_code_id = user.get('generated_code')
    phone_list = get_users_login_by_invite_code(generated_code_id)
    phone_list = make_standard_phones(phone_list)
    data = UserResponseDTO(user, phone_list)
    data_dict = data.__dict__
    data_dict['user']['number'] = standard_phone(data_dict['user']['number'])
    return data_dict


def get_user_by_phone(phone, dict_type=True):
    try:
        if dict_type is True:
            return model_to_dict(User.objects.get(number=phone))
        else:
            return User.objects.get(number=phone)
    except ObjectDoesNotExist:
        print(f"User {phone} не существует")
    except MultipleObjectsReturned:
        print(f"Найдено более одного объекта {phone}")


def get_user_by_code_id(code_id):
    return User.objects.filter(generated_code=code_id).first()


def get_users_login_by_invite_code(invite_code):
    return list(User.objects
                .filter(applied_code=invite_code)
                .values_list('number', flat=True))


def get_invite_code_by_id(code_id):
    return InviteCode.objects.get(id=code_id)


def get_invite_code_by_code(code):
    return InviteCode.objects.get(code=code)


def update_user_applied_code(code, phone):
    invite_code = get_invite_code_by_code(code)
    user = get_user_by_phone(phone, dict_type=False)
    user.applied_code = invite_code
    user.save()


def replace_code_by_id(user: dict, generated=True):
    field_name: str
    if generated is True:
        field_name = 'generated_code'
    else:
        field_name = 'applied_code'
    code_id = user[field_name]
    code = get_invite_code_value(code_id)
    if code:
        user.update({field_name: code})
    else:
        pass


def get_invite_code_value(code_id):
    invite_code = InviteCode.objects.filter(id=code_id).first()
    if invite_code:
        return invite_code.code
    else:
        return None


def delete_user_id(user: dict):
    del user['id']


class UserResponseDTO:
    def __init__(self, user, users_login_list):
        self.user = user
        self.users_login_list = users_login_list
        delete_user_id(user)
        replace_code_by_id(user, generated=True)
        replace_code_by_id(user, generated=False)

    def __str__(self):
        return f"UserResponseDTO(user={self.user}, users_login_list={self.users_login_list})"


def check_applied_code(request):
    code = request.GET.get('code')
    phone = request.GET.get('phone')
    if check_valid_invite_code(code, phone):
        update_user_applied_code(code, phone)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


def check_valid_invite_code(code, phone):
    user = get_user_by_phone(phone)
    generated_code_object = get_invite_code_by_id(user['generated_code'])
    return code[:2] == "rf" and code != generated_code_object.code and not absent_invite_code(code)


def standard_phone(phone: int) -> str:
    return f"+7 ({phone[1:4]}) {phone[4:7]}-{phone[7:9]}-{phone[9:11]}"
