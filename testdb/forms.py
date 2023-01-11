from django import forms
#formularz logowania
class LoginForm(forms.Form):
    username = forms.EmailField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget= forms.PasswordInput)
#formularz opcji
class OptionsForm(forms.Form):
    compare  = forms.BooleanField(label='Compare', required=False)
    findphone = forms.BooleanField(label='Find phone', required=False)
    savesearch = forms.BooleanField(label='Save search', required=False)

class SearchForm(forms.Form):
    model = forms.CharField(label='Model', max_length=64)
    brand = forms.CharField(label='Brand', max_length=16)
    release = forms.DateField(label='Release date')
    height = forms.FloatField(label='Height', min_value=0, step_size = 0.01)
    width = forms.FloatField(label='Width', min_value=0, step_size = 0.01)
    thickness = forms.FloatField(label='Thickness', min_value=0, step_size = 0.01)
    reslution = forms.CharField(label='Resolution', max_length=12)
    ppi = forms.IntegerField(label='PPI',min_value=0, max_value=1000)
    cpu = forms.CharField(label='CPU', max_length=128)
    chipset = forms.CharField(label='Chipset', max_length=23)
    gpu = forms.CharField(label='GPU', max_length=64)
    memory_card_dedicated = forms.BooleanField(label='Memory card dedicated', required=False)
    internal_memory = forms.IntegerField(label='Internal memory',min_value=0, max_value=4096, step_size = 1)
    ram = forms.IntegerField(label='RAM',min_value=0, step_size = 1)
    wifi = forms.CharField(label='Wi-Fi', max_length=32)
    sim = forms.CharField(label='SIM', max_length=128)
    connector = forms.CharField(label='Connector', max_length=32)
    audio_jack = forms.BooleanField(label='Audio jack', required=False)
    bluetooth_version = forms.FloatField(label='Bluetooth version', min_value=3, step_size = 0.1)
    gps = forms.BooleanField(label='GPS', required=False)
    nfc = forms.BooleanField(label='NFC', required=False)
    radio = forms.BooleanField(label='Radio', required=False)
    battery_capacity = forms.IntegerField(label='Battery', min_value=0, step_size = 100)
    battery_removable = forms.BooleanField(label='Removable battery', required=False)