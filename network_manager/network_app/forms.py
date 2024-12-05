from django import forms

from django import forms

class DeviceConfigForm(forms.Form):
    ip = forms.CharField(label='Device IP Address', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(render_value=True))
    secret = forms.CharField(label='Enable Secret', max_length=100, widget=forms.PasswordInput(render_value=True))
    interface = forms.ChoiceField(
        label='Interface',
        choices=[
            ('GigabitEthernet1', 'GigabitEthernet1'),
            ('loopback0', 'loopback')
        ]
    )
    ip_addr = forms.CharField(label='Interface IP Address', max_length=100)
    mask = forms.CharField(label='Subnet Mask', max_length=100)

class OSPFConfigForm(forms.Form):
    ip = forms.CharField(label='Device IP Address', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(render_value=True))
    secret = forms.CharField(label='Enable Secret', max_length=100, widget=forms.PasswordInput(render_value=True))
    process_id = forms.CharField(label='OSPF Process ID', max_length=10)
    network = forms.CharField(label='OSPF Network', max_length=100)
    wildcard_mask = forms.CharField(label='Wildcard Mask', max_length=100)
    area = forms.CharField(label='OSPF Area', max_length=10)

class IPSecConfigForm(forms.Form):
    ip = forms.CharField(label='Device IP Address', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(render_value=True))
    secret = forms.CharField(label='Enable Secret', max_length=100, widget=forms.PasswordInput(render_value=True))
    crypto_map = forms.CharField(label='Crypto Map Name', max_length=100)
    isakmp_policy = forms.CharField(label='ISAKMP Policy', max_length=100)

class ACLConfigForm(forms.Form):
    ip = forms.CharField(label='Device IP Address', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(render_value=True))
    secret = forms.CharField(label='Enable Secret', max_length=100, widget=forms.PasswordInput(render_value=True))
    acl_number = forms.CharField(label='ACL Number', max_length=50)
    acl_action = forms.CharField(label='Action (permit/deny)', max_length=10)
    acl_interface = forms.ChoiceField(
        label='Interface',
        choices=[
            ('g1', 'GigabitEthernet1'),
            ('loopback0', 'loopback')
        ])
