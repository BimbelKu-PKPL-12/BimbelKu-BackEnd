from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Bimbel(models.Model):
    nama = models.CharField(max_length=255)
    lokasi = models.CharField(max_length=255)
    kuota_awal = models.PositiveIntegerField()
    sisa_kuota = models.PositiveIntegerField()
    deskripsi = models.TextField(blank=True, null=True)
    harga = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bimbels')
    
    def __str__(self):
        return self.nama
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Bimbel"
        verbose_name_plural = "Bimbel"