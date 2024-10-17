from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models

class Ctapresu(models.Model):
    id_cuenta = models.AutoField(primary_key=True)
    nombre_cuenta = models.CharField(max_length=30)
    def __str__(self):
        return self.nombre_cuenta

class Codunidad(models.Model):
    id_codigo = models.AutoField(primary_key=True)
    nombre_codigo = models.CharField(max_length=30)
    ctapresu = models.ForeignKey(Ctapresu, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_codigo

class UsuarioManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('El nombre de usuario debe ser proporcionado')

        # Crea la instancia del usuario
        user = self.model(username=username, **extra_fields)
        
        # Encripta la contraseña
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)  # Este campo es manejado por AbstractBaseUser
    rol_usuario = models.CharField(max_length=30)
    email_usuario = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class Anexo(models.Model):
    id_anexo = models.AutoField(primary_key=True)
    numero_anexo = models.IntegerField()
    cargo_fijo = models.DecimalField(max_digits=10, decimal_places=2)
    estado_anexo = models.CharField(max_length=30)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    codunidad = models.ForeignKey(Codunidad, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.numero_anexo)

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre_proveedor = models.CharField(max_length=30)
    tarifa_cel = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tarifa_slm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tarifa_ldi = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.nombre_proveedor

class Llamada(models.Model):
    id_llamada = models.AutoField(primary_key=True)
    origen_llamada = models.IntegerField()
    destino_llamada = models.IntegerField()
    identificador_llamada = models.IntegerField()
    app_llamada = models.CharField(max_length=30)
    inicio_llamada = models.DateTimeField()
    duracion_llamada = models.IntegerField()
    segundos_facturados = models.IntegerField()
    disposicion = models.CharField(max_length=30)
    tipo_llamada = models.CharField(max_length=20)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    anexo = models.ForeignKey(Anexo, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_llamada)

class Tarificacion(models.Model):
    id_tarificacion = models.AutoField(primary_key=True)
    fecha_inicio = models.DateTimeField()
    fecha_termino = models.DateTimeField()
    costo_total = models.DecimalField(max_digits=12, decimal_places=2)
    minutos_totales = models.IntegerField()
    tipo_llamada = models.CharField(max_length=20)
    anexo = models.ForeignKey(Anexo, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_tarificacion)

