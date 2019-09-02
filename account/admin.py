from django.contrib import admin
from account.models import UserProfile

# Register your models here.
admin.site.site_header = "Admin"
admin.site.register(UserProfile)
