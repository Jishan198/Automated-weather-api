from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail 
import time
@shared_task
def process_successful_payment(user_id):
    try:
        user = User.objects.get(id=user_id)
        
        # 1. Upgrade the user
        user.is_staff = True
        user.save()
        print(f"CELERY WORKER: Upgraded {user.username} to Premium.")

        # 2. Construct and send the Welcome Email
        subject = 'Welcome to Premium Data Access!'
        message = f'Hi {user.username},\n\nThank you for upgrading! Your account is now unlocked.\n\nEnjoy the Automated Data Dashboard.'
        from_email = 'noreply@datadashboard.com'
        recipient_list = [user.email if user.email else 'test@example.com']

        print(f"CELERY WORKER: Sending email to {recipient_list[0]}...")
        
        # This is the actual Django command to send emails
        send_mail(subject, message, from_email, recipient_list)
        
        print(f"CELERY WORKER: Email successfully sent!")
        
    except User.DoesNotExist:
        print(f"CELERY WORKER ERROR: User ID {user_id} not found.")