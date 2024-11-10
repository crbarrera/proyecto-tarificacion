"""
URL configuration for tarificacion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app_tarificacion import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('login/', auth_views.LoginView.as_view(template_name='iniciar_sesion.html'), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('proveedores/', views.listar_proveedores, name = 'proveedores'),
    path('proveedores/crear/', views.crear_proveedor, name = 'crear_proveedor'),
    path('proveedores/<int:id>/', views.modificar_proveedor, name = 'modificar_proveedor'),
    path('proveedores/<int:id>/eliminar', views.eliminar_proveedor, name = 'eliminar_proveedor'),
    path('usuarios/', views.listar_usuarios, name = 'usuarios'),
    path('usuarios/crear', views.crear_usuario, name='crear_usuario'),
    path('usuarios/<int:id>/', views.modificar_usuario, name='modificar_usuario'),
    path('usuarios/<int:id>/eliminar', views.eliminar_usuario, name = 'eliminar_usuario'),
    path('codigos_unidad/', views.listar_codigos_unidad, name = 'codigos_unidad'),
    path('codigos_unidad/crear/', views.crear_codigo_unidad, name = 'crear_codigo_unidad'),
    path('codigos_unidad/<int:id>/', views.modificar_codigo_unidad, name = 'modificar_codigo_unidad'),
    path('codigos_unidad/<int:id>/eliminar', views.eliminar_codigo_unidad, name = 'eliminar_codigo_unidad'),
    path('cuentas_presupuestarias/', views.listar_cuentas_presupuestarias, name = 'cuentas_presupuestarias'),
    path('cuentas_presupuestarias/crear/', views.crear_cuenta_presupuestaria, name = 'crear_cuenta_presupuestaria'),
    path('cuentas_presupuestarias/<int:id>/', views.modificar_cuenta_presupuestaria, name = 'modificar_cuenta_presupuestaria'),
    path('cuentas_presupuestarias/<int:id>/eliminar', views.eliminar_cuenta_presupuestaria, name = 'eliminar_cuenta_presupuestaria'),
    path('anexos/', views.listar_anexos, name = 'anexos'),
    path('anexos/crear/', views.crear_anexo, name = 'crear_anexo'),
    path('anexos/<int:id>/', views.modificar_anexo, name = 'modificar_anexo'),
    path('anexos/<int:id>/eliminar', views.eliminar_anexo, name = 'eliminar_anexo'),
    path('responsables_unidad/', views.listar_responsables_unidad, name = 'listar_responsables_unidad'),
    path('anexos_activos/', views.listar_anexos_activos, name = 'listar_anexos_activos'),
    path('calcular_tarificacion/', views.calcular_tarificacion, name='calcular_tarificacion'),
    path('consultar_tarificacion_anexo/', views.consultar_tarificacion_anexo, name='consultar_tarificacion_anexo'),
    path('consultar_tarificacion_codigo/', views.consultar_tarificacion_codigo, name='consultar_tarificacion_codigo'),
    path('tarificacion/<int:id_tarificacion>/', views.detalle_tarificacion, name='detalle_tarificacion'),
    path('generar_reporte_pdf/<int:id_tarificacion>/', views.generar_reporte_pdf, name='generar_reporte_pdf'),
    path('enviar_reporte/<int:id_tarificacion>/', views.enviar_reporte, name='enviar_reporte'),
    path('reporte_general/', views.reporte_general, name='reporte_general'),
    path('generar_reportes/', views.generar_reportes, name='generar_reportes'),
    path('enviar_reporte_general/', views.enviar_reporte_general, name='enviar_reporte_general'),
    path('reporte_responsable/<str:username>/', views.generar_reporte_responsable_pdf, name='reporte_responsable_pdf'),
    path('consultar_trafico_por_proveedor/', views.consultar_trafico_por_proveedor, name='consultar_trafico_por_proveedor'),
    path('generar_reporte_xls/<int:id_tarificacion>/', views.generar_reporte_xls, name='generar_reporte_xls'),
    path('reporte_general_xls/', views.reporte_general_xls, name='reporte_general_xls'),
    path('reporte_responsable_xls/<str:username>/', views.generar_reporte_responsable_xls, name='reporte_responsable_xls'),
]
