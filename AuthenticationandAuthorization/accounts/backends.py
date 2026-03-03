from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from accounts.forms import UserModel


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if not username:
            return None
        users = UserModel.objects.filter(email=username)

        if users.count() != 1:
            return None

        user = users.first()
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
