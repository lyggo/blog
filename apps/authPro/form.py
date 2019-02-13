from django import forms
from apps.forms import FormMixin
from utils import mcache


class LoginForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11, min_length=11,
                                error_messages={'min_length': '手机号长度有误', 'max_length': '手机号长度有误',
                                                'required': '手机号不能为空'})
    password = forms.CharField(max_length=20, min_length=6,
                               error_messages={'max_length': '密码最大长度不能超过20', 'min_length': '密码最小长度不能小于6',
                                               'required': '密码不能为空'})
    remember = forms.BooleanField(required=False)


class RegisterForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11, min_length=11,
                                error_messages={'min_length': '手机号长度有误', 'max_length': '手机号长度有误',
                                                'required': '手机号不能为空'})
    password = forms.CharField(max_length=20, min_length=6,
                               error_messages={'max_length': '密码最大长度不能超过20', 'min_length': '密码最小长度不能小于6',
                                               'required': '密码不能为空'})
    sms_captcha = forms.CharField(max_length=4, min_length=4,
                                  error_messages={'max_length': '短信验证码长度有误', 'min_length': '短信验证码长度有误',
                                                  'required': '短信验证码不能为空'})
    password_repeat = forms.CharField(max_length=20, min_length=6,
                                      error_messages={'max_length': '密码最大长度不能超过20', 'min_length': '密码最小长度不能小于6',
                                                      'required': '密码不能为空'})
    username = forms.CharField(max_length=50, min_length=2,
                               error_messages={'max_length': '用户名过长', 'min_length': '用户名过短', 'required': '用户名不能为空'})
    graph_captcha = forms.CharField(max_length=4, min_length=4,
                                    error_messages={'max_length': '图形验证码长度有误', 'min_length': '图形验证码长度有误',
                                                    'required': '图形验证码不能为空'})


    def check_data(self):
        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')
        if password != password_repeat:
            return self.add_error('password', '两次密码不一致')
        # 短信验证码
        sms_captcha = self.cleaned_data.get('sms_captcha')
        sms_captcha_cache = mcache.get_key(sms_captcha)
        print('=============')
        print(sms_captcha)
        print(sms_captcha_cache)
        print('=============')
        if not sms_captcha_cache and sms_captcha != sms_captcha_cache:
            return self.add_error('sms_captcha', '短信验证码有误')
        # 图形验证码
        graph_captcha = self.cleaned_data.get('graph_captcha')
        graph_captcha_cache = mcache.get_key(graph_captcha)
        print('*************')
        print(graph_captcha)
        print(graph_captcha_cache)
        print('*************')
        if not graph_captcha_cache and graph_captcha != graph_captcha_cache:
            return self.add_error('graph_captcha', '图形验证码有误')

        # 默认False
        return True