from django.contrib import admin

from .models import Cuisine, Menu, Nutrition, Ingredient, Serving, FeatureTag

# Register your models here.

class PriceAdmin(admin.ModelAdmin):
    list_display = ['menu', 'serving', 'price']
    

admin.site.register(Cuisine)
admin.site.register(FeatureTag)
admin.site.register(Menu)
admin.site.register(Nutrition)
admin.site.register(Ingredient)
admin.site.register(Serving)
