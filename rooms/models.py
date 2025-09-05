from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Room(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name='รหัสห้อง')
    name = models.CharField(max_length=100, verbose_name='ชื่อห้อง')
    capacity = models.PositiveIntegerField(default=30, verbose_name='ความจุ')
    is_active = models.BooleanField(default=True, verbose_name='เปิดใช้งาน')

    class Meta:
        ordering = ['code']
        verbose_name = 'ห้องเรียน'
        verbose_name_plural = 'ห้องเรียน'

    def __str__(self):
        return f'{self.code} - {self.name}'

class Booking(models.Model):
    STATUS_CHOICES = (
        ('active', 'ใช้งาน'),
        ('cancelled', 'ยกเลิก'),
    )
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    title = models.CharField(max_length=200, verbose_name='หัวข้อ/วิชา')
    start = models.DateTimeField(verbose_name='เริ่ม')
    end = models.DateTimeField(verbose_name='สิ้นสุด')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start']
        verbose_name = 'การจอง'
        verbose_name_plural = 'การจอง'
        indexes = [
            models.Index(fields=['room', 'start', 'end', 'status']),
        ]

    def clean(self):
        if self.end <= self.start:
            raise ValidationError('เวลาสิ้นสุดต้องมากกว่าเวลาเริ่ม')

        if self.start < timezone.now():
            raise ValidationError('ไม่อนุญาตให้จองย้อนหลัง')

        if not self.room.is_active:
            raise ValidationError('ห้องนี้ถูกปิดใช้งาน')

        # กันการทับซ้อน (เฉพาะสถานะ active)
        qs = Booking.objects.filter(room=self.room, status='active')
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        overlap = qs.filter(start__lt=self.end, end__gt=self.start).exists()
        if overlap:
            raise ValidationError('ช่วงเวลานี้ถูกจองแล้ว')

    def __str__(self):
        return f'{self.room} | {self.title} | {self.start:%Y-%m-%d %H:%M}'
