from django import template
from django.utils.timezone import now
from datetime import datetime

register = template.Library()


@register.filter
def date_format(val):
    # 判断是否时间类型
    if not isinstance(val, datetime):
        return val
    # 获取发布时间
    time_new = now()
    # 相减 时间戳 转 秒
    sec = (time_new-val).total_seconds()
    # 秒 转 刚刚 一天前
    if sec < 60:
        return '刚刚'
    elif 60 <= sec < 60*60:
        mint = int(sec / 60)
        return '{}分钟前'.format(mint)
    elif 60*60 <= sec < 60*60*24:
        hour = int(sec / 60 / 60)
        return '{}小时前'.format(hour)
    elif 60*60*24 <= sec < 60*60*24*30:
        day = int(sec / 60 / 60 / 24)
        return '{}天前'.format(day)
    else:
        return val.strftime('%Y-%m-%d %H:%M')



