from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin Bimbel'),
        ('siswa', 'Siswa'),
    )

    username_validator = RegexValidator(
        regex=r'^[\w\s.@+-]+$',
        message='Username hanya boleh berisi huruf, angka, spasi, dan karakter @/./+/-/_.'
    )
    
    username = models.CharField(
        max_length=150,
        unique=False,
        validators=[username_validator],
        error_messages={}
    )
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='siswa')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Field tambahan untuk siswa
    no_telp = models.CharField(max_length=15, null=True, blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    alamat = models.TextField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"