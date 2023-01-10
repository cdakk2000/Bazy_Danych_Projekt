from django import forms
#formularz logowania
class LoginForm(forms.Form):
    username = forms.EmailField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100)
#formularz opcji
class OptionsForm(forms.Form):
    compare  = forms.BooleanField(label='Compare', required=False)
    findphone = forms.BooleanField(label='Find phone', required=False)
    savesearch = forms.BooleanField(label='Save search', required=False)