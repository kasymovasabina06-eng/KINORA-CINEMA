from django.contrib import admin
from .models import Genre,Movie
class MovieInline(admin.TabularInline):
    model=Movie; extra=0; fields=('title','year','is_upcoming'); show_change_link=True
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display=('name','slug'); prepopulated_fields={'slug':('name',)}; inlines=[MovieInline]
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display=('title','year','genre','rating','is_upcoming'); list_filter=('genre','is_upcoming','year'); search_fields=('title','original_title','actors'); list_editable=('is_upcoming',)
admin.site.site_header='KINORA • Управление кинотеатром'
