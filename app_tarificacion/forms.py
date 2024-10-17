# forms.py
from django import forms
from .models import Codunidad, Ctapresu, Usuario

class UsuarioForm(forms.ModelForm):
    ROLES = [
        ('Responsable de Unidad', 'Responsable de Unidad'),
        ('Administrador', 'Administrador'),
    ]
    
    password = forms.CharField(widget=forms.PasswordInput, required=False, label='Contraseña')  # Permitir que la contraseña sea opcional
    
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'rol_usuario', 'email_usuario']
    
    rol_usuario = forms.ChoiceField(choices=ROLES, label='Rol de Usuario')

    
class ProveedorForm(forms.Form):
    nombre_proveedor = forms.CharField(max_length=30, label='Nombre del Proveedor')
    tarifa_cel = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label='Tarifa Celular')
    tarifa_slm = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label='Tarifa SLM')
    tarifa_ldi = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label='Tarifa LDI')

class CodigoUnidadForm(forms.Form):
    nombre_codigo = forms.CharField(max_length=30, label='Nombre del Código')
    ctapresu_id = forms.ModelChoiceField(queryset=Ctapresu.objects.all(), label='Cuenta Presupuestaria', to_field_name='nombre_cuenta')
    
class CuentaPresupuestariaForm(forms.Form):
    nombre_cuenta = forms.CharField(max_length=30, label='Nombre de la Cuenta Presupuestaria')
    
class AnexoForm(forms.Form):
    ESTADOS = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]

    numero_anexo = forms.IntegerField(label='Número de Anexo')
    cargo_fijo = forms.DecimalField(max_digits=10, decimal_places=2, label='Cargo Fijo')
    estado_anexo = forms.ChoiceField(choices=ESTADOS, label='Estado del Anexo')
    usuario_id = forms.ModelChoiceField(queryset=Usuario.objects.all(), label='Usuario', to_field_name='username')
    codunidad_id = forms.ModelChoiceField(queryset=Codunidad.objects.all(), label='Código Unidad', to_field_name='nombre_codigo')
    

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label='Nombre de Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')