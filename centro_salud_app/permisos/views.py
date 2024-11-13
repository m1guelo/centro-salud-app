from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from weasyprint import HTML
import os

from .forms import (
    UserRegisterForm,
    UserPermissionRequestForm,
    AdminPermissionForm,
    AdminPermissionRequestForm,
    CompensationRequestForm,
    UserProfileForm,
)
from .models import (
    PermissionRequest,
    PermissionRequestAdmin,
    CompensationRequest,
    UserProfile,
)

# Función para verificar si el usuario es administrador
def is_admin(user):
    return user.is_staff

@login_required
def home(request):
    return render(request, "home.html")

# ----------------------------
# Autenticación
# ----------------------------

def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm()})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "signin.html",
                {
                    "form": AuthenticationForm(),
                    "error": "El nombre de usuario o contraseña es incorrecto.",
                },
            )
        else:
            login(request, user)
            profile, created = UserProfile.objects.get_or_create(user=user)
            if not profile.full_name or not profile.rut or not profile.firma:
                return redirect("complete_profile")
            return redirect("home")

@login_required
def signout(request):
    logout(request)
    messages.info(request, "Haz cerrado sesión.")
    return redirect("signin")

# ----------------------------
# Perfil de usuario y gestión
# ----------------------------

@login_required
def complete_profile(request):
    profile = request.user.userprofile
    if profile.full_name and profile.rut and profile.firma:
        return redirect("home")

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = UserProfileForm(instance=profile)

    return render(request, "complete_profile.html", {"form": form})

@login_required
@user_passes_test(is_admin)
def user_management(request):
    users = UserProfile.objects.select_related('user').all()
    return render(request, "user_management.html", {"users": users})

