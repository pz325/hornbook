from django.db import models
from django.contrib.auth.models import User
from card import Card


class Category(models.Model):
    '''
    id is the index
    can be filtered by User
    '''
    user = models.ForeignKey(User, editable=False, db_index=True, related_name='categories')
    display = models.CharField(max_length=200, default="display")
    num_retired = models.PositiveSmallIntegerField(default=10)
    card = models.ForeignKey(Card, null=True)

    def __unicode__(self):
        return self.user.username + ': ' + self.display
