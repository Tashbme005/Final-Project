from django.contrib.auth.models import User


def login_as_admin(client):
    User.objects.create_user(
        username='admin',
        email='admin@oasbay.ug',
        password='test-pass-123',
        is_staff=True,
        is_superuser=True,
    )
    client.login(username='admin', password='test-pass-123')
