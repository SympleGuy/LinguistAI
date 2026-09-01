from django.core.management.base import BaseCommand
from django.db.models import Q
from myapp.models import User as AppUser


class Command(BaseCommand):
    help = "Set role for a LinguistAI user (e.g. 'admin' or 'user')"

    def add_arguments(self, parser):
        parser.add_argument("identifier", type=str, help="Username, Email, or UUID of the user")
        parser.add_argument("role", type=str, nargs="?", default="admin", choices=["admin", "user"], help="Role to assign: 'admin' or 'user' (default: admin)")

    def handle(self, *args, **options):
        identifier = options["identifier"].strip()
        role = options["role"].strip().lower()

        user = AppUser.objects.filter(
            Q(email__iexact=identifier) | Q(username__iexact=identifier) | Q(id__icontains=identifier)
        ).first()

        if not user:
            self.stdout.write(self.style.ERROR(f"User with identifier '{identifier}' not found in database."))
            return

        user.role = role
        user.save()

        self.stdout.write(self.style.SUCCESS(
            f"Successfully updated user '{user.username}' ({user.email}) to role: {role.upper()}"
        ))
