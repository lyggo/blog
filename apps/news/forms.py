from django import forms
from apps.forms import FormMixin


class AddNewsCommentForm(forms.Form, FormMixin):
    news_id = forms.IntegerField(error_messages={'required': '新闻ID不能为空'})
    content = forms.CharField(error_messages={'required': '新闻评论不能为空'})
    