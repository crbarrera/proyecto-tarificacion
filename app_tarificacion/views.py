from django.shortcuts import redirect, render, get_object_or_404
from .models import Anexo, Codunidad, Ctapresu, Usuario, Proveedor
from .forms import AnexoForm, CuentaPresupuestariaForm, LoginForm, UsuarioForm, ProveedorForm, CodigoUnidadForm
from django.db import IntegrityError, connection, DatabaseError
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login, authenticate  
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import cx_Oracle
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.hashers import make_password

@login_required
def index(request):
    rol_user = None
    if request.user.is_authenticated:
        rol_user = request.user.rol_usuario  # Accede al rol del usuario autenticado
    
    return render(request, 'index.html', {'rol_user': rol_user})
  

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         # Autenticación del usuario
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             auth_login(request, user)  # Usamos auth_login en vez de login para evitar conflictos
#             return redirect(request.GET.get('next', 'home'))  # Redirigir a la página principal o a 'next'
#         else:
#             messages.error(request, 'Nombre de usuario o contraseña incorrectos.')

#     return render(request, 'iniciar_sesion.html')
  
class CustomLogoutView(LogoutView):
    next_page = 'login'  # Asegúrate de que 'login' esté definido en tus urls

@login_required
def listar_usuarios(request):
    query = request.GET.get('query', '')
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    if query:
        cursor.callproc('buscar_usuarios', [query, out_cur])
    else:
        cursor.callproc('listar_usuarios', [out_cur])

    usuarios = []

    for fila in out_cur:
        id_usuario, username, email_usuario, rol_usuario = fila
        usuarios.append({
            'id_usuario': id_usuario,
            'username': username,
            'email_usuario': email_usuario,
            'rol_usuario': rol_usuario
        })

    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})

@login_required
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            rol_usuario = form.cleaned_data['rol_usuario']
            email_usuario = form.cleaned_data['email_usuario']

            try:
                # Genera el hash de la contraseña con Django
                password_hashed = make_password(password)

                # Llama al procedimiento almacenado pasándole el hash de la contraseña
                with connection.cursor() as cursor:
                    cursor.callproc('crear_usuario', [username, password_hashed, rol_usuario, email_usuario])

                return redirect('usuarios')
            except DatabaseError as e:
                error_message = str(e)
                if 'ORA-20002' in error_message:
                    form.add_error('username', 'El nombre de usuario ya existe.')
                else:
                    form.add_error(None, 'Ocurrió un error al crear el usuario.')
    else:
        form = UsuarioForm()
    
    return render(request, 'crear_usuario.html', {'form': form})

@login_required
def modificar_usuario(request, id):
    # Obtiene el usuario actual basado en el ID proporcionado
    usuario_actual = get_object_or_404(Usuario, id_usuario=id)

    if request.method == 'POST':
        # Se pasa la instancia del usuario actual al formulario
        form = UsuarioForm(request.POST, instance=usuario_actual)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']  # Esto será vacío si no se cambia
            rol_usuario = form.cleaned_data['rol_usuario']
            email_usuario = form.cleaned_data['email_usuario']

            try:
                # Genera un nuevo hash solo si se proporciona una nueva contraseña
                if password:
                    password_hashed = make_password(password)
                else:
                    password_hashed = usuario_actual.password  # Mantiene el hash actual si no se cambia

                # Llama al procedimiento almacenado
                with connection.cursor() as cursor:
                    cursor.callproc('modificar_usuario', [
                        usuario_actual.id_usuario,
                        username,
                        password_hashed,  # Asegúrate de pasar el hash
                        rol_usuario,
                        email_usuario
                    ])
                
                return redirect('usuarios')  # Redirige a la lista de usuarios
            except DatabaseError as e:
                error_message = str(e)
                if 'ORA-20001' in error_message:
                    form.add_error('rol_usuario', 'Rol de usuario inválido.')
                else:
                    form.add_error(None, 'Ocurrió un error al modificar el usuario.')
    else:
        # Prepara el formulario con los datos actuales del usuario
        form = UsuarioForm(instance=usuario_actual)

    return render(request, 'modificar_usuario.html', {'form': form, 'usuario': usuario_actual})

@login_required
def eliminar_usuario(request, id):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.callproc('eliminar_usuario', [id])
            return redirect('usuarios')  # Redirige a la lista de usuarios después de eliminar
        except DatabaseError as e:
            # Manejo de errores si es necesario
            error_message = str(e)
            # Puedes manejar el error según lo necesites
            # Por ejemplo, agregar un mensaje de error a la sesión

    return redirect('usuarios')  # Redirige si la solicitud no es POST

