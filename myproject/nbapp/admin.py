from django.contrib import admin
from .models import Emiten, TbpTable2

# Register your models here.
#for list emiten in admin mode
class EmitenAdmin(admin.ModelAdmin):
    list_display = ('emiten_code', 'emiten_name')
admin.site.register(Emiten, EmitenAdmin)


#for list sentencesplit in admin mode
class TbpTable2Admin(admin.ModelAdmin):
    list_display = ('title', 'source', 'date', 'paragraph', 'emiten')
admin.site.register(TbpTable2, TbpTable2Admin)