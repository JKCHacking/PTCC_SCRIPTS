from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(label="Email",
                            max_length=100,
                            widget=forms.EmailInput(attrs={'class': 'form-control'}))

    password = forms.CharField(label="Password",
                               max_length=100,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
