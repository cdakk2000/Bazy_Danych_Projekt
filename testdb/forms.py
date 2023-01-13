from django import forms
#formularz logowania
class LoginForm(forms.Form):
    username = forms.EmailField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget= forms.PasswordInput)
    register = forms.BooleanField(label='Register', required=False)

#formularz opcji
class OptionsForm(forms.Form):
    compare  = forms.BooleanField(label='Compare', required=False)
    findphone = forms.BooleanField(label='Find phone', required=False)
    savesearch = forms.BooleanField(label='Save search', required=False)
    manage = forms.BooleanField(label='Manage', required=False)

class SearchForm(forms.Form):
    model = forms.CharField(label='Model', max_length=64, required=False)
    brand_name = forms.CharField(label='Brand', max_length=16, required=False)
    release = forms.DateField(label='Release date', required=False)
    height = forms.FloatField(label='Height', min_value=0, step_size = 0.01, required=False)
    width = forms.FloatField(label='Width', min_value=0, step_size = 0.01, required = False)
    thickness = forms.FloatField(label='Thickness', min_value=0, step_size = 0.01, required = False)
    resolution = forms.CharField(label='Resolution', max_length=12, required = False)
    ppi = forms.IntegerField(label='PPI',min_value=0, max_value=1000, required = False)
    cpu_name = forms.CharField(label='CPU', max_length=128, required = False)
    chipset_name = forms.CharField(label='Chipset', max_length=23, required = False)
    gpu_name = forms.CharField(label='GPU', max_length=64, required = False)
    memory_card_dedicated = forms.BooleanField(label='Memory card dedicated', required=False)
    internal_memory = forms.IntegerField(label='Internal memory',min_value=0, max_value=4096, step_size = 1, required = False)
    ram = forms.IntegerField(label='RAM',min_value=0, step_size = 1, required = False)
    wifi = forms.CharField(label='Wi-Fi', max_length=32, required = False)
    sim = forms.CharField(label='SIM', max_length=128, required = False)
    connector = forms.CharField(label='Connector', max_length=32, required = False)
    audio_jack = forms.BooleanField(label='Audio jack', required=False)
    bluetooth_version = forms.FloatField(label='Bluetooth version', min_value=3, step_size = 0.1, required = False)
    gps = forms.BooleanField(label='GPS', required=False)
    nfc = forms.BooleanField(label='NFC', required=False)
    radio = forms.BooleanField(label='Radio', required=False)
    battery_capacity = forms.IntegerField(label='Battery', min_value=0, step_size = 10, required = False)
    battery_removable = forms.BooleanField(label='Removable battery', required=False)

#class AdminOptions(forms.Form):
#   addphone = forms.BooleanField(label='Add phone', required=False)
#    deletephone = forms.BooleanField(label='Delete phone', required=False)
#   editphone = forms.BooleanField(label='Edit phone', required=False)
#    comments = format.BooleanField(label='Comments', required=False)
