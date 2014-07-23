import pwgen

superuser_password = pwgen.pwgen(20, 1, no_symbols=True)
adminuser_password = pwgen.pwgen(20, 1, no_symbols=True)

from django.contrib.auth.management.commands import changepassword
from django.core import management

management.call_command('createsuperuser',
                        interactive=False,
                        username='superuser',
                        email='superuser@example.com')

command = changepassword.Command()
command._get_pass = lambda *args: superuser_password
command.execute('superuser')

from django.contrib.auth.models import User

if not User.objects.filter(username='admin').count():
    User.objects.create_superuser('admin', 'admin@example.com', adminuser_password)


print 'Django superuser password:', superuser_password
print 'Django admin password:', adminuser_password
