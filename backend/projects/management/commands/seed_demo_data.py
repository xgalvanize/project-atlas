from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from projects.models import Project, Action, Actor

class Command(BaseCommand):
    help = "Seed demo Projects, Actions, and Actors with winter/emergency scenario"

    def handle(self, *args, **kwargs):
        # Clear old demo data
        Action.objects.all().delete()
        Project.objects.all().delete()
        Actor.objects.all().delete()
        User.objects.filter(username__in=["alice", "bob", "charlie"]).delete()

        # Create Users
        alice_user = User.objects.create(username="alice")
        bob_user = User.objects.create(username="bob")
        charlie_user = User.objects.create(username="charlie")

        # Create Actors
        alice = Actor.objects.create(name="Alice", role="volunteer", user=alice_user)
        bob = Actor.objects.create(name="Bob", role="staff", user=bob_user)
        charlie = Actor.objects.create(name="Charlie", role="field expert", user=charlie_user)

        # Create Projects
        project1 = Project.objects.create(name="Winter Shelter Project", owner=alice_user)
        project2 = Project.objects.create(name="Street Outreach Project", owner=bob_user)

        # Winter Shelter Project Actions
        Action.objects.create(
            project=project1,
            action_type="field_assessment",
            status="completed",
            context={"note": "Assess shelter capacity and street populations"},
            actor=charlie
        )
        Action.objects.create(
            project=project1,
            action_type="deliver_resource",
            status="in_progress",
            context={"note": "Deliver winter kits: blankets, food, water"},
            actor=bob
        )
        Action.objects.create(
            project=project1,
            action_type="deploy_expert",
            status="pending",
            context={"note": "Deploy survival expert to streets for outreach"},
            actor=charlie
        )
        Action.objects.create(
            project=project1,
            action_type="checkin",
            status="pending",
            context={"note": "Call shelter manager for status update"},
            actor=alice
        )

        # Street Outreach Project Actions
        Action.objects.create(
            project=project2,
            action_type="field_assessment",
            status="pending",
            context={"note": "Assess locations where homeless people are concentrated"},
            actor=alice
        )
        Action.objects.create(
            project=project2,
            action_type="deliver_resource",
            status="pending",
            context={"note": "Send food packs and hygiene kits to street locations"},
            actor=bob
        )
        Action.objects.create(
            project=project2,
            action_type="checkin",
            status="pending",
            context={"note": "Follow up with volunteers on outreach"},
            actor=charlie
        )

        self.stdout.write(self.style.SUCCESS("Winter/emergency scenario demo data seeded successfully!"))
