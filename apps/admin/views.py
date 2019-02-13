import os
from django.contrib.admin.views.decorators import staff_member_required
from django.http import QueryDict
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from tanzhou_django_project import settings
from utils import json_status
from apps.news.models import NewsTag, News, NewsHot,NewsBanner
from qiniu import Auth
from django.http import JsonResponse
from .form import NewsPubForm, NewsHotAddForm, NewsBannerForm
from utils.decorators import ajax_login_required
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from urllib.parse import urlencode

# 必须是员工才可以访问
@staff_member_required(login_url='/authPro/login/')
def index(request):
    return render(request, 'admin/base/index.html')

@method_decorator([csrf_exempt, staff_member_required(login_url='/authPro/login/')], name='dispatch')
class NewsTagView(View):
    def get(self, request):
        news_tags = NewsTag.objects.filter(is_delete=True).all()
        return render(request, 'admin/news/news_tag_manage.html',
                      context={'news_tag': news_tags})

    def post(self, request):
        name = request.POST.get('name')
        if name and bool(name.strip()):
            # exists() 是否存在
            news_tag_exists = NewsTag.objects.filter(name=name).exists()
            if news_tag_exists:
                return json_status.params_error(message='该标签已存在,请不要重复输入')
            NewsTag.objects.create(name=name)
            return json_status.result(message='成功')
        return json_status.params_error(message='标签名不能为空')


    def put(self, request):
        res = QueryDict(request.body)
        tag_name = res.get('tag_name', None)
        tag_id = res.get('tag_id', None)
        if tag_id and tag_name:
            tag = NewsTag.objects.filter(id=tag_id)
            if tag:
                news_tag_exists = NewsTag.objects.filter(name=tag_name).exists()
                if news_tag_exists:
                    return json_status.params_error(message='该标签已存在,请不要重复输入')
                tag.update(name=tag_name)
                return json_status.result()
            return json_status.params_error(message='标签不存在')
        return json_status.params_error(message='标签不存在')


    def delete(self, request):
        res = QueryDict(request.body)
        tag_id = res.get('tag_id', None)
        tag = NewsTag.objects.filter(id=tag_id)
        if tag_id and tag:
            tag.update(is_delete=False)
            return json_status.result()
        return json_status.params_error(message='标签不存在')

@method_decorator([csrf_exempt, staff_member_required(login_url='/authPro/login/')], name='dispatch')
class NewsPubView(View):
    def get(self, request):
        news_tags = NewsTag.objects.filter(is_delete=True).all()
        return render(request, 'admin/news/news_pub.html',
                      context={'news_tags': news_tags})

    def post(self, request):
        form = NewsPubForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            tag_id = form.cleaned_data.get('tag_id')
            thumbnail_url = form.cleaned_data.get('thumbnail_url')
            content = form.cleaned_data.get('content')
            tag = NewsTag.objects.get(id=tag_id)
            if tag:
                News.objects.create(title=title, desc=desc, tag=tag, thumbnail_url=thumbnail_url, content=content, author=request.user)
                return json_status.result()
            return json_status.params_error(message='标签不存在')
        print(form.errors)
        return json_status.params_error(message=form.get_error())


# 新闻删除
@staff_member_required(login_url='/authPro/login/')
@csrf_exempt
def delete(self, request):
    from django.http import QueryDict
    res = QueryDict(request.body)
    news_id = res.get('news_id')
    if news_id:
        news = News.objects.filter(id=news_id).first()
        if news:
            hot_news = NewsHot.objects.filter(news=news)
            if hot_news:
                hot_news.update(is_delete=True)
            news.is_delete = True
            news.save()
            return json_status.result()
        return json_status.params_error(message="新闻不存在")
    return json_status.params_error(message="参数错误")


@method_decorator([csrf_exempt, staff_member_required(login_url='/authPro/login/')], name='dispatch')
class NewsEditView(View):
    def get(self,request):
        news_id = request.GET.get('news_id')
        if news_id:
            news = News.objects.filter(id=news_id).first()
            if news:
                news_tags = NewsTag.objects.filter(is_delete=True).all()
                context = {'news':news, 'news_tags': news_tags}
                return render(request, 'admin/news/news_pub.html', context=context)
            return json_status.params_error(message='新闻找不到')
        return json_status.params_error(message='新闻id错误')

