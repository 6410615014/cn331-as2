from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "form-control form-control-lg rounded-pill shadow-sm",
            })

        self.fields["username"].widget.attrs["placeholder"] = "กรอกชื่อผู้ใช้"
        self.fields["email"].widget.attrs["placeholder"] = "กรอกอีเมล"
        self.fields["password1"].widget.attrs["placeholder"] = "ตั้งรหัสผ่าน"
        self.fields["password2"].widget.attrs["placeholder"] = "ยืนยันรหัสผ่าน"

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('room', 'title', 'start', 'end')
        widgets = {
            'room': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'start': forms.DateTimeInput(attrs={
                'class': 'form-control flatpickr-dt',
                'id': 'id_start',
                'autocomplete': 'off',
                'placeholder': 'YYYY-MM-DD HH:MM',
            }),
            'end': forms.DateTimeInput(attrs={
                'class': 'form-control flatpickr-dt',
                'id': 'id_end',
                'autocomplete': 'off',
                'placeholder': 'YYYY-MM-DD HH:MM',
            }),
        }


