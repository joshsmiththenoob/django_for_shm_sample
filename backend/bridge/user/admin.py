from django.contrib import admin
from .models import AuthUrl, AuthGroupUrls

# Register your models here.
admin.site.register(AuthUrl)


# Customize the display on admin page
@admin.register(AuthGroupUrls)
class AuthGroupUrlsAdmin(admin.ModelAdmin):
    # 指定在列表中顯示的欄位
    list_display = ('id', 'group', 'url')
    # 如果需要支持搜尋，可以加入以下代碼
    search_fields = ('group__name', 'url__path')
    # 添加過濾器，根據需要選擇欄位
    list_filter = ('group', 'url')

