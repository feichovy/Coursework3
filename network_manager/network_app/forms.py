from django import forms

class DeviceConfigForm(forms.Form):
    ip = forms.CharField(label='Device IP Address', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    secret = forms.CharField(label='Enable Secret', max_length=100, widget=forms.PasswordInput)
    interface = forms.CharField(label='Interface', max_length=50)
    ip_addr = forms.CharField(label='Interface IP Address', max_length=100)
    mask = forms.CharField(label='Subnet Mask', max_length=100)


class OSPFConfigForm(forms.Form):
    ip = forms.CharField(label='Device IP Address', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    secret = forms.CharField(label='Enable Secret', max_length=100, widget=forms.PasswordInput)
    ospf_process = forms.CharField(label='OSPF Process ID', max_length=50)
    ospf_network = forms.CharField(label='OSPF Network', max_length=100)
    ospf_wildcard = forms.CharField(label='Wildcard Mask', max_length=100)
    ospf_area = forms.CharField(label='OSPF Area', max_length=50)

class IPSecConfigForm(forms.Form):
    ip = forms.CharField(label='Device IP Address', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    secret = forms.CharField(label='Enable Secret', max_length=100, widget=forms.PasswordInput)
    crypto_map = forms.CharField(label='Crypto Map Name', max_length=100)
    isakmp_policy = forms.CharField(label='ISAKMP Policy', max_length=100)

class ACLConfigForm(forms.Form):
    ip = forms.CharField(label='Device IP Address', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    secret = forms.CharField(label='Enable Secret', max_length=100, widget=forms.PasswordInput)
    acl_number = forms.CharField(label='ACL Number', max_length=50)
    acl_action = forms.CharField(label='Action (permit/deny)', max_length=10)
    acl_protocol = forms.CharField(label='Protocol (ip/tcp/udp)', max_length=10)
    acl_source = forms.CharField(label='Source Address', max_length=100)
    acl_destination = forms.CharField(label='Destination Address', max_length=100)