@login_required
def listar_proveedores(request):
    query = request.GET.get('query', '')
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    if query:
        cursor.callproc('buscar_proveedores', [query, out_cur])
    else:
        cursor.callproc('listar_proveedores', [out_cur])

    proveedores = []

    for fila in out_cur:
        id_proveedor, nombre_proveedor, tarifa_cel, tarifa_slm, tarifa_ldi = fila
        proveedores.append({
            'id_proveedor': id_proveedor,
            'nombre_proveedor': nombre_proveedor,
            'tarifa_cel': tarifa_cel,
            'tarifa_slm': tarifa_slm,
            'tarifa_ldi': tarifa_ldi
        })

    return render(request, 'listar_proveedores.html', {'proveedores': proveedores})
  
@login_required
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            nombre_proveedor = form.cleaned_data['nombre_proveedor']
            tarifa_cel = form.cleaned_data['tarifa_cel']
            tarifa_slm = form.cleaned_data['tarifa_slm']
            tarifa_ldi = form.cleaned_data['tarifa_ldi']
            
            try:
                with connection.cursor() as cursor:
                    cursor.callproc('crear_proveedor', [nombre_proveedor, tarifa_cel, tarifa_slm, tarifa_ldi])
                return redirect('proveedores')
            except DatabaseError as e:
                form.add_error(None, 'Ocurrió un error al crear el proveedor.')
    else:
        form = ProveedorForm()
    
    return render(request, 'crear_proveedor.html', {'form': form})

@login_required
def modificar_proveedor(request, id):
    proveedor_actual = get_object_or_404(Proveedor, id_proveedor=id)

    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            nombre_proveedor = form.cleaned_data['nombre_proveedor']
            tarifa_cel = form.cleaned_data['tarifa_cel']
            tarifa_slm = form.cleaned_data['tarifa_slm']
            tarifa_ldi = form.cleaned_data['tarifa_ldi']

            try:
                with connection.cursor() as cursor:
                    cursor.callproc('modificar_proveedor', [proveedor_actual.id_proveedor, nombre_proveedor, tarifa_cel, tarifa_slm, tarifa_ldi])
                return redirect('proveedores')
            except DatabaseError as e:
                form.add_error(None, 'Ocurrió un error al modificar el proveedor.')
    else:
        initial_data = {
            'nombre_proveedor': proveedor_actual.nombre_proveedor,
            'tarifa_cel': proveedor_actual.tarifa_cel,
            'tarifa_slm': proveedor_actual.tarifa_slm,
            'tarifa_ldi': proveedor_actual.tarifa_ldi,
        }
        form = ProveedorForm(initial=initial_data)

    return render(request, 'modificar_proveedor.html', {'form': form, 'proveedor': proveedor_actual})

@login_required
def eliminar_proveedor(request, id):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.callproc('eliminar_proveedor', [id])
            return redirect('proveedores')
        except DatabaseError as e:
            # Manejo de errores si es necesario
            error_message = str(e)
            # Puedes manejar el error según lo necesites
            # Por ejemplo, agregar un mensaje de error a la sesión

    return redirect('proveedores')

@login_required
def listar_codigos_unidad(request):
    query = request.GET.get('query', '')
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    if query:
        cursor.callproc('buscar_codigos_unidad', [query, out_cur])
    else:
        cursor.callproc('listar_codigos_unidad', [out_cur])

    codigos_unidad = []

    for fila in out_cur:
        id_codigo, nombre_codigo, ctapresu_id = fila
        ctapresu = Ctapresu.objects.get(id_cuenta=ctapresu_id)
        codigos_unidad.append({
            'id_codigo': id_codigo,
            'nombre_codigo': nombre_codigo,
            'ctapresu': ctapresu.nombre_cuenta
        })

    return render(request, 'listar_codigos_unidad.html', {'codigos_unidad': codigos_unidad})

@login_required
def crear_codigo_unidad(request):
    if request.method == 'POST':
        form = CodigoUnidadForm(request.POST)
        if form.is_valid():
            nombre_codigo = form.cleaned_data['nombre_codigo']
            ctapresu_id = form.cleaned_data['ctapresu_id']
            
            try:
                with connection.cursor() as cursor:
                    cursor.callproc('crear_codigo_unidad', [nombre_codigo, ctapresu_id.id_cuenta])
                return redirect('codigos_unidad')
            except DatabaseError as e:
                form.add_error(None, 'Ocurrió un error al crear el código de unidad.')
        else:
            print(form.errors)  # Agrega esto para depurar errores de validación
    else:
        form = CodigoUnidadForm()
    
    return render(request, 'crear_codigo_unidad.html', {'form': form})

