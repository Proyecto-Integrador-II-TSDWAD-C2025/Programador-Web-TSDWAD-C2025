"""Alta explicita y privada de una cuenta administradora de la aplicacion."""

import getpass
import sys

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email
from django.db import transaction

from api.models import Rol, Usuario


class Command(BaseCommand):
    help = 'Crea una cuenta de pruebas con rol administrador, sin privilegios Django.'

    def add_arguments(self, parser):
        parser.add_argument('--email', required=True)
        parser.add_argument('--nombre', default='Equipo')
        parser.add_argument('--apellido', default='Pruebas')

    def handle(self, *args, **options):
        email = Usuario.objects.normalize_email(options['email'].strip())
        try:
            validate_email(email)
        except ValidationError:
            raise CommandError('Indica un email valido.') from None

        if Usuario.objects.filter(email__iexact=email).exists():
            raise CommandError('La cuenta ya existe; no se modifico su rol ni contrasena.')
        if not sys.stdin.isatty():
            raise CommandError('Usa una terminal interactiva para ingresar la contrasena sin eco.')

        password = getpass.getpass('Contrasena privada (no se mostrara): ')
        confirmation = getpass.getpass('Repetir contrasena: ')
        if password != confirmation:
            raise CommandError('Las contrasenas no coinciden; no se creo la cuenta.')
        if not (
            len(password) >= 12
            and any(c.isupper() for c in password)
            and any(c.islower() for c in password)
            and any(c.isdigit() for c in password)
            and any(not c.isalnum() and not c.isspace() for c in password)
        ):
            raise CommandError('Usa al menos 12 caracteres con mayuscula, minuscula, numero y simbolo.')

        user = Usuario(email=email, nombre=options['nombre'], apellido=options['apellido'])
        try:
            validate_password(password, user=user)
        except ValidationError as error:
            raise CommandError(' '.join(error.messages)) from None

        with transaction.atomic():
            # Nunca convertir ni sobrescribir silenciosamente una cuenta existente.
            if Usuario.objects.filter(email__iexact=email).exists():
                raise CommandError('La cuenta ya existe; no se modifico.')
            role, _ = Rol.objects.get_or_create(nombre_rol='administrador')
            Usuario.objects.create_user(
                email=email, password=password, nombre=user.nombre, apellido=user.apellido,
                id_rol=role, is_active=True, is_staff=False, is_superuser=False,
            )
        self.stdout.write(self.style.SUCCESS(
            'Cuenta de pruebas creada con rol administrador. No se genero ni mostro un token.'
        ))
