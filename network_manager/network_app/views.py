from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from .forms import DeviceConfigForm
from netmiko import ConnectHandler

# Create SSH connection and enter configure terminal
def connect_to_device(username, ip, password, secret):
    try:
        network_device = {
            'device_type': 'cisco_ios',
            'host': ip,
            'username': username,
            'password': password,
            'secret': secret
        }
        connection = ConnectHandler(**network_device)
        connection.enable()
        return connection, None
    except Exception as e:
        return None, f"Failed to connect via SSH: {str(e)}"

# Configure Loopback0 & GigabitEthernet1
def config_interface(connection, interface, ip, mask):
    commands = [
        f"interface {interface}",
        f"ip address {ip} {mask}",
        "no shutdown",
    ]
    try:
        connection.send_config_set(commands)
        return f"[SUCCESS] {interface} configured with {ip}/{mask} successfully"
    except Exception as e:
        return f"[ERROR] Fail to configure {interface}: {str(e)}"

# Django view for configuring device
def config_device(request):
    if request.method == 'POST':
        form = DeviceConfigForm(request.POST)
        if form.is_valid():
            # 获取表单数据
            ip = form.cleaned_data['ip']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            secret = form.cleaned_data['secret']
            interface = form.cleaned_data['interface']
            ip_addr = form.cleaned_data['ip_addr']
            mask = form.cleaned_data['mask']

            # 建立设备连接
            connection, error_message = connect_to_device(username, ip, password, secret)
            if connection:
                result = config_interface(connection, interface, ip_addr, mask)
                connection.disconnect()
                return HttpResponse(f"Configuration Result: {result}")
            else:
                return HttpResponse(f'[ERROR] Unable to connect to the device: {error_message}')
    else:
        form = DeviceConfigForm()

    return render(request, 'network_app/config_device.html', {'form': form})
