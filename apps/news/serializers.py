from rest_framework import serializers
from .models import NewsComment, News, NewsTag, NewsHot, NewsBanner
from apps.authPro.serializers import UserSerializer


class NewsCommentSerializers(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = NewsComment
        # 序列化字段
        fields = ('id', 'content', 'create_time', 'author')


class NewsTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsTag
        fields = ('id','name',)


class NewsSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    tag = NewsTagSerializer()
    class Meta:
        model = News
        fields = ('id','title','desc', 'thumbnail_url', 'pub_time', 'author', 'tag')


class NewsHotSerializer(serializers.ModelSerializer):
    news = NewsSerializer()
    class Meta:
        model = NewsHot
        fields = ('id', 'priority','is_detele','news')


class NewsBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsBanner
        fields = '__all__'