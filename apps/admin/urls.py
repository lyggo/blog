from django.urls import path
from . import views, course_view, doc_view

app_name = 'admin'

urlpatterns = [
    path('', views.index, name='index'),
    path('news-tag-manage/', views.NewsTagView.as_view(), name='news_tag_manage'),
    path('news-pub/', views.NewsPubView.as_view(), name='news_pub'),
    path('news-edit/', views.NewsEditView.as_view(), name='news_edit'),              path('news-banner/', views.NewsBannerView.as_view(), name='news_banner'),
    path('news-manage/', views.NewsManageViews.as_view(), name='news_manage'),
    path('news-hot/', views.NewsHotViews.as_view(), name='news_hot'),
    path('news-hot-add/', views.NewsHotAddViews.as_view(), name='news_hot_add'),
    path('upload-file/', views.upload_file, name='upload_file'),
    path('up-token/', views.up_token, name='up_token'),
]

# course
urlpatterns += [
    path('course-pub/', course_view.CoursePubView.as_view(), name='course_pub'),
    path('teacher-add/', course_view.add_teacher),
]

""" doc """
urlpatterns += [
    path('doc-upload/', doc_view.DocUploadView.as_view(), name='doc_upload'),

]

