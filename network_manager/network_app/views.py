import json
import os
from netmiko import ConnectHandler
from django.shortcuts import render
from django.http import HttpResponse
from .forms import DeviceConfigForm, OSPFConfigForm, IPSecConfigForm, ACLConfigForm

# 配置文件路径
CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'config.json')

# 读取配置文件
def read_config(file_path):
    if not os.path.exists(file_path):
        # 如果文件不存在，创建并写入默认配置
        default_config = {
            'devices': [
                {
                    'name': 'default_device',
                    'ip': '192.168.56.1',
                    'username': 'admin',
                    'password': 'password',
                    'connection_type': 'ssh',
                    'secret': 'enable_password'
                }
            ]
        }
        with open(file_path, 'w') as file:
            json.dump(default_config, file, indent=4)
        print(f"[INFO] Configuration file '{file_path}' has been created with default settings. Please modify it to fit your environment.")
        return default_config

    # 如果文件存在，读取文件内容
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
        return config
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to read configuration from '{file_path}': {str(e)}")
        return {}

# Welcome 主页面视图
def welcome(request):
    return render(request, 'network_app/welcome.html')

# 配置接口视图
def config_device(request):
    config = read_config(CONFIG_FILE_PATH)
    device = config['devices'][0]  # 假设只有一个设备的情况

    if request.method == 'POST':
        form = DeviceConfigForm(request.POST)
        if form.is_valid():
            ip = form.cleaned_data['ip']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            secret = form.cleaned_data['secret']
            interface = form.cleaned_data['interface']
            ip_addr = form.cleaned_data['ip_addr']
            mask = form.cleaned_data['mask']

            network_device = {
                'device_type': 'cisco_ios',
                'host': ip,
                'username': username,
                'password': password,
                'secret': secret
            }

            commands = [
                f"interface {interface}",
                f"ip address {ip_addr} {mask}",
                "no shutdown"
            ]

            try:
                connection = ConnectHandler(**network_device)
                connection.enable()
                output = connection.send_config_set(commands)
                connection.disconnect()

                # 更新配置文件中的设备 IP 地址
                device['ip'] = ip_addr
                with open(CONFIG_FILE_PATH, 'w') as file:
                    json.dump(config, file, indent=4)

                return HttpResponse(f"Configuration Result: {output}")
            except Exception as e:
                return HttpResponse(f"[ERROR] Could not connect to the router: {str(e)}")

    else:
        # 使用读取的配置文件信息作为表单初始值
        form = DeviceConfigForm(initial={
            'ip': device['ip'],
            'username': device['username'],
            'password': device['password'],
            'secret': device['secret']
        })

    return render(request, 'network_app/config_device.html', {'form': form})

# 配置 OSPF 视图
def config_ospf(request):
    config = read_config(CONFIG_FILE_PATH)
    device = config['devices'][0]  # 假设只有一个设备的情况

    if request.method == 'POST':
        form = OSPFConfigForm(request.POST)
        if form.is_valid():
            ip = form.cleaned_data['ip']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            secret = form.cleaned_data['secret']
            ospf_process = form.cleaned_data['ospf_process']
            ospf_network = form.cleaned_data['ospf_network']
            ospf_wildcard = form.cleaned_data['ospf_wildcard']
            ospf_area = form.cleaned_data['ospf_area']

            network_device = {
                'device_type': 'cisco_ios',
                'host': ip,
                'username': username,
                'password': password,
                'secret': secret
            }

            commands = [
                f"router ospf {ospf_process}",
                f"network {ospf_network} {ospf_wildcard} area {ospf_area}"
            ]

            try:
                connection = ConnectHandler(**network_device)
                connection.enable()
                output = connection.send_config_set(commands)
                connection.disconnect()
                return HttpResponse(f"OSPF Configuration Result: {output}")
            except Exception as e:
                return HttpResponse(f"[ERROR] Could not connect to the router: {str(e)}")

    else:
        form = OSPFConfigForm(initial={
            'ip': device['ip'],
            'username': device['username'],
            'password': device['password'],
            'secret': device['secret']
        })

    return render(request, 'network_app/config_ospf.html', {'form': form})

# 配置 IPSec 视图
def config_ipsec(request):
    config = read_config(CONFIG_FILE_PATH)
    device = config['devices'][0]  # 假设只有一个设备的情况

    if request.method == 'POST':
        form = IPSecConfigForm(request.POST)
        if form.is_valid():
            ip = form.cleaned_data['ip']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            secret = form.cleaned_data['secret']
            crypto_map = form.cleaned_data['crypto_map']
            isakmp_policy = form.cleaned_data['isakmp_policy']

            network_device = {
                'device_type': 'cisco_ios',
                'host': ip,
                'username': username,
                'password': password,
                'secret': secret
            }

            commands = [
                f"crypto map {crypto_map}",
                f"crypto isakmp policy {isakmp_policy}"
            ]

            try:
                connection = ConnectHandler(**network_device)
                connection.enable()
                output = connection.send_config_set(commands)
                connection.disconnect()
                return HttpResponse(f"IPSec Configuration Result: {output}")
            except Exception as e:
                return HttpResponse(f"[ERROR] Could not connect to the router: {str(e)}")

    else:
        form = IPSecConfigForm(initial={
            'ip': device['ip'],
            'username': device['username'],
            'password': device['password'],
            'secret': device['secret']
        })

    return render(request, 'network_app/config_ipsec.html', {'form': form})

# 配置 ACL 视图
def config_acl(request):
    config = read_config(CONFIG_FILE_PATH)
    device = config['devices'][0]  # 假设只有一个设备的情况

    if request.method == 'POST':
        form = ACLConfigForm(request.POST)
        if form.is_valid():
            ip = form.cleaned_data['ip']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            secret = form.cleaned_data['secret']
            acl_number = form.cleaned_data['acl_number']
            acl_action = form.cleaned_data['acl_action']
            acl_protocol = form.cleaned_data['acl_protocol']
            acl_source = form.cleaned_data['acl_source']
            acl_destination = form.cleaned_data['acl_destination']

            network_device = {
                'device_type': 'cisco_ios',
                'host': ip,
                'username': username,
                'password': password,
                'secret': secret
            }

            commands = [
                f"access-list {acl_number} {acl_action} {acl_protocol} {acl_source} {acl_destination}"
            ]

            try:
                connection = ConnectHandler(**network_device)
                connection.enable()
                output = connection.send_config_set(commands)
                connection.disconnect()
                return HttpResponse(f"ACL Configuration Result: {output}")
            except Exception as e:
                return HttpResponse(f"[ERROR] Could not connect to the router: {str(e)}")

    else:
        form = ACLConfigForm(initial={
            'ip': device['ip'],
            'username': device['username'],
            'password': device['password'],
            'secret': device['secret']
        })

    return render(request, 'network_app/config_acl.html', {'form': form})
