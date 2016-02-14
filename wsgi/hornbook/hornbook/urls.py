"""hornbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
# from django.views.generic import TemplateView

from rest_framework import routers

from study.views import HanziStudyCountViewSet
from study.views import HanziStudyRecordViewSet
from study.views import UserViewSet
from study.views import CategoryViewSet
from study.views import CardViewSet

import lexicon.views

admin.autodiscover()


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'study/hanzi_study_count', HanziStudyCountViewSet, base_name='hanzistudycount')
router.register(r'study/hanzi_study_record', HanziStudyRecordViewSet, base_name='hanzistudyrecord')
router.register(r'study/category', CategoryViewSet, base_name='category')
router.register(r'study/card', CardViewSet, base_name='card')
router.register(r'study/user', UserViewSet, base_name='user')
router.register(r'lexicon/hanzi', lexicon.views.HanziViewSet, base_name='hanzi')

urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api-admin/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),

    url(r'^$', 'hornbook.views.index'),

    # log in/out
    # url(r'^accounts/login/$', 'django.contrib.auth.views.login',
    #     {'template_name': 'login.html'}),
    # url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
    #     {'next_page': '/'}),
]
