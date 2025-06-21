from django.contrib import admin
from .models import clients, Owner, Meeting
# Register your models here.

admin.site.register(clients)
admin.site.register(Owner)
admin.site.register(Meeting)