from django.db import models


class NewsTag(models.Model):
    name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
    # 用于表示是否删除
    is_delete = models.BooleanField(default=True)


# 新闻模型
class News(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    thumbnail_url = models.URLField()
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=True)

    # 外键 标签 作者
    tag = models.ForeignKey('NewsTag', on_delete=models.CASCADE)
    author = models.ForeignKey('authPro.User', on_delete=models.CASCADE)


    class Meta:
        # 倒序
        ordering = ('-id',)


class NewsComment(models.Model):
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=True)
    author = models.ForeignKey('authPro.User', on_delete=models.CASCADE)
    news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='comments')
    class Meta:
        # 倒序
        ordering = ('-id',)


class NewsHot(models.Model):
    news = models.OneToOneField('News', on_delete=models.CASCADE)
#     优先级
    priority = models.IntegerField()
    is_detele = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Mete:
        # 默认小到大
        ordering = ['-priority']


class NewsBanner(models.Model):
    image_url = models.URLField()
    priority = models.IntegerField()
    link_to = models.URLField()
    create_date = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        ordering = ['-priority']