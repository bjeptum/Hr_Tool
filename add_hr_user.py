import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PulseTrack.settings')
django.setup()

from django.contrib.auth.models import User, Group

# --- CONFIGURE THESE ---
HR_USERNAME = 'Alvin'
HR_EMAIL = 'alvinkariuki07@gmail.com'
HR_PASSWORD = '123456'  # Change after login!
# -----------------------

user, created = User.objects.get_or_create(username=HR_USERNAME, defaults={
    'email': HR_EMAIL,
})
user.set_password(HR_PASSWORD)
user.is_active = True
user.save()
print(f'User {HR_USERNAME} password set and activated.')

hr_group, _ = Group.objects.get_or_create(name='HR')
user.groups.add(hr_group)
print(f'User {HR_USERNAME} added to HR group.')
print(f'Login with username: {HR_USERNAME} and password: {HR_PASSWORD}')
