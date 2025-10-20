from django.core.mail import send_mail
from django.conf import settings
from .models import Profile  # Make sure you import the Profile model

def send_announcement_email(announcement):
    """
    Sends an email to all users with profiles notifying them of a new announcement.

    :param announcement: The announcement object containing title and message
    """
    # Get all users who have profiles
    student_emails = Profile.objects.all().values_list('user__email', flat=True)

    subject = f"New Announcement: {announcement.title}"
    message = f"Dear Student,\n\nA new announcement has been made:\n\n{announcement.content}\n\nPlease check the announcement section for more details."

    # Send the email to all users with profiles
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        list(student_emails),  # Convert to list for send_mail
        fail_silently=False,
    )
