from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from study.models import Category
from study.models import HanziStudyCount

import logging
log = logging.getLogger('hornbook')


def setupNewUser(user):
    # add category
    read_hanzi = Category.objects.create(user=user, name='read_hanzi')
    write_hanzi = Category.objects.create(user=user, name='write_hanzi')
    chinese_poem = Category.objects.create(user=user, name='chinese_poem')
    # add count
    HanziStudyCount.objects.create(user=user, category=read_hanzi, count=1)
    HanziStudyCount.objects.create(user=user, category=write_hanzi, count=1)
    HanziStudyCount.objects.create(user=user, category=chinese_poem, count=1)


class MyAdapter(DefaultAccountAdapter):
    def new_user(self, request):
        log.debug('MyAdapter.new_user')
        return super(MyAdapter, self).new_user(request)

    def save_user(self, request, user, form, commit=True):
        log.debug('MyAdapter.save_user')
        user = super(MyAdapter, self).save_user(request, user, form, commit)
        setupNewUser(user)
        return user

    def get_login_redirect_url(self, request):
        return '/'


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    override save_user
    """
    def pre_social_login(self, request, sociallogin):
        log.debug('MySocialAccountAdapter.pre_social_login')
        return super(MySocialAccountAdapter, self).pre_social_login(request, sociallogin)

    def new_user(self, request, sociallogin):
        log.debug('MySocialAccountAdapter.new_user')
        return super(MySocialAccountAdapter, self).new_user(request, sociallogin)

    def save_user(self, request, sociallogin, form=None):
        log.debug('MySocialAccountAdapter.save_user')
        user = super(MySocialAccountAdapter, self).save_user(request, sociallogin, form)
        setupNewUser(user)
        return user

    def populate_user(self, *args, **kwargs):
        log.debug('MySocialAccountAdapter.populate_user')
        return super(MySocialAccountAdapter, self).populate_user(*args, **kwargs)
