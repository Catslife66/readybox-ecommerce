from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordResetView

from .forms import UserProfileEditForm, UserRegisterForm, UserPasswordResetForm
from .models import User
from cart.models import CartItem


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('menu:menu_list')
    else:
        form = AuthenticationForm()
    context = {'form': form }
    return render(request, 'accounts/registration/login.html', context)
    

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')
    return render(request, 'accounts/registration/logout.html')


def register_view(request):
    session_id = request.session.session_key
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()

            cartItems = CartItem.objects.filter(session_id=session_id)
            cartItems.update(user=user)
            CartItem.objects.bulk_update(cartItems, ['user'])
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
    
    context = {'form': form}
    return render(request, 'accounts/registration/register.html', context)


def check_username(request):
    if request.htmx:
        user_name = request.POST.get('user_name')
        try:
            user = User.objects.filter(user_name=user_name)
            return HttpResponse('The username has been taken.')
        except:
            return HttpResponse('')


@login_required
def edit_profile(request):
    user = request.user
    form = UserProfileEditForm(request.POST or None, instance=user)
    context ={'form': form}
    if form.is_valid():
        user_update = form.save(commit=False)
        user_update.first_name = form.cleaned_data['first_name']
        user_update.last_name = form.cleaned_data['last_name']
        user_update.mobile = form.cleaned_data['mobile']
        update_session_auth_hash(request, user) 
        new_password = form.cleaned_data['new_password1']
        if new_password != '':
            user_update.set_password(form.cleaned_data['new_password1'])
        user_update.save()

        messages.success(request, 'Profile saved')
        print('changed success')
        context['message'] = 'success'
        return redirect(reverse('accounts:dashboard'))
   
    return render(request, 'accounts/user/profile.html', context)


