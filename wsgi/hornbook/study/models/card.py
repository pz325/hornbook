from django.db import models


class Card(models.Model):
    '''
    '''
    font_size = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return 'font size: ' + self.font_size
