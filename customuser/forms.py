from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin', 'is_teacher')

    def clean_password(self):
        return self.initial["password"]


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=50, required=True,
                             widget=forms.EmailInput(
                                 attrs={'placeholder': 'Username',
                                        'class': 'border p-3 w-100 my-2'}
                             )
                             )
    password = forms.CharField(
        max_length=50, required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password', 'class': 'border p-3 w-100 my-2'}
        )
    )


class UserRegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'password']
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'placeholder': 'Email', 'class': 'border p-3 w-100 my-2'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'class': 'border p-3 w-100 my-2'}))


class UserPasswordEditForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Current Password', 'class': 'form-control'}))
    new_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'New Password', 'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))


class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Name', 'class': 'form-control', 'required': 'required'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Email', 'class': 'form-control', 'required': 'required'}))
    message = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Message', 'class': 'border w-100 p-3 mt-3 mt-lg-4', 'required': 'required'}))
