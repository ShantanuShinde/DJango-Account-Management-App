from django import forms

class LoginForm(forms.Form):
    name = forms.CharField(label="Name:", max_length=100, empty_value="Enter Name", required=True)
    email = forms.EmailField(label="Email:", empty_value="Enter Email", required=True)
    password = forms.CharField(label="Password:", empty_value="Enter Password:", required=True, widget = forms.PasswordInput())
    
class VerificationForm(forms.Form):
    verification_code = forms.IntegerField(label="Verification Code", min_value=1111, max_value=9999, required=True)