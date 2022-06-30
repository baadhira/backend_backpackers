from django.contrib import admin
from app.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



admin.site.register(User)
# admin.site.register(Profile)
admin.site.register(Album)
admin.site.register(SendHostRequest)
admin.site.register(Feedback)
admin.site.register(Friendrequest)
admin.site.register(ReportUser)
admin.site.register(PopularDest)
# admin.site.register(BlockUser)
admin.site.register(SendHostRequestReply)






# class UserModelAdmin(BaseUserAdmin):
  

#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_display = ('id','email','phone_number' ,'username','first_name', 'last_name' )
#     list_filter = ('is_admin',)
#     fieldsets = (
#         ('User Credentials', {'fields': ('username', 'password')}),
#         ('Personal info', {'fields': ('email','phone_number' ,'first_name', 'last_name')}),
#         ('Permissions', {'fields': ('is_admin',)}),
#     )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email','phone_number' ,'username','first_name', 'last_name', 'password1', 'password2'),
#         }),
#     )
#     search_fields = ('username',)
#     ordering = ('username','id')
#     filter_horizontal = ()


# Now register the new UserAdmin...

