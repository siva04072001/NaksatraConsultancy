from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Tickets)
admin.site.register(Department)
admin.site.register(Location)
admin.site.register(Subdivision)
admin.site.register(Item)

