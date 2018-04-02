from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(City_Information)
admin.site.register(City_Hotplace)
admin.site.register(Company_Information)
admin.site.register(Travel_Information)
admin.site.register(Travel_Schedule)
