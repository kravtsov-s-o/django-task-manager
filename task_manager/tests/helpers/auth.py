from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(username="user", password="password123"):
    return User.objects.create_user(
        username=username,
        password=password,
    )
