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

class SaveSearchForm(forms.Form):
    brand = forms.CharField(label='Brand', max_length=64, required=False) 
    model = forms.CharField(label='Model', max_length=64, required=False)
   # email = forms.EmailField(label='Email', max_length=100, required=False)
   # password = forms.CharField(label='Password', max_length=100, widget= forms.PasswordInput, required=False)

class AdminOptionsForm(forms.Form):
    addphone = forms.BooleanField(label='Add phone', required=False)
    deletephone = forms.BooleanField(label='Delete phone', required=False)
    editphone = forms.BooleanField(label='Edit phone', required=False)
    comments = forms.BooleanField(label='Delete comments', required=False)
    deleteuser = forms.BooleanField(label='Delete user', required=False)

class AdminPhoneForm(forms.Form):
    model = forms.CharField(label='Model', max_length=64, required=True)
    brand_name = forms.CharField(label='Brand', max_length=16, required=True)
    release = forms.DateField(label='Release date', required=False)
    height = forms.FloatField(label='Height', min_value=0, step_size = 0.01, required=False)
    width = forms.FloatField(label='Width', min_value=0, step_size = 0.01, required = False)
    thickness = forms.FloatField(label='Thickness', min_value=0, step_size = 0.01, required = False)
    resolution = forms.CharField(label='Resolution', max_length=12, required = False)
    ppi = forms.IntegerField(label='PPI',min_value=0, max_value=1000, required = False)
    cpu_name = forms.CharField(label='CPU', max_length=128, required = False)
    chipset_name = forms.CharField(label='Chipset', max_length=23, required = False)
    gpu_name = forms.CharField(label='GPU', max_length=64, required = False)
    memory_card_dedicated = forms.CharField(label='Memory card dedicated(y/n)', required=False, max_length=3)
    internal_memory = forms.IntegerField(label='Internal memory',min_value=0, max_value=4096, step_size = 1, required = False)
    ram = forms.IntegerField(label='RAM',min_value=0, step_size = 1, required = False)
    wifi = forms.CharField(label='Wi-Fi', max_length=32, required = False)
    sim = forms.CharField(label='SIM', max_length=128, required = False)
    connector = forms.CharField(label='Connector', max_length=32, required = False)
    audio_jack = forms.CharField(label='Audio jack(y/n)', required=False, max_length=3)
    bluetooth_version = forms.FloatField(label='Bluetooth version', min_value=3, step_size = 0.1, required = False)
    gps = forms.CharField(label='GPS(y/n)', required=False, max_length=3)
    nfc = forms.CharField(label='NFC(y/n)', required=False, max_length=3)
    radio = forms.CharField(label='Radio(y/n)', required=False, max_length=3)
    battery_capacity = forms.IntegerField(label='Battery', min_value=0, step_size = 10, required = False)
    battery_removable = forms.CharField(label='Removable battery(y/n)', required=False, max_length=3)
    cameras = forms.CharField(label='Cameras (MP/f, MP/f ...)', max_length=128, required = False)
    photourl = forms.CharField(label='Photo URL', max_length=256, required = False)


class AdminDeletePhoneForm(forms.Form):
    model = forms.CharField(label='Model', max_length=64, required=True)
    brand_name = forms.CharField(label='Brand', max_length=16, required=True)

class CommentForm(forms.Form):
    comment = forms.CharField(label='Comment', max_length=1024, required=True)
    email = forms.EmailField(label='Username', max_length=64, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, max_length=64, required=True)

class AdminDeleteCommentsForm(forms.Form):
    comment_id = forms.IntegerField(label="Comment ID", min_value=0, step_size = 1, required = False)

class AdminDeleteUserForm(forms.Form):
    user_id = forms.IntegerField(label="User ID", min_value=0, step_size=1, required=False)
