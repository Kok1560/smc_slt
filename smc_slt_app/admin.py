from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Inventory)
admin.site.register(Product)
admin.site.register(Event)
admin.site.register(Order)
admin.site.register(Maintenance)
admin.site.register(Package)




