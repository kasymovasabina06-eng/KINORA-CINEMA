from django.contrib import admin
from .models import Cinema,Hall,Showtime,Profile,Booking,BookingSeat
class HallInline(admin.TabularInline): model=Hall; extra=0
@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin): list_display=('name','address'); inlines=[HallInline]
@admin.register(Hall)
class HallAdmin(admin.ModelAdmin): list_display=('name','cinema','rows','columns'); list_filter=('cinema',)
@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin): list_display=('movie','hall','starts_at','price'); list_filter=('hall__cinema','starts_at'); search_fields=('movie__title',)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin): list_display=('user','phone'); filter_horizontal=('favorites',)
class BookingSeatInline(admin.TabularInline): model=BookingSeat; extra=0; readonly_fields=('showtime','row','number')
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin): list_display=('id','user','showtime','total','status','created_at'); list_filter=('status',); readonly_fields=('user','showtime','total','status','created_at'); inlines=[BookingSeatInline]