@login_required
def modificar_codigo_unidad(request, id):
    codigo_unidad_actual = get_object_or_404(Codunidad, id_codigo=id)

    if request.method == 'POST':
        form = CodigoUnidadForm(request.POST)
        if form.is_valid():
            nombre_codigo = form.cleaned_data['nombre_codigo']
            ctapresu_id = form.cleaned_data['ctapresu_id']

            try:
                with connection.cursor() as cursor:
                    cursor.callproc('modificar_codigo_unidad', [codigo_unidad_actual.id_codigo, nombre_codigo, ctapresu_id.id_cuenta])
                return redirect('codigos_unidad')
            except DatabaseError as e:
                form.add_error(None, 'Ocurrió un error al modificar el código de unidad.')
    else:
        initial_data = {
            'nombre_codigo': codigo_unidad_actual.nombre_codigo,
            'ctapresu_id': codigo_unidad_actual.ctapresu
        }
        form = CodigoUnidadForm(initial=initial_data)

    return render(request, 'modificar_codigo_unidad.html', {'form': form, 'codigo_unidad': codigo_unidad_actual})

@login_required
def eliminar_codigo_unidad(request, id):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.callproc('eliminar_codigo_unidad', [id])
            return redirect('codigos_unidad')
        except DatabaseError as e:
            # Manejo de errores si es necesario
            error_message = str(e)
            # Puedes manejar el error según lo necesites
            # Por ejemplo, agregar un mensaje de error a la sesión

    return redirect('codigos_unidad')

@login_required
def listar_cuentas_presupuestarias(request):
    query = request.GET.get('query', '')
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    if query:
        cursor.callproc('buscar_cuentas_presupuestarias', [query, out_cur])
    else:
        cursor.callproc('listar_cuentas_presupuestarias', [out_cur])

    cuentas_presupuestarias = []

    for fila in out_cur:
        id_cuenta, nombre_cuenta = fila
        cuentas_presupuestarias.append({
            'id_cuenta': id_cuenta,
            'nombre_cuenta': nombre_cuenta
        })

    return render(request, 'listar_cuentas_presupuestarias.html', {'cuentas_presupuestarias': cuentas_presupuestarias})

@login_required
def crear_cuenta_presupuestaria(request):
    if request.method == 'POST':
        form = CuentaPresupuestariaForm(request.POST)
        if form.is_valid():
            nombre_cuenta = form.cleaned_data['nombre_cuenta']
            
            try:
                with connection.cursor() as cursor:
                    cursor.callproc('crear_cuenta_presupuestaria', [nombre_cuenta])
                return redirect('cuentas_presupuestarias')
            except DatabaseError as e:
                form.add_error(None, 'Ocurrió un error al crear la cuenta presupuestaria.')
    else:
        form = CuentaPresupuestariaForm()
    
    return render(request, 'crear_cuenta_presupuestaria.html', {'form': form})

@login_required
def modificar_cuenta_presupuestaria(request, id):
    cuenta_actual = get_object_or_404(Ctapresu, id_cuenta=id)

    if request.method == 'POST':
        form = CuentaPresupuestariaForm(request.POST)
        if form.is_valid():
            nombre_cuenta = form.cleaned_data['nombre_cuenta']

            try:
                with connection.cursor() as cursor:
                    cursor.callproc('modificar_cuenta_presupuestaria', [cuenta_actual.id_cuenta, nombre_cuenta])
                return redirect('cuentas_presupuestarias')
            except DatabaseError as e:
                form.add_error(None, 'Ocurrió un error al modificar la cuenta presupuestaria.')
    else:
        initial_data = {
            'nombre_cuenta': cuenta_actual.nombre_cuenta,
        }
        form = CuentaPresupuestariaForm(initial=initial_data)

    return render(request, 'modificar_cuenta_presupuestaria.html', {'form': form, 'cuenta': cuenta_actual})

@login_required
def eliminar_cuenta_presupuestaria(request, id):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.callproc('eliminar_cuenta_presupuestaria', [id])
            return redirect('cuentas_presupuestarias')
        except DatabaseError as e:
            # Manejo de errores si es necesario
            error_message = str(e)
            # Puedes manejar el error según lo necesites
            # Por ejemplo, agregar un mensaje de error a la sesión

    return redirect('cuentas_presupuestarias')

