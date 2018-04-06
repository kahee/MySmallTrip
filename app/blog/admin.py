from django.contrib import admin

# Register your models here.
from .models import Blog,BlogImage


admin.site.register(Blog)
admin.site.register(BlogImage)
