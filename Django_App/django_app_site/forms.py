from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label="Username:", max_length=100, empty_value="Enter Username", required=True)
    email = forms.EmailField(label="Email:", empty_value="Enter Email", required=True)
    password = forms.CharField(label="Password:", empty_value="Enter Password:", required=True, widget = forms.PasswordInput, min_length=6, max_length=12)
    # password = forms.CharField(label="Password:", empty_value="Enter Password:", widget = forms.PasswordInput, validators=[validate_password])

    def clean(self, *args, **kwargs):
        cleaned_data = self.cleaned_data
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError("Username already exists! Please choose a different username")
        elif User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("Email has already been registered. Please use login to access your account")
        else:
            return cleaned_data

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    

class VerificationForm(forms.Form):
    verification_code = forms.IntegerField(label="Verification Code", min_value=1111, max_value=9999, required=True)

    def __init__(self, *args, request=None, **kwargs):
        super(VerificationForm, self).__init__(*args, **kwargs)
        self.request = request

    def clean(self, *args, **kwargs):
        cleaned_data = self.cleaned_data

        if self.request.session.get("verification_code") != self.cleaned_data["verification_code"]:
            print(self.request.session.get("verification_code"))
            raise forms.ValidationError("Invalid verification code!")
        else:
            return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(label="Username:", max_length=100, empty_value="Enter Username", required=True)
    password = forms.CharField(label="Password:", empty_value="Enter Password:", required=True, widget = forms.PasswordInput)

    def clean(self, *args, **kwargs):
        cleaned_data = self.cleaned_data

        user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])

        if not user:
            raise forms.ValidationError("Invalid Username or password!")
        else:
            cleaned_data['user'] = user
            return cleaned_data

class ChangeUsername(forms.Form):
    username = forms.CharField(label="New Username:", max_length=100, empty_value="Enter Username", required=True)

    def clean(self, *args, **kwargs):
        cleaned_data = self.cleaned_data

        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError("Username already exists! Please choose a different username")
        else:
            return cleaned_data
            
class ChangePassword(forms.Form):
    password = forms.CharField(label="Current Password:", empty_value="Enter Password:", required=True, widget = forms.PasswordInput)
    new_password = forms.CharField(label="New Password:", empty_value="Enter Password:", required=True, widget = forms.PasswordInput, min_length=6, max_length=12)

    def __init__(self, *args, request=None, **kwargs):
        super(ChangePassword, self).__init__(*args, **kwargs)
        self.request = request

    def clean(self, *args, **kwargs):
        cleaned_data = self.cleaned_data

        user = authenticate(username=self.request.session.get('username'), password=self.cleaned_data['password'])
        if not user:
            raise forms.ValidationError("Invalid password!")
        else:
            cleaned_data['user'] = user
            return cleaned_data