@login_required
def listar_anexos(request):
    query = request.GET.get('query', '')
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    if query:
        cursor.callproc('buscar_anexos', [query, out_cur])
    else:
        cursor.callproc('listar_anexos', [out_cur])

    anexos = []

    for fila in out_cur:
        id_anexo, numero_anexo, cargo_fijo, estado_anexo, usuario_id, codunidad_id = fila
        usuario = Usuario.objects.get(id_usuario=usuario_id)
        codunidad = Codunidad.objects.get(id_codigo=codunidad_id)
        anexos.append({
            'id_anexo': id_anexo,
            'numero_anexo': numero_anexo,
            'cargo_fijo': cargo_fijo,
            'estado_anexo': estado_anexo,
            'usuario': usuario.username,
            'codunidad': codunidad.nombre_codigo
        })

    return render(request, 'listar_anexos.html', {'anexos': anexos})

@login_required
def crear_anexo(request):
    if request.method == 'POST':
        form = AnexoForm(request.POST)
        if form.is_valid():
            numero_anexo = form.cleaned_data['numero_anexo']
            cargo_fijo = form.cleaned_data['cargo_fijo']
            estado_anexo = form.cleaned_data['estado_anexo']
            usuario = form.cleaned_data['usuario_id']
            codunidad = form.cleaned_data['codunidad_id']
            
            try:
                with connection.cursor() as cursor:
                    cursor.callproc('crear_anexo', [numero_anexo, cargo_fijo, estado_anexo, usuario.id_usuario, codunidad.id_codigo])
                return redirect('anexos')
            except DatabaseError as e:
                form.add_error(None, 'Ocurrió un error al crear el anexo.')
        else:
            print(form.errors)  # Agrega esto para depurar errores de validación
    else:
        form = AnexoForm()
    
    return render(request, 'crear_anexo.html', {'form': form})

@login_required
def modificar_anexo(request, id):
    anexo_actual = get_object_or_404(Anexo, id_anexo=id)

    if request.method == 'POST':
        form = AnexoForm(request.POST)
        if form.is_valid():
            numero_anexo = form.cleaned_data['numero_anexo']
            cargo_fijo = form.cleaned_data['cargo_fijo']
            estado_anexo = form.cleaned_data['estado_anexo']
            usuario = form.cleaned_data['usuario_id']
            codunidad = form.cleaned_data['codunidad_id']

            try:
                with connection.cursor() as cursor:
                    cursor.callproc('modificar_anexo', [anexo_actual.id_anexo, numero_anexo, cargo_fijo, estado_anexo, usuario.id_usuario, codunidad.id_codigo])
                return redirect('anexos')
            except DatabaseError as e:
                form.add_error(None, 'Ocurrió un error al modificar el anexo.')
    else:
        initial_data = {
            'numero_anexo': anexo_actual.numero_anexo,
            'cargo_fijo': anexo_actual.cargo_fijo,
            'estado_anexo': anexo_actual.estado_anexo,
            'usuario_id': anexo_actual.usuario,
            'codunidad_id': anexo_actual.codunidad,
        }
        form = AnexoForm(initial=initial_data)

    return render(request, 'modificar_anexo.html', {'form': form, 'anexo': anexo_actual})

@login_required
def eliminar_anexo(request, id):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.callproc('eliminar_anexo', [id])
            return redirect('anexos')
        except DatabaseError as e:
            # Manejo de errores si es necesario
            error_message = str(e)
            # Puedes manejar el error según lo necesites
            # Por ejemplo, agregar un mensaje de error a la sesión

    return redirect('anexos')

@login_required
def listar_responsables_unidad(request):
    query = request.GET.get('query', '')
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    if query:
        cursor.callproc('buscar_responsables_unidad', [query, out_cur])
    else:
        cursor.callproc('listar_responsables_unidad', [out_cur])

    responsables = []

    for fila in out_cur:
        id_usuario, username, email_usuario, rol_usuario = fila
        responsables.append({
            'id_usuario': id_usuario,
            'username': username,
            'email_usuario': email_usuario,
            'rol_usuario': rol_usuario
        })

    return render(request, 'listar_responsables_unidad.html', {'responsables': responsables})

@login_required

def listar_anexos_activos(request):
    query = request.GET.get('query', '')
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    if query:
        cursor.callproc('buscar_anexos_activos', [query, out_cur])
    else:
        cursor.callproc('listar_anexos_activos', [out_cur])

    anexos = []

    for fila in out_cur:
        id_anexo, numero_anexo, cargo_fijo, estado_anexo, usuario_id, codunidad_id = fila
        usuario = Usuario.objects.get(id_usuario=usuario_id)
        codunidad = Codunidad.objects.get(id_codigo=codunidad_id)
        anexos.append({
            'id_anexo': id_anexo,
            'numero_anexo': numero_anexo,
            'cargo_fijo': cargo_fijo,
            'estado_anexo': estado_anexo,
            'usuario': usuario.username,
            'codunidad': codunidad.nombre_codigo
        })

    return render(request, 'listar_anexos_activos.html', {'anexos': anexos})
