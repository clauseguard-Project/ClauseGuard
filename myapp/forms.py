from django import forms
from django.contrib.auth.hashers import make_password
from .models import user


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a password',
            'required': True
        }),
        label='Password',
        min_length=8,
        help_text='Password must be at least 8 characters long.'
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'required': True
        }),
        label='Confirm Password'
    )

    class Meta:
        model = user
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username',
                'required': True,
                'minlength': 3
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
                'required': True
            }),
        }
        labels = {
            'username': 'Username',
            'email': 'Email Address',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if user.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists. Please choose a different one.')
        if len(username) < 3:
            raise forms.ValidationError('Username must be at least 3 characters long.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if user.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already registered. Please use a different email.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        # Check for at least one uppercase, one lowercase, and one digit
        if not any(char.isupper() for char in password):
            raise forms.ValidationError('Password must contain at least one uppercase letter.')
        if not any(char.islower() for char in password):
            raise forms.ValidationError('Password must contain at least one lowercase letter.')
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError('Password must contain at least one digit.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError('Passwords do not match. Please try again.')
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Hash the password before saving
        user.password_hash = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
