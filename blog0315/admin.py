from django.contrib import admin
from .models import Profile,Article,Category,Tag,Testnum,ReadNum,Testfiled
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

#            ### 改下USR的模型，增加昵称的显示
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username' ,'nickname','is_staff','is_active','is_superuser')

    def nickname(self, obj):
        return obj.profile.nickname
    nickname.short_description = '昵称'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfieAdmin(admin.ModelAdmin):
    list_display = ('user','nickname','logo','telephone')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'created_time', 'modified_time',  'author','read_num']
admin.site.register(Article, ArticleAdmin)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class ReadNumAdmin(admin.ModelAdmin):
    list_display = ['article','read_num']
admin.site.register(ReadNum, ReadNumAdmin)

admin.site.register(Testfiled)
admin.site.register(Tag)
admin.site.register(Testnum)



# Register your models here.
