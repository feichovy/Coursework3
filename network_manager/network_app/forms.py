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
    isakmp_policy = forms.IntegerField(label='ISAKMP Policy Number', min_value=1, max_value=100)  # 简单为数字

class ACLConfigForm(forms.Form):
    ip = forms.CharField(label='Device IP Address', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(render_value=True))
    secret = forms.CharField(label='Enable Secret', max_length=100, widget=forms.PasswordInput(render_value=True))
    acl_number = forms.IntegerField(label='ACL Number (1-99)', min_value=1, max_value=99)
    action = forms.ChoiceField(
        label='Action',
        choices=[('permit', 'Permit'), ('deny', 'Deny')]
    )
    source_ip = forms.CharField(label='Source IP Address', max_length=100)
    wildcard_mask = forms.CharField(label='Wildcard Mask', max_length=100)
    interface = forms.ChoiceField(
        label='Interface',
        choices=[
            ('GigabitEthernet1', 'GigabitEthernet1'),
            ('Loopback0', 'Loopback0')
        ]
    )
    direction = forms.ChoiceField(
        label='Direction',
        choices=[
            ('in', 'Inbound'),
            ('out', 'Outbound')
        ]
    )