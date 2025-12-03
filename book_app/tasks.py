from celery import shared_task
from .models import BorrowedBook
from django.utils import timezone

@shared_task
def check_borrow_overdue(borrow_id):
    try:
        record = BorrowedBook.objects.get(id=borrow_id)
        if not record.is_overdue:
            record.is_overdue = True
            record.save()
            # Add any overdue actions (email, fines, etc.)
    except BorrowedBook.DoesNotExist:
        pass  # Handle missing record