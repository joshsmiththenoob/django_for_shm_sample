from django.contrib import admin
from .models import (Agency, 
                    AuthAgencyUsers, 
                    Sensor, 
                    Bridge, 
                    AuthAgencyBridges,
                    EngineeringFirm)

# Register your models here.
admin.site.register([Agency, Bridge])


# @admin.register(AuthAgencyUsers)
# class AuthAgencyUsersAdmin(admin.ModelAdmin):
#     # 指定在列表中顯示的欄位
#     list_display = ('id', 'agency', 'user')
#     # 如果需要支持搜尋，可以加入以下代碼
#     search_fields = ('agency__name', 'user__name')
#     # 添加過濾器，根據需要選擇欄位
#     list_filter = ('agency', 'user')


# @admin.register(AuthAgencyBridges)
# class AuthAgencyUsersAdmin(admin.ModelAdmin):
#     # 指定在列表中顯示的欄位
#     list_display = ('id', 'agency', 'bridge')
#     # 如果需要支持搜尋，可以加入以下代碼
#     search_fields = ('agency__name', 'bridge__name')
#     # 添加過濾器，根據需要選擇欄位
#     list_filter = ('agency', 'bridge')



# @admin.register(Sensor)
# class SensorNamesAdmin(admin.ModelAdmin):
#     # 指定在列表中顯示的欄位
#     list_display = ('id', 'bid', 'sensor')
#     # 如果需要支持搜尋，可以加入以下代碼
#     search_fields = ('bridge__name', 'sensor__name')
#     # 添加過濾器，根據需要選擇欄位
#     list_filter = ('bid', 'sensor')


# @admin.register(EngineeringFirm)
# class EngineeringFirmAdmin(admin.ModelAdmin):
#     # 指定在列表中顯示的欄位
#     list_display = ('id', 'name', 'agency__name')
#     # 如果需要支持搜尋，可以加入以下代碼
#     search_fields = ('name',)
#     # 添加過濾器，根據需要選擇欄位
#     list_filter = ('name',)