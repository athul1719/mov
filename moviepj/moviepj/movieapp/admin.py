from django.contrib import admin

from movieapp.models import Category, Movie, PetOwner


# Register your models here.
class categoryadmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Category,categoryadmin)

class movieadmin(admin.ModelAdmin):
    list_display = ['name','desc','date','actors','category','trailer']
    list_editable = ['desc','date','trailer']
    prepopulated_fields = {'slug':('name',)}
    list_per_page = 20
admin.site.register(Movie,movieadmin)

class petowneradmin(admin.ModelAdmin):
    list_display = ['username','first_name','last_name','email','password']
    list_per_page = 20
admin.site.register(PetOwner,petowneradmin)