from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from apps.custom_user.models import Role  # Ajusta según tu estructura

class Command(BaseCommand):
    help = 'Crea un superusuario con nombre, apellido y rol'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, required=True)
        parser.add_argument('--password', type=str, required=True)
        parser.add_argument('--name', type=str, required=True)
        parser.add_argument('--last_name', type=str, required=True)
        parser.add_argument('--role_id', type=int, required=True)

    def handle(self, *args, **options):
        User = get_user_model()
        email = options['email']
        password = options['password']
        name = options['name']
        last_name = options['last_name']
        role_id = options['role_id']

        if User.objects.filter(email=email).exists():
            raise CommandError(f'El usuario con correo {email} ya existe.')

        try:
            role = Role.objects.get(role_id=role_id)
        except Role.DoesNotExist:
            raise CommandError(f'No existe un rol con role_id={role_id}')

        user = User.objects.create_superuser(
            email=email,
            password=password,
            name=name,
            last_name=last_name,
            role_id=role  # 👈 Pasas la instancia, no el entero
        )

        self.stdout.write(self.style.SUCCESS(f'Superusuario {email} creado correctamente.'))
