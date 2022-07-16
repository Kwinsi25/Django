from django.contrib import admin
from Language.models import language
from django.utils.html import format_html
from Project.settings import DATE_TIME_FORMAT
# Register your models here.
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['title','locale','icons','isDefault','status','created_date','updated_date',]

    def created_date(self, obj):
        return obj.createdAt.strftime(DATE_TIME_FORMAT)
    def updated_date(self, obj):
        return obj.updatedAt.strftime(DATE_TIME_FORMAT)

    def icons(self,obj):
        return format_html(f'<img src ="/media/{obj.icon}" style="height:30; width:30px;">')


admin.site.register(language,LanguageAdmin)