from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),

    path('bookings/new/', views.booking_create, name='booking_create'),
    path('bookings/mine/', views.my_bookings, name='my_bookings'),
    path('bookings/<int:pk>/cancel/', views.booking_cancel, name='booking_cancel'),

    # admin-lite
    path('manage/rooms/', views.manage_rooms, name='manage_rooms'),
    path('manage/rooms/<int:pk>/toggle/', views.toggle_room_active, name='toggle_room_active'),
]
