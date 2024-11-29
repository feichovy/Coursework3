from django import forms

class DeviceConfigForm(forms.Form):
    ip = forms.CharField(label='Device IP Address', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    secret = forms.CharField(label='Enable Secret', max_length=100, widget=forms.PasswordInput)
    interface = forms.CharField(label='Interface (e.g., Loopback0 or GigabitEthernet1)', max_length=50)
    ip_addr = forms.CharField(label='Interface IP Address', max_length=100)
    mask = forms.CharField(label='Subnet Mask', max_length=100)
