from django import forms

class LoginForm(forms.Form):
    name = forms.CharField(label="Name:", max_length=100, empty_value="Enter Name", required=True)
    email = forms.EmailField(label="Email:", empty_value="Enter Email", required=True)
    password = forms.CharField(label="Password:", empty_value="Enter Password:", required=True, widget = forms.PasswordInput())
    
