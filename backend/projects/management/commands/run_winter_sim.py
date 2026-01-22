import random
from django.core.management.base import BaseCommand
from projects.models import Project, Action, Actor

class Command(BaseCommand):
    help = "Simulate winter/emergency events and auto-generate Actions"

    def handle(self, *args, **kwargs):
        projects = Project.objects.all()
        actors = list(Actor.objects.all())

        if not projects or not actors:
            self.stdout.write(self.style.WARNING("No projects or actors exist. Run seed_demo_data first."))
            return

        for project in projects:
            # Random chance of emergency event
            event_chance = random.random()
            if event_chance > 0.5:
                # Generate a new action dynamically
                actor = random.choice(actors)
                action_type = random.choice([
                    "deliver_resource",
                    "deploy_expert",
                    "field_assessment",
                    "checkin"
                ])
                context_note = f"Auto-generated {action_type} for {project.name}"
                
                Action.objects.create(
                    project=project,
                    action_type=action_type,
                    status="pending",
                    context={"note": context_note},
                    actor=actor
                )

                self.stdout.write(self.style.SUCCESS(
                    f"New Action '{action_type}' added to Project '{project.name}' assigned to Actor '{actor.name}'"
                ))

        self.stdout.write(self.style.SUCCESS("Winter/emergency simulation run complete!"))
