from django.contrib import admin
from event.models import *
# # Register your models here.
admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(JoinedPeople)
admin.site.register(ReportEvent)
admin.site.register(EventComment)




