from django import forms
from django.forms import ModelForm
from users.models import Profile
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    """
    Model form for user params, it's done here so we can add more params than Django's default ones
    """

    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="Nombre de usuario")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}), label="Correo electrónico")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label="Contraseña")
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label="Repetir contraseña")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_repeat']


class LoginForm(forms.Form):
    """
    Model form for user login, only taking into account username and password
    """

    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="Nombre de usuario")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label="Contraseña")

    class Meta:
        model = User
        fields = ['username', 'password']
        exclude = ['email', 'password_repeat']


class PasswordForm(forms.Form):
    """
    Model form for user recovering password via email
    """

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}), label="Correo electrónico")

    class Meta:
        model = User
        fields = ['email']
        exclude = ['username', 'password', 'password_repeat']


class ProfileForm(forms.Form):
    """
    Model form for user changing his password with the old one
    TODO: it should be renamed to a clearer name like ChangePasswordForm
    """

    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label="Contraseña antigua")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label="Nueva contraseña")
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label="Repetir nueva contraseña")
