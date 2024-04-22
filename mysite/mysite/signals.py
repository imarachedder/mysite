from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

@receiver(user_login_failed)
def handle_failed_login(sender, credentials, **kwargs):
    username = credentials.get('username')
    if username:
        user = User.objects.filter(username=username).first()
        if user:
            now = timezone.now()
            user.failed_login_attempts += 1
            user.last_failed_login = now
            user.save()

            if user.failed_login_attempts >= settings.MAX_ATTEMPTS:
                user.is_active = False  # Блокировка аккаунта
                user.lockout_until = now + timezone.timedelta(minutes=settings.LOCKOUT_PERIOD)
                user.save()
