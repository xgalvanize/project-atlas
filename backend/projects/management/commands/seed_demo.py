from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from projects.models import Project, Action

class Command(BaseCommand):
    help = "Seed demo Projects and Actions"

    def handle(self, *args, **options):
        # Create a demo user
        user, created = User.objects.get_or_create(username="demo_user")
        if created:
            user.set_password("demo1234")  # optional password
            user.is_staff = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created user: {user.username}"))
        else:
            self.stdout.write(f"User {user.username} already exists")

        # Create a demo project
        project, created = Project.objects.get_or_create(
            name="Demo Project",
            owner=user
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created project: {project.name}"))
        else:
            self.stdout.write(f"Project {project.name} already exists")

        # Create demo actions
        actions_data = [
            {"action_type": "deliver_resource", "status": "pending", "context": {"note": "Send food pack"}},
            {"action_type": "deploy_expert", "status": "in_progress", "context": {"note": "Assign field expert"}},
            {"action_type": "checkin", "status": "pending", "context": {"note": "Call client for status"}}
        ]

        for ad in actions_data:
            action, created = Action.objects.get_or_create(**ad)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created action: {action.action_type}"))
            else:
                self.stdout.write(f"Action {action.action_type} already exists")

        self.stdout.write(self.style.SUCCESS("Seeding complete!"))
