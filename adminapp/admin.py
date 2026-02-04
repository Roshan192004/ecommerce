from django.contrib import admin
from .models import Category, Medicine
from .models import DeliveryLocation
from .models import ServiceableLocation
admin.site.register(Category)
admin.site.register(Medicine)
admin.site.register(DeliveryLocation)
admin.site.register(ServiceableLocation)