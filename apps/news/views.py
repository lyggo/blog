from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.views.decorators.http import require_GET
from .models import NewsTag, News, NewsBanner
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .forms import AddNewsCommentForm
from utils import json_status
from .models import NewsComment, NewsHot
from .serializers import NewsCommentSerializers, NewsSerializer, NewsTagSerializer, NewsHotSerializer, NewsBannerSerializer
from django.contrib.auth.decorators import login_required
from utils.decorators import ajax_login_required
from django.conf import settings


@require_GET
def index(request):
    # select_related 预查询
    news_tags = NewsTag.objects.filter(is_delete=True).all()
    newses = News.objects.defer('content').select_related('tag', 'author').filter(is_delete=True).all()[0:settings.ONE_PAGE_NEWS_COUNT]
    h_newses = NewsHot.objects.filter(is_detele=True).all()
    banners = NewsBanner.objects.filter(is_delete=False).all()
    context = {
        'news_tags': news_tags,
        'newses': newses,
        'h_newses': h_newses,
        'banners': banners,
    }
    return render(request, 'news/index.html',
                  context=context)


def news_list(request):
    page = int(request.GET.get('page', 1))
    tag_id = int(request.GET.get('tag_id', 0))
    # 计算一页
    # 开始位置
    start_page = settings.ONE_PAGE_NEWS_COUNT*(page - 1)
    # 结束位置
    end_page = start_page + settings.ONE_PAGE_NEWS_COUNT
    # print(start_page, end_page)
    if tag_id:
        newses = News.objects.defer('content').select_related('tag', 'author').filter(is_delete=True, tag=tag_id).all()[start_page:end_page]
    # 返回序列化的数据
    else:
        newses = News.objects.defer('content').select_related('tag', 'author').filter(is_delete=True).all()[
                 start_page:end_page]
    serializer = NewsSerializer(newses, many=True)
    return json_status.result(data={'newses':serializer.data})



def news_detail(request, news_id):
    try:
        # news = News.objects.filter(id=news_id, is_delete=True).first()
        news = News.objects.get(id=news_id, is_delete=True)
        return render(request, 'news/news_detail.html',
                      context={'news': news})
    except News.DoesNotExist:
        raise Http404


@method_decorator([csrf_exempt, ajax_login_required], name='dispatch')
class AddNewsComment(View):
    def post(self, request):
        form = AddNewsCommentForm(request.POST)
        if form.is_valid():
            news_id = form.cleaned_data.get('news_id')
            content = form.cleaned_data.get('content')
            news = News.objects.filter(id=news_id).first()
            if news:
                comment = NewsComment.objects.create(content=content, author=request.user, news=news)
                serializer = NewsCommentSerializers(comment)
                return json_status.result(data=serializer.data)
            # print(news_id, content)
            return json_status.params_error(message='新闻不存在')
        return json_status.params_error(message=form.get_error())


def comment_list_with_news(request):
    news_id = request.GET.get('news_id')
    news = News.objects.filter(id=news_id).first()
    if news:
        news_comments = news.comments.all()
        serializer = NewsCommentSerializers(news_comments, many=True)
        return json_status.result(data=serializer.data)
    return json_status.params_error(message='新闻找不到')

def search(request):
    q = request.GET.get("q", '')
    if q:
        result_newses = News.objects.select_related('tag', 'author').filter(Q(title__icontains=q)|Q(author__username__icontains=q)|Q(tag__name__icontains=q)|Q(content__icontains=q)|Q(desc__icontains=q))
        context = {
            "result_newses": result_newses,
            "q": q,
        }
    else:
        h_newses = NewsHot.objects.select_related('news', 'news__tag', 'news__author').filter(is_detele=False)
        context = {
            "h_newses": h_newses,
        }
    return render(request, 'news/search.html', context=context)

# 返回新闻标签的api接口
def news_tag_list(request):
    news_tags = NewsTag.objects.filter(is_delete=True).all()
    serializer = NewsTagSerializer(news_tags, many=True)
    return json_status.result(data={'tags':serializer.data})

# /news/news-with-tag/
def news_with_tag(request):
    tag_id = int(request.GET.get('tag_id', 0))
    if tag_id:
        newses = News.objects.filter(tag=tag_id, is_delete=True).all()
        if not tag_id:
            return json_status.params_error(message='该分类下无新闻')
    else:
        newses = News.objects.filter(is_delete=True).all()
    serialzier = NewsSerializer(newses, many=True)
    return json_status.result(data={'newses':serialzier.data})


# /news/hot/list/
def hot_news_list(request):
    # 所有新闻
    hot_newses = NewsHot.objects.filter(is_detele=True).all()
    serializer = NewsHotSerializer(hot_newses, many=True)
    return json_status.result(data=serializer.data)


@require_GET   #  /news/banner/list/
def news_banner_list(request):
    """返回banner的列表 """
    banners = NewsBanner.objects.filter(is_delete=False)
    serializer = NewsBannerSerializer(banners, many=True)
    return json_status.result(data={"banners": serializer.data})


