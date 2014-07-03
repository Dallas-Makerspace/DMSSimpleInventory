from django.contrib import admin
from inventory.models import Part
from inventory.models import Bin
from inventory.models import Package
from inventory.models import Category

admin.site.register(Part)
admin.site.register(Bin)
admin.site.register(Package)
admin.site.register(Category)
