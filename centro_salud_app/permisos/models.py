from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    CARGO_CHOICES = [
        ('Dentista', 'Dentista'),
        ('Medico', 'Médico'),
        ('Quimico-Farmaceutico', 'Químico-Farmacéutico'),
        ('Asistente Social', 'Asistente Social'),
        ('Enfermera', 'Enfermera'),
        ('Kinesiologo', 'Kinesiólogo'),
        ('Matrona', 'Matrona'),
        ('Nutricionista', 'Nutricionista'),
        ('Psicologo', 'Psicólogo'),
        ('Tecnologo Medico', 'Tecnólogo Médico'),
        ('Fonoaudiologo', 'Fonoaudiólogo'),
        ('Terapeuta Ocupacional', 'Terapeuta Ocupacional'),
        ('Educadora de Parvulos', 'Educadora de Párvulos'),
        ('Profesor de Educacion Fisica', 'Profesor de Educación Física'),
        ('Abogado', 'Abogado'),
        ('Ingeniero en Informatica', 'Ingeniero en Informática'),
        ('Ingeniero en Prevencion de Riesgos', 'Ingeniero en Prevención de Riesgos'),
        ('Ingeniero en Administracion de Empresas', 'Ingeniero en Administración de Empresas'),
        ('Ingeniero Comercial', 'Ingeniero Comercial'),
        ('Contador Auditor', 'Contador Auditor'),
        ('TENS Enfermeria', 'TENS (Enfermería)'),
        ('TANS Administracion', 'TANS (Administración)'),
        ('Podologo', 'Podólogo'),
        ('Estadistico', 'Estadístico'),
        ('Programador', 'Programador/ Técnico en Computación'),
        ('Paramedico', 'Paramédico'),
        ('Secretaria', 'Secretaria'),
        ('Administrativos de Salud', 'Administrativos de Salud'),
        ('Auxiliar de Servicio', 'Auxiliar de Servicio'),
        ('Conductor', 'Conductor'),
        ('Estafeta', 'Estafeta'),
        ('Director de Consultorio', 'Director de Consultorio (CESFAM Arrau Méndez)'),
        ('Director de Departamento de Salud Municipal', 'Director de Departamento de Salud Municipal'),
    ]
    
    DEPARTAMENTO_CHOICES = [
        ('Posta de Salud Rural Villa Baviera', 'Posta de Salud Rural Villa Baviera'),
        ('Posta de Salud Rural Los Canelos', 'Posta de Salud Rural Los Canelos'),
        ('Posta de Salud Rural Bullileo', 'Posta de Salud Rural Bullileo'),
        ('Posta de Salud Rural Bajos de Huenutil', 'Posta de Salud Rural Bajos de Huenutil'),
        ('Posta de Salud Rural Catillo', 'Posta de Salud Rural Catillo'),
        ('Posta de Salud Rural Digua', 'Posta de Salud Rural Digua'),
        ('Posta de Salud Rural Monte Flor', 'Posta de Salud Rural Monte Flor'),
        ('Posta de Salud Rural San Alejo', 'Posta de Salud Rural San Alejo'),
        ('Posta de Salud Rural Talquita', 'Posta de Salud Rural Talquita'),
        ('Posta de Salud Rural Los Carros', 'Posta de Salud Rural Los Carros'),
        ('Posta de Salud Rural Perquilauquén', 'Posta de Salud Rural Perquilauquén'),
        ('Posta de Salud Rural La Orilla', 'Posta de Salud Rural La Orilla'),
        ('Posta de Salud Rural Fuerte Viejo', 'Posta de Salud Rural Fuerte Viejo'),
        ('Centro Comunitario de Salud Familiar Los Olivos', 'Centro Comunitario de Salud Familiar Los Olivos'),
        ('Centro de Salud Familiar Arrau Méndez', 'Centro de Salud Familiar Arrau Méndez'),
        ('SAR', 'SAR'),
        ('Hospital San José', 'Hospital San José'),
        ('Centro Comunitario de Salud Familiar Buenos Aires', 'Centro Comunitario de Salud Familiar Buenos Aires'),
        ('Departamento de Salud Municipal Parral', 'Departamento de Salud Municipal Parral'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField("Nombre completo", max_length=100)
    rut = models.CharField("RUT", max_length=12)
    position = models.CharField("Cargo", max_length=50, choices=CARGO_CHOICES, null=True, blank=True)
    establishment = models.CharField("Establecimiento", max_length=100, choices=DEPARTAMENTO_CHOICES, null=True, blank=True)
    permissions = models.CharField("Permisos", max_length=100, null=True, blank=True)
    firma = models.ImageField("Firma", upload_to='firmas/', null=True, blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"


class PermissionRequest(models.Model):
    CARGO_CHOICES = UserProfile.CARGO_CHOICES
    DEPARTAMENTO_CHOICES = UserProfile.DEPARTAMENTO_CHOICES
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado')
    ]
    REQUEST_TYPE_CHOICES = [
        ('FERIADO', 'Solicitud de Feriado Legal'),
        ('ADMINISTRATIVO', 'Permiso Administrativo'),
        ('COMPENSACION', 'Compensación de Tiempo')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField("Nombre completo", max_length=100)
    rut = models.CharField("RUT", max_length=12)
    position = models.CharField("Cargo", max_length=50, choices=CARGO_CHOICES)
    establishment = models.CharField("Establecimiento", max_length=50, choices=DEPARTAMENTO_CHOICES)
    request_type = models.CharField("Tipo de Solicitud", max_length=20, choices=REQUEST_TYPE_CHOICES, default='FERIADO')
    number_of_days = models.PositiveIntegerField("Número de días")
    date_from = models.DateField("Fecha desde")
    date_to = models.DateField("Fecha hasta")
    period = models.CharField("Periodo", max_length=20)

    autorizado = models.BooleanField("Autorizado", default=False)
    anticipado = models.BooleanField("Anticipado", default=False)
    postergado = models.BooleanField("Postergado", default=False)
    additional_date_from = models.DateField("Fecha desde", null=True, blank=True)
    additional_date_to = models.DateField("Fecha hasta", null=True, blank=True)
    firma_funcionario = models.FileField("Firma del funcionario", upload_to='firmas/', null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.number_of_days} días desde {self.date_from} - Estado: {self.estado}"


class PermissionRequestAdmin(models.Model):
    CARGO_CHOICES = UserProfile.CARGO_CHOICES
    DEPARTAMENTO_CHOICES = UserProfile.DEPARTAMENTO_CHOICES
    JORNADA_CHOICES = [
        ('Completa', 'Completa'),
        ('Mañana', 'Mañana'),
        ('Tarde', 'Tarde')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField("Nombre completo", max_length=100)
    rut = models.CharField("RUT", max_length=12)
    position = models.CharField("Cargo", max_length=50, choices=CARGO_CHOICES)
    establishment = models.CharField("Establecimiento", max_length=100, choices=DEPARTAMENTO_CHOICES)
    number_of_days = models.PositiveIntegerField("Número de días")
    date_from = models.DateField("Fecha desde")
    date_to = models.DateField("Fecha hasta")
    jornada = models.CharField("Jornada", max_length=50, choices=JORNADA_CHOICES, default='Completa')
    firma_funcionario = models.ImageField("Firma del funcionario", upload_to='firmas/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.position}"


class CompensationRequest(models.Model):
    CARGO_CHOICES = UserProfile.CARGO_CHOICES
    DEPARTAMENTO_CHOICES= UserProfile.DEPARTAMENTO_CHOICES

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField("Nombre completo", max_length=100)
    rut = models.CharField("RUT", max_length=12)
    position = models.CharField("Cargo", max_length=50, choices=CARGO_CHOICES)
    establishment = models.CharField("Establecimiento", max_length=100, choices=DEPARTAMENTO_CHOICES)

    number_of_hours = models.PositiveIntegerField("Número de horas")
    date_from = models.DateField("Fecha desde")
    date_to = models.DateField("Fecha hasta")
    time_from = models.TimeField("Horario desde")
    time_to = models.TimeField("Horario hasta")
    firma_funcionario = models.FileField("Firma del funcionario", upload_to='firmas/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.number_of_hours} horas desde {self.date_from}"


class Permission(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('feriado', 'Solicitud de Feriado Legal'),
        ('administrativo', 'Permiso Administrativo'),
        ('compensacion', 'Compensación de Tiempo'),
    ]

    full_name = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)
    date_from = models.DateField()
    date_to = models.DateField()
    estado = models.CharField(max_length=20, default='pendiente')
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES, default='FERIADO')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.get_request_type_display()}"
