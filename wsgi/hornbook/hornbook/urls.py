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
from rest_framework import routers
from study.views import HanziStudyCountViewSet
from study.views import HanziStudyRecordViewSet
from study.views import UserViewSet
from lexicon.views import HanziViewSet

import lexicon.views


router = routers.DefaultRouter()
router.register(r'study/hanzi-study-count', HanziStudyCountViewSet)
router.register(r'study/hanzi-study-record', HanziStudyRecordViewSet)
router.register(r'study/user', UserViewSet)
# router.register(r'lexicon/hanzi', HanziViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-admin/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^api/lexicon/hanzis', lexicon.views.HanziList.as_view()),
    url(r'^api/lexicon/hanzi/(?P<content>\w+)', lexicon.views.HanziDetail.as_view()),
    url(r'^api/lexicon/hanzi', lexicon.views.HanziCreate.as_view()),
]
