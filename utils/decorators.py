from functools import wraps
from .json_status import un_auth_error
from django.shortcuts import redirect, reverse


def ajax_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request,*args, **kwargs)
        else:
            if request.is_ajax():
                return un_auth_error(message='请先登录')
            return redirect(reverse('/authPro/login/'))
    return wrapper