@ajax_login_required
@csrf_exempt
def upload_file(request):
    file = request.FILES.get('upload_file')
    file_name = file.name
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    with open(file_path, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
    #         返回当前视图对应的绝对路径
    file_url = request.build_absolute_uri(settings.MEDIA_URL+file_name)
    return json_status.result(data={'file_url': file_url})


def up_token(request):

    # 需要填写你的 Access Key 和 Secret Key
    access_key = '8VLej4xsAijBEpXVCxWXpn-T1ZFPeKTvpcHfWn8g'
    secret_key = 'lAW1VeKi04t-7NC0H0IWZUc7QQz_okMfdkuX4ynX'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'json'

    # 3600为token过期时间，秒为单位。3600等于一小时
    token = q.upload_token(bucket_name)
    print(token)
    return JsonResponse({'uptoken': token})


class NewsManageViews(View):
    def get(self, request):
        p = int(request.GET.get('p', 1))
        newses = News.objects.defer('content').select_related('tag', 'author')
        start_time = request.GET.get('start_time', '')
        end_time = request.GET.get('end_time', '')
        # form  id
        title = request.GET.get('title', '')
        author = request.GET.get('author', '')
        # print('====================')
        # print(author)
        # print('====================')
        tag_id = int(request.GET.get('tag_id', 0))
        if start_time and end_time:
            start_date = datetime.strptime(start_time, '%Y/%m/%d')
            end_date =  datetime.strptime(end_time, '%Y/%m/%d') + timedelta(days=1)
            from django.utils.timezone import make_aware
            newses = newses.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))
        if title:
            newses = newses.filter(title__icontains=title)
        if author:
            newses = newses.filter(author__username__icontains=author)
            # print('====================')
            # print(newses)
            # print('====================')
        if tag_id:
            newses = newses.filter(tag=tag_id)
        news_tags = NewsTag.objects.filter(is_delete=True).all()
        paginator = Paginator(newses, settings.ONE_PAGE_NEWS_COUNT)
        page = paginator.page(p)
        page_date = self.get_page_data(paginator, page)
        context = {
            'newses': page.object_list,
            'news_tags': news_tags,
            'paginator': paginator,
            'page': page,
            'start_time': start_time,
            'end_time': end_time,
            'title': title,
            'author': author,
            'tag_id':tag_id,
            'other_param': urlencode({
                'start_time': start_time,
                'end_time': end_time,
                'title': title,
                'author': author,
                'tag_id': tag_id,
            })
        }
        context.update(page_date)
        # print('==============================')
        # print(page_date)
        # print('==============================')
        return render(request, 'admin/news/news_manage.html', context=context)
    @staticmethod
    def get_page_data(paginator, page, around_count=2):
        # 获取当前所在页码
        current_page = page.number
        # 获取总的页数
        total_page = paginator.num_pages

        # 标志位,
        left_has_more = False
        right_has_more = False

        # 算出当前页左边的页码
        left_start_index = current_page - around_count
        left_end_index = current_page
        if current_page <= around_count + around_count + 1:
            left_pages = range(1, left_end_index)
        else:
            left_has_more = True
            left_pages = range(left_start_index, left_end_index)
        # 算出当前页右边的页码
        right_start_index = current_page + 1
        right_end_index = current_page + around_count + 1
        if current_page >= total_page - around_count - around_count:
            right_pages = range(right_start_index, total_page + 1)
        else:
            right_has_more = True
            right_pages = range(right_start_index, right_end_index)

        return {
            'current_page': current_page,
            'total_page': total_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'left_pages': left_pages,
            'right_pages': right_pages,
        }


@method_decorator(csrf_exempt, name='dispatch')
class NewsHotViews(View):
    def get(self, request):
        return render(request, 'admin/news/news_hot.html')

    def put(self, request):
        ret = QueryDict(request.body)
        priority = int(ret.get('priority', 0))
        if priority:
            hot_news_id = int(ret.get('hot_news_id', 0))
            hot_news = NewsHot.objects.filter(id=hot_news_id)
            if hot_news:
                hot_news.update(priority=priority)
                return json_status.result()
            return json_status.params_error(message='热门新闻不存在')
        return json_status.params_error(message='优先级错误')


    def delete(self,request):
        ret = QueryDict(request.body)
        hot_news_id = int(ret.get('hot_news_id', 0))
        hot_news = NewsHot.objects.filter(id=hot_news_id)
        if hot_news:
            hot_news.update(is_detele=False)
            return json_status.result()
        return json_status.params_error(message='热门新闻不存在')





@method_decorator(csrf_exempt, name='dispatch')
class NewsHotAddViews(View):
    def get(self, request):
        return render(request, 'admin/news/news_hot_add.html')

    def post(self,request):
        form = NewsHotAddForm(request.POST)
        if form.is_valid():
            news_id  = form.cleaned_data.get('news_id')
            priority = form.cleaned_data.get('priority')
            news = News.objects.filter(id=news_id).first()
            if news:
                hot_news = NewsHot.objects.filter(news=news).exists()
                if hot_news:
                    return json_status.params_error(message='该新闻已经是热门新闻')
                NewsHot.objects.create(priority=priority, news=news)
                return json_status.result()
            return json_status.params_error(message='新闻不存在')
        return json_status.params_error(message=form.get_error())


# /admin/news/banner/
@method_decorator([csrf_exempt, ], name="dispatch")
class NewsBannerView(View):
    """新闻轮播图的增删改查"""
    def get(self, request):
        return render(request, 'admin/news/news_banner.html')

    def post(self, request):
        form = NewsBannerForm(request.POST)
        if form.is_valid():
            link_to = form.cleaned_data.get("link_to")
            image_url = form.cleaned_data.get('image_url')
            priority = form.cleaned_data.get('priority')
            print('link_to:{},image_url:{},priority:{} '.format(link_to, image_url, priority))
            banner = NewsBanner.objects.create(image_url=image_url, priority=priority, link_to=link_to)
            return json_status.result(data={"banner_id": banner.id, "priority": priority})
        return json_status.params_error(message=form.get_error())

    def put(self, request):
        p = QueryDict(request.body)
        banner_id = p.get("banner_id")
        image_url = p.get("image_url")
        priority = p.get("priority")
        link_to = p.get("link_to")
        if banner_id:
            banner = NewsBanner.objects.filter(id=banner_id)
            if banner:
                banner.update(image_url=image_url, priority=priority, link_to=link_to)
                return json_status.result()
            return json_status.result().params_error(message='轮播图找不到')
        return json_status.result().params_error(message="bannerId不存在")

    def delete(self, request):
        d = QueryDict(request.body)
        banner_id = d.get("banner_id")
        if banner_id:
            banner = NewsBanner.objects.filter(id=banner_id)
            if banner:
                banner.update(is_delete=True)
                return json_status.result()
            return json_status.params_error(message="轮播图不存在")
        return json_status.params_error(message="轮播图id不存在")
