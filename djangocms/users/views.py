from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as do_login, logout as do_logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from users.forms import RegisterForm, LoginForm, PasswordForm, ChangePasswordForm, RolesForm
from users.models import Profile, Role
from django.template.loader import render_to_string, get_template
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMultiAlternatives, EmailMessage
from users.tokens import account_activation_token
import random
import string


def welcome(request):
    """
    Renders a welcome website after login
    """
    return render(request, 'welcome.html')


def register(request):
    """
    Form for the first time a user creates his account
    It handles (almost) all input exception
    """

    form = RegisterForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, 'register.html', {
                    'form': form,
                    'error_message': 'Nombre de usuario ya existente'
                })

            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, 'register.html', {
                    'form': form,
                    'error_message': 'Email ya utilizado previamente'
                })

            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, 'register.html', {
                    'form': form,
                    'error_message': 'Las contraseñas no coinciden'
                })

            else:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                
                user.save()
                profile = Profile.objects.create(user=user, verified=False)

                mail_subject = 'Activa tu cuenta de Cool Men Software'
                message = render_to_string('email.html', {
                    'user': user,
                    'domain': 'http://localhost:5432',
                    'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                    'token': account_activation_token.make_token(user),
                })
                from_email = 'coolmensoftware@gmail.com'
                to_email = form.cleaned_data.get('email')
                email = EmailMultiAlternatives(mail_subject, message, from_email, to=[to_email])
                email.content_subtype = 'html'

                email.send()

                context = {
                    'user': user
                }

                return render(request, 'welcome.html', context)

    return render(request, 'register.html', {'form': form})


def login(request):
    """
    Form for user login
    It handles (almost) all input exception
    """

    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None and Profile.objects.filter(user=user, verified=True):
                do_login(request, user)
                return redirect('/', {'user': user})

            elif Profile.objects.filter(user=user, verified=False):
                return render(request, 'login.html', {
                    'form': form,
                    'error_message': 'El correo electrónico no ha sido confirmado'
                })

            elif (User.objects.filter(username=form.cleaned_data['username']).exists() == False) \
                or (User.objects.filter(username=form.cleaned_data['password']).exists() == False):
                return render(request, 'login.html', {
                    'form': form,
                    'error_message': 'El usuario o la contraseña son incorrectos'
                })

    return render(request, 'login.html', {'form': form})


def logout(request):
    """
    Logouts user if he is logged in
    """

    do_logout(request)
    
    return redirect('/users/login')


def activate(request, uidb64, token):
    """
    If user has a token (account already created), he can automatically log in
    """

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    context = {
        'user': user
    }

    if user is not None and account_activation_token.check_token(user, token):
        Profile.objects.filter(user=user).update(verified=True)
        do_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return redirect('/users/welcome', context)

    else:
        return redirect('/users/welcome', context)


def recover_password(request):
    """
    Form for recovering user's password via email
    It handles (almost) all input exception
    """

    form = PasswordForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)

            if User.objects.filter(email=form.cleaned_data['email']).exists():
                new_password = ''.join((random.choice(string.ascii_letters + string.digits) for i in range(8)))
                user.set_password(new_password)
                user.save()

                mail_subject = 'Recuperación de contraseña'
                message = '<h3>Tu nueva contraseña es:</h3><strong>' + new_password + '</strong><br> \
                        <p>Ya puedes iniciar sesión en Cool Men Software con ella.</p>'
                from_email = 'coolmensoftware@gmail.com'
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, from_email, to=[to_email])
                email.content_subtype = 'html'

                email.send()

                return redirect('/users/login')

            else:
                return render(request, 'recover_password.html', {
                    'form': form,
                    'error_message': 'El correo electrónico no está registrado'
                })

    return render(request, 'recover_password.html', {'form': form})


def change_password(request):
    """
    Form for changing user's password knowing the old one
    It handles (almost) all input exception
    """

    form = ChangePasswordForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            if form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, 'change_password.html', {
                    'form': form,
                    'error_message': 'Las nuevas contraseñas no coinciden'
                })

            elif request.user.check_password(form.cleaned_data['old_password']) == False:
                return render(request, 'change_password.html', {
                    'form': form,
                    'error_message': 'La contraseña antigua no es correcta'
                })

            elif form.cleaned_data['password'] == form.cleaned_data['old_password']:
                return render(request, 'change_password.html', {
                    'form': form,
                    'error_message': 'La contraseña nueva no puede ser la misma que la antigua'
                })

            else:
                request.user.set_password(form.cleaned_data['password'])
                request.user.save()
                update_session_auth_hash(request, request.user)

                return redirect('/')

    return render(request, 'change_password.html', {'form': form})


def profile(request):
    """
    Returns user extra information (not Django's default one)
    """

    user = Profile.objects.get(user=request.user)

    form = RolesForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            return redirect('/')

    context = {
        'username': request.user.username,
        'verified': user.verified,
        'roles': user.roles.all(),
        'form': form,
        'admin_form': False
    }

    if request.user.username == 'admin':
        for i in range(Role.objects.count()):
            user.roles.add(Role.objects.get(pk=i + 1))
            context['admin_form'] = True

    # This deletes the form but its interesting to have that form for possible future needs
    context['admin_form'] = True

    return render(request, 'profile.html', context)