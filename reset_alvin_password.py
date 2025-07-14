import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PulseTrack.settings')
django.setup()

from django.contrib.auth.models import User

username = 'Alvin'
password = '123456'

try:
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_active = True
    user.save()
    print(f"Password for user '{username}' has been reset and user activated.")
except User.DoesNotExist:
    print(f"User '{username}' does not exist.")
