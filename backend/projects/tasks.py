from celery import shared_task
from .models import Action

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 5})
def process_action(self, action_id):
    action = Action.objects.get(id=action_id)

    # mark as in progress
    action.status = "in_progress"
    action.save()

    # 🔧 placeholder logic
    # later this can call APIs, notify people, assign actors, etc
    print(f"Processing action {action.id}: {action.action_type}")

    # mark done
    action.status = "completed"
    action.save()

    return action.id

# from celery import shared_task
# from .models import Action

# @shared_task
# def process_action(action_id):
#     action = Action.objects.get(id=action_id)
#     action.status = "processed"
#     action.save()
#     return f"Action {action_id} processed"
