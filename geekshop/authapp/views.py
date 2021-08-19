from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, HttpResponseRedirect

from geekshop import settings
from .forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from django.contrib import auth
from django.urls import reverse

from .models import ShopUser


def login(request):
    title = 'вход'
    login_form = ShopUserLoginForm(data=request.POST)

    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user, 'django.contrib.auth.backends.ModelBackend')
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('index'))

    content = {'title': title,
               'login_form': login_form,
               'next': next
               }
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    title = 'Подтверждение учетной записи'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                message = 'Сообщение с инструкциями по активации вашей учетной записи отправлено на ваш почтовый ящик.'
                context = {
                    'title': title,
                    'message': message,
                    'register_form': register_form
                }
                return render(request, 'authapp/verification_sent.html', context=context)
            else:

                message = 'Неудлаось отправить сообщение.'
                context = {
                    'title': title,
                    'message': message,
                    'register_form': register_form
                }
                return render(request, 'authapp/verification_sent.html', context=context)
    else:
        register_form = ShopUserRegisterForm()
        message = ''
    message = ''
    context = {
        'title': title,
        'message': message,
        'register_form': register_form
    }
    return render(request, 'authapp/register.html', context)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('index'))


@transaction.atomic
def edit(request):
    title = 'редактирование'
    user = request.user

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=user)
        profile_form = ShopUserProfileEditForm(
            instance=request.user.shopuserprofile
        )
    content = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form,
        'user': user,
    }
    return render(request, 'authapp/edit.html', content)


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = f'Подтверждение учетной записи {user.username}'

    message = f'Для подтверждения учетной записи {user.username} на портале \
    {settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
