from django.contrib import admin

# Register your models here.
from models.card import Card
from models.log import StudySessionContentLog
from models.log import StudySessionResultLog
from models.study import HanziStudyRecord
from models.study import HanziStudyCount
from models.category import Category


admin.site.register(HanziStudyRecord)
admin.site.register(HanziStudyCount)
admin.site.register(Category)
admin.site.register(StudySessionContentLog)
admin.site.register(StudySessionResultLog)
admin.site.register(Card)
