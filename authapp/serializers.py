from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    no_telp = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tanggal_lahir = serializers.DateField(required=False, allow_null=True)
    alamat = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'role', 
                  'no_telp', 'tanggal_lahir', 'alamat')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Validasi field tambahan untuk siswa
        if attrs.get('role') == 'siswa':
            if not attrs.get('no_telp'):
                raise serializers.ValidationError({"no_telp": "Nomor telepon wajib diisi untuk siswa."})
            if not attrs.get('tanggal_lahir'):
                raise serializers.ValidationError({"tanggal_lahir": "Tanggal lahir wajib diisi untuk siswa."})
            if not attrs.get('alamat'):
                raise serializers.ValidationError({"alamat": "Alamat wajib diisi untuk siswa."})
                
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role'],
            password=validated_data['password']
        )
        
        # Simpan field tambahan untuk siswa
        if validated_data.get('role') == 'siswa':
            user.no_telp = validated_data.get('no_telp')
            user.tanggal_lahir = validated_data.get('tanggal_lahir')
            user.alamat = validated_data.get('alamat')
            user.save()
            
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role',
                 'no_telp', 'tanggal_lahir', 'alamat')