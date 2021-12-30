from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account,SocialLogin,WaitList,Feedback

# Register your models here.

class AccountAdmin(UserAdmin):
	list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'user_country', 'no_files')
	search_feilds = ('email', 'username',)
	readonly_fields = ('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets =()

class WaitListAdmin(admin.ModelAdmin):
	list_display = ('email','joined', 'time',)
	search_feilds = ('email', )
	filter_horizontal = ()
	list_filter = ('email','joined', 'time',)
	fieldsets =()


class FeedbackAdmin(admin.ModelAdmin):
	list_display = ('email','name', 'message','time',)
	search_feilds = ('email','name' )
	filter_horizontal = ()
	list_filter = ('email','name','time',)
	fieldsets =()


admin.site.register(Account, AccountAdmin)	
admin.site.register(SocialLogin)	
admin.site.register(WaitList,WaitListAdmin)
admin.site.register(Feedback,FeedbackAdmin)