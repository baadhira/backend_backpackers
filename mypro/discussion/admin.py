from django.contrib import admin

# Register your models here.
from discussion.models import *

admin.site.register(Discussion)
admin.site.register(DiscussionComment)
admin.site.register(LikeDisComment)
admin.site.register(ReplyDiscussionComment)
#
# admin.site.register(ReportDiscussion)

admin.site.register(Comment)
admin.site.register(ReportComment)


