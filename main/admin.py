from django.contrib import admin

# Register your models here.
from main.models import *


class ImageInlineAdmin(admin.TabularInline):
    model = Image
    fields = ('image', )
    max_num = 5

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [ImageInlineAdmin, ]


admin.site.register(Category)


