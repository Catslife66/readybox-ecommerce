from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, UserChangeForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.password_validation import validate_password

from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-control', 'required':'required'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean(self):
        cleaned_data = self.cleaned_data

        username = str(self.cleaned_data['username']).lower()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This user name has been taken.')
        
        email = str(cleaned_data['email']).lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email has been registered.')
        
        return cleaned_data


class UserPasswordResetForm(PasswordResetForm):
    email = forms.CharField(label='Email Address', widget=forms.EmailInput(attrs={'class':'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if not user:
            raise forms.ValidationError('Sorry, this email does not match the email you registed with.')
        return email


class UserPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(attrs={'class':'form-control mb-3'}))
    new_password2 = forms.CharField(label='New password confirmation', widget=forms.PasswordInput(attrs={'class':'form-control mb-3'}))


class UserProfileEditForm(forms.ModelForm):
    old_password = forms.CharField(required=False, label='Old password', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    new_password1 = forms.CharField(required=False, label='New password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(required=False, label='New password confirmation', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = fields = ['username', 'first_name', 'last_name', 'email', 'mobile']



    def cleaned_username(self):
        username = self.cleaned_data['username']
        if username == self.instance.username:
            # If the username has not changed, return the original username
            return username
        

    def cleaned_email(self):
        email = self.cleaned_data['email']
        if email == self.instance.email:
            # If the email has not changed, return the original email
            return email


    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data['old_password']
        new_password1 = cleaned_data['new_password1']
        new_password2 = cleaned_data['new_password2']
    
        #check password
        if old_password or new_password1 or new_password2:
            if not self.instance.check_password(old_password):
                # If the old password is incorrect, raise a validation error
                raise forms.ValidationError('Your old password was entered incorrectly. Please enter it again.')
            
            # Use the built-in PasswordChangeForm to validate the new passwords
            password_change_form = PasswordChangeForm(user=self.instance, data=cleaned_data)
            if not password_change_form.is_valid():
                # If the new passwords are invalid, raise a validation error
                raise forms.ValidationError(password_change_form.errors)
            
        return cleaned_data
    