from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BorrowedBook
from django.core.exceptions import ObjectDoesNotExist

@receiver(post_save, sender=BorrowedBook)
def start_countdown(sender, instance, created, **kwargs):
    if created:
        # Initialize countdown timer
        instance.check_overdue()  # Initial status check
        
        # Start background task for overdue checking
        from .tasks import check_borrow_overdue
        check_borrow_overdue.apply_async(
            (instance.id,),
            eta=instance.due_time  # Execute at due time
        )