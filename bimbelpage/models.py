from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Model User lokal untuk menyimpan data dasar user dari auth service
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
    
    class Meta:
        swappable = 'AUTH_USER_MODEL'


class Bimbel(models.Model):
    nama = models.CharField(max_length=255)
    lokasi = models.CharField(max_length=255)
    kuota_awal = models.PositiveIntegerField()
    sisa_kuota = models.PositiveIntegerField()
    deskripsi = models.TextField(blank=True, null=True)
    harga = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_approved = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bimbels')
    
    def __str__(self):
        return self.nama
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Bimbel"
        verbose_name_plural = "Bimbel"