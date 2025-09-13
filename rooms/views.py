from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from .models import Room, Booking
from .forms import RegisterForm, BookingForm , AdminBookingUpdateForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'สมัครสมาชิกสำเร็จ กรุณาเข้าสู่ระบบ')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})

@login_required
def room_list(request):
    rooms = Room.objects.filter(is_active=True)
    return render(request, 'rooms/room_list.html', {'rooms': rooms})

@login_required
def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk, is_active=True)
    bookings = room.bookings.filter(status='active', end__gte=timezone.now()).order_by('start')
    return render(request, 'rooms/room_detail.html', {'room': room, 'bookings': bookings})

@login_required
def booking_create(request):
    if request.user.is_staff:
        messages.error(request, 'ผู้ดูแลระบบไม่สามารถสร้างการจองได้ โปรดจัดการผ่านหน้า "จัดการห้อง"')
        return redirect('rooms:manage_rooms')
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            try:
                booking.full_clean()
                booking.save()
                messages.success(request, 'สร้างการจองสำเร็จ')
                return redirect('rooms:my_bookings')
            except Exception as e:
                form.add_error(None, e)
    else:
        form = BookingForm()
    return render(request, 'rooms/booking_form.html', {'form': form})

@login_required
def my_bookings(request):
    if request.user.is_staff:
        messages.info(request, 'ผู้ดูแลระบบไม่มีหน้าการจองส่วนตัว')
        return redirect('rooms:manage_rooms')
    
    qs = Booking.objects.filter(user=request.user).order_by('-start')[:100]
    return render(request, 'rooms/my_bookings.html', {'bookings': qs})

@login_required
def booking_cancel(request, pk):
    if request.user.is_staff:
        messages.error(request, 'ผู้ดูแลระบบให้ยกเลิกจากหน้าจัดการห้องเท่านั้น')
        return redirect('rooms:manage_rooms')
    
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if booking.status == 'cancelled':
        messages.info(request, 'การจองนี้ถูกยกเลิกแล้ว')
    else:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'ยกเลิกการจองเรียบร้อย')
    return redirect('rooms:my_bookings')

def is_staff(user): return user.is_staff

@user_passes_test(is_staff)
def manage_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/manage_rooms.html', {'rooms': rooms})

@user_passes_test(is_staff)
def toggle_room_active(request, pk):
    room = get_object_or_404(Room, pk=pk)
    room.is_active = not room.is_active
    room.save()
    return redirect('rooms:manage_rooms')

def is_staff(user): 
    return user.is_staff

@user_passes_test(is_staff)
def manage_room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    bookings = room.bookings.filter(end__gte=timezone.now()).order_by('start')
    return render(request, 'rooms/manage_room_detail.html', {
        'room': room,
        'bookings': bookings,
    })

@user_passes_test(is_staff)
def admin_booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = AdminBookingUpdateForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'แก้ไขการจองเรียบร้อย')
            return redirect('rooms:manage_room_detail', pk=booking.room_id)
    else:
        form = AdminBookingUpdateForm(instance=booking)
    return render(request, 'rooms/admin_booking_form.html', {
        'form': form,
        'booking': booking,
    })

@user_passes_test(is_staff)
def admin_booking_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        if booking.status == 'cancelled':
            messages.info(request, 'การจองนี้ถูกยกเลิกอยู่แล้ว')
        else:
            booking.status = 'cancelled'
            booking.save()
            messages.success(request, 'ยกเลิกการจองเรียบร้อย')
        return redirect('rooms:manage_room_detail', pk=booking.room_id)
    messages.error(request, 'วิธีการไม่ถูกต้อง')
    return redirect('rooms:manage_room_detail', pk=booking.room_id)

