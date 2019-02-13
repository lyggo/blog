from django.shortcuts import render, redirect, reverse
from django.views import View

from utils.alisms.demo_sms_send import send_sms
from .form import LoginForm, RegisterForm
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import  csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from utils.captcha.captcha import Captcha
from io import BytesIO
from utils import mcache
from .models import User
from utils import json_status

@method_decorator([csrf_exempt,], name='dispatch')
class LoginView(View):

    def get(self, request):
        return render(request, 'authPro/login.html')

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone', None)
            password = form.cleaned_data.get('password', None)
            remember = form.cleaned_data.get('remember', None)
            # print(telephone, password)
            # print(remember)
            # print(dir(request.session))
            user = authenticate(username=telephone, password=password)
            if user:
                login(request, user)
                # print(remember)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                    return json_status.result(message='登录成功')
                # return JsonResponse({"code": 0, "msg": "登录成功"})
            # return JsonResponse({"code": 1, "msg": "用户名或密码错误"})
            return json_status.params_error(message='用户名或密码错误')
        return JsonResponse({"code": 1, "msg": form.get_error()})


@method_decorator([csrf_exempt,], name='dispatch')
class RegisterView(View):
    def get(self, request):
        return render(request, 'authPro/register.html')

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid() and form.check_data():
            telephone = form.cleaned_data.get('telephone')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # print('^^^^^^^^^^^^^^^')
            # print(telephone)
            # print(username)
            # print(password)
            # print('^^^^^^^^^^^^^^^')
            user = User.objects.create_user(telephone=telephone, username=username, password=password)
            login(request, user)
            # return JsonResponse({'code': 0, 'msg': '注册成功'})
            return json_status.result(message='注册成功')
        # return JsonResponse({"code": 1, "msg": form.get_error()})
        return json_status.params_error(message=form.get_error())


def logout_view(request):
    logout(request)
    return redirect(reverse("authPro:login"))


def graph_captcha(request):
    text, img = Captcha.gene_code()
    out = BytesIO()
    # 塞管道
    img.save(out, 'png')
    out.seek(0)
    resp = HttpResponse(content_type="image/png")
    resp.write(out.read())
    mcache.set_key(text.lower(), text.lower())
    return resp


def sms_captcha(request):
    # 手机号
    telephone = request.GET.get('telephone')
    # 验证码
    captcha = Captcha.gene_text()
    # 发送短信
    # send_sms(telephone, captcha)
    # 缓存验证码
    ret = mcache.set_key(captcha.lower(), captcha.lower())
    print('手机号 {} 验证码 {}'.format(telephone, captcha))
    # return JsonResponse(str(ret, encoding='utf-8'), safe=False)
    # return JsonResponse({'code': 0})
    return json_status.result(message='验证码发送成功')