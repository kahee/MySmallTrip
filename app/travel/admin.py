from django.contrib import admin

# Register your models here.
from imagekit.admin import AdminThumbnail

from .models import CityHotplace, TravelInformation, TravelSchedule, CompanyInformation, CityInformation, \
    TravelInformationImage

#
# class PhotoAdmin(admin.ModelAdmin):
#     list_display = ('__str__', "admin_thumbnail")
#     admin_thumbnail = AdminThumbnail(image_field='product_thumbnail')



admin.site.register(CityInformation)
admin.site.register(CityHotplace)
admin.site.register(CompanyInformation)
admin.site.register(TravelInformation)
admin.site.register(TravelSchedule)
# admin.site.register(TravelInformationImage)

admin.site.register(TravelInformationImage)