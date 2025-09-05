from django.contrib import admin
from .models import Room, Booking

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'capacity', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('code', 'name')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'title', 'user', 'start', 'end', 'status')
    list_filter = ('status', 'room')
    search_fields = ('title', 'user__username')
