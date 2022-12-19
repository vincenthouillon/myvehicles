from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserChangeForm,
    UserCreationForm,
)


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email")


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = "__all__"


class UserProfileForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email")


class UserPasswordChangeForm(PasswordChangeForm):
    pass


class UserPasswordResetForm(PasswordResetForm):
    pass


class UserPasswordResetConfirmForm(SetPasswordForm):
    user = get_user_model()  # type:ignore