@login_required
@user_passes_test(is_admin)
def create_user(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_staff = form.cleaned_data["user_type"] == "admin"
                user.save()
                UserProfile.objects.create(user=user)
                messages.success(
                    request, f"Usuario {user.username} creado exitosamente."
                )
                return redirect("user_management")
            except IntegrityError:
                return render(
                    request,
                    "register.html",
                    {"form": form, "error": "El nombre de usuario ya existe."},
                )
    else:
        form = UserRegisterForm()
    return render(request, "create_user.html", {"form": form})

@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = UserRegisterForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user_management")
    else:
        form = UserRegisterForm(instance=user)
    return render(request, "edit_user.html", {"form": form})

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.delete()
        return redirect("user_management")
    return render(request, "delete_user.html", {"user": user})

# Vista de registro de usuarios para administradores
@login_required
@user_passes_test(is_admin)
def signup(request):
    if request.method == "GET":
        return render(request, "register.html", {"form": UserRegisterForm()})
    else:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_staff = form.cleaned_data["user_type"] == "admin"
                user.save()
                messages.success(
                    request, f"Usuario {user.username} creado exitosamente."
                )
                return redirect("user_management")
            except IntegrityError:
                return render(
                    request,
                    "register.html",
                    {"form": form, "error": "El nombre de usuario ya existe."},
                )
        else:
            return render(
                request,
                "register.html",
                {"form": form, "error": "Las contraseñas no coinciden."},
            )

# ----------------------------
# Solicitudes de permisos
# ----------------------------

@login_required
def request_permission(request):
    if request.method == "POST":
        form = UserPermissionRequestForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            permission_request = form.save(commit=False)
            permission_request.user = request.user
            permission_request.save()
            messages.success(
                request, "Su solicitud de permiso ha sido enviada exitosamente."
            )
            return redirect("home")
    else:
        form = UserPermissionRequestForm(user=request.user)
    return render(request, "request_permission.html", {"form": form})

@login_required
def admin_permission_request(request):
    if request.method == "POST":
        form = AdminPermissionRequestForm(
            request.POST, request.FILES, user=request.user
        )
        if form.is_valid():
            permission_request = form.save(commit=False)
            permission_request.user = request.user
            permission_request.save()
            messages.success(
                request,
                "Su solicitud de permiso administrativo ha sido enviada exitosamente.",
            )
            return redirect("home")
    else:
        form = AdminPermissionRequestForm(user=request.user)
    return render(request, "admin_permission_request.html", {"form": form})

@login_required
def compensation_request(request):
    if request.method == "POST":
        form = CompensationRequestForm(request.POST, request.FILES)
        if form.is_valid():
            compensation_request = form.save(commit=False)
            compensation_request.user = request.user
            compensation_request.save()
            messages.success(
                request,
                "Su solicitud de compensación de tiempo ha sido enviada exitosamente.",
            )
            return redirect("home")
    else:
        form = CompensationRequestForm()
    return render(request, "compensation_request.html", {"form": form})

# ----------------------------
# Listados y detalles de permisos
# ----------------------------

@login_required
@user_passes_test(is_admin)
def regular_permission_list(request):
    query = request.GET.get("q", "")
    regular_permissions = PermissionRequest.objects.filter(
        Q(full_name__icontains=query) | Q(rut__icontains=query)
    )
    return render(request, "regular_permission_list.html", {"regular_permissions": regular_permissions, "query": query})

@login_required
@user_passes_test(is_admin)
def admin_permission_list(request):
    query = request.GET.get("q", "")
    admin_permissions = PermissionRequestAdmin.objects.filter(
        Q(full_name__icontains=query) | Q(rut__icontains=query)
    )
    return render(
        request,
        "admin_permission_list.html",
        {"admin_permissions": admin_permissions, "query": query},
    )

@login_required
@user_passes_test(is_admin)
def compensation_request_list(request):
    query = request.GET.get("q", "")
    compensation_requests = CompensationRequest.objects.filter(
        Q(full_name__icontains=query) | Q(rut__icontains=query)
    )
    return render(
        request,
        "compensation_request_list.html",
        {"compensation_requests": compensation_requests, "query": query},
    )

@login_required
def user_permission_status(request, tipo=None):
    if tipo == 'FERIADO':
        permissions = PermissionRequest.objects.filter(user=request.user, request_type='FERIADO')
    elif tipo == 'ADMINISTRATIVO':
        permissions = PermissionRequest.objects.filter(user=request.user, request_type='ADMINISTRATIVO')
    elif tipo == 'COMPENSACION':
        permissions = PermissionRequest.objects.filter(user=request.user, request_type='COMPENSACION')
    else:
        # Filtrar todas las solicitudes si no se especifica un tipo
        permissions = PermissionRequest.objects.filter(user=request.user)
    return render(request, 'user_permission_status.html', {'permissions': permissions})

@login_required
@user_passes_test(is_admin)
def regular_permission_detail(request, permission_id):
    permission = get_object_or_404(PermissionRequest, id=permission_id)
    if request.method == "POST":
        form = AdminPermissionForm(request.POST, request.FILES, instance=permission)
        if form.is_valid():
            permission.estado = "completado"
            form.save()
            messages.success(request, "La solicitud de permiso ha sido completada.")
            return redirect("regular_permission_list")
    else:
        form = AdminPermissionForm(instance=permission)
    return render(request, "regular_permission_detail.html", {"form": form, "permission": permission})

@login_required
@user_passes_test(is_admin)
def admin_permission_admin_detail(request, permission_id):
    permission = get_object_or_404(PermissionRequestAdmin, id=permission_id)
    if request.method == "POST":
        form = AdminPermissionForm(request.POST, request.FILES, instance=permission)
        if form.is_valid():
            form.save()
            messages.success(
                request, "La solicitud de permiso administrativo ha sido actualizada."
            )
            return redirect("admin_permission_list")
    else:
        form = AdminPermissionForm(instance=permission)
    return render(
        request,
        "admin_permission_admin_detail.html",
        {"form": form, "permission": permission},
    )
    
@login_required
@user_passes_test(is_admin)
def admin_permission_detail(request, permission_id):
    permission = get_object_or_404(PermissionRequest, id=permission_id)
    if request.method == "POST":
        form = AdminPermissionForm(request.POST, request.FILES, instance=permission)
        if form.is_valid():
            permission.estado = "completado"  # Cambia el estado a "completado"
            form.save()
            messages.success(request, "La solicitud de permiso ha sido completada.")
            return redirect("regular_permission_list")
    else:
        form = AdminPermissionForm(instance=permission)
    return render(
        request,
        "admin_permission_detail.html",
        {"form": form, "permission": permission},
    )


@login_required
@user_passes_test(is_admin)
def compensation_request_detail(request, request_id):
    compensation_request = get_object_or_404(CompensationRequest, id=request_id)
    if request.method == "POST":
        form = AdminPermissionForm(request.POST, request.FILES, instance=compensation_request)
        if form.is_valid():
            form.save()
            messages.success(request, "La solicitud de compensación de tiempo ha sido actualizada.")
            return redirect("compensation_request_list")
    else:
        form = AdminPermissionForm(instance=compensation_request)
    return render(
        request,
        "compensation_request_detail.html",
        {"form": form, "compensation_request": compensation_request},
    )

# ----------------------------
# Generación de PDFs
# ----------------------------

@login_required
def generate_user_permission_pdf(request, permission_id):
    permission = get_object_or_404(PermissionRequest, id=permission_id, user=request.user)
    html_string = render_to_string('permission_pdf_template.html', {'permission': permission})
    
    temp_dir = os.path.join(os.path.dirname(__file__), 'temp_files')
    os.makedirs(temp_dir, exist_ok=True)
    temp_pdf_path = os.path.join(temp_dir, f"Solicitud_{permission_id}_usuario.pdf")
    
    if os.path.isfile(temp_pdf_path):
        os.remove(temp_pdf_path)

    HTML(string=html_string).write_pdf(temp_pdf_path)
    with open(temp_pdf_path, "rb") as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Solicitud_{permission_id}.pdf"'
        return response

@login_required
@user_passes_test(is_admin)
def generate_permission_pdf(request, permission_id):
    permission = get_object_or_404(PermissionRequest, id=permission_id)
    html_string = render_to_string('permission_pdf_template.html', {'permission': permission})
    
    temp_dir = os.path.join(os.path.dirname(__file__), 'temp_files')
    os.makedirs(temp_dir, exist_ok=True)
    temp_pdf_path = os.path.join(temp_dir, f"Solicitud_{permission_id}_admin.pdf")
    
    if os.path.isfile(temp_pdf_path):
        os.remove(temp_pdf_path)

    HTML(string=html_string).write_pdf(temp_pdf_path)
    with open(temp_pdf_path, "rb") as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Solicitud_{permission_id}_admin.pdf"'
        return response


@login_required
def user_permission_status_feriado(request):
    permissions = PermissionRequest.objects.filter(user=request.user, request_type='FERIADO')
    return render(request, "user_permission_status.html", {"permissions": permissions})

@login_required
def user_permission_status_administrativo(request):
    permissions = PermissionRequest.objects.filter(user=request.user, request_type='ADMINISTRATIVO')
    return render(request, "user_permission_status.html", {"permissions": permissions})

@login_required
def user_permission_status_compensacion(request):
    permissions = PermissionRequest.objects.filter(user=request.user, request_type='COMPENSACION')
    return render(request, "user_permission_status.html", {"permissions": permissions})