import json
import os
from netmiko import ConnectHandler
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .forms import DeviceConfigForm, OSPFConfigForm, IPSecConfigForm, ACLConfigForm

# 配置文件路径
CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

# 读取配置文件
def read_config(file_path):
    if not os.path.exists(file_path):
        # 如果文件不存在，创建并写入默认配置
        default_config = {
            'devices': [
                {
                    'name': 'default_device',
                    'ip': '192.168.56.103',
                    'username': 'admin',
                    'password': '0428',
                    'connection_type': 'ssh',
                    'secret': '0428'
                }
            ]
        }
        with open(file_path, 'w') as file:
            json.dump(default_config, file, indent=4)
        print(f"[INFO] Configuration file '{file_path}' has been created with default settings.")
        return default_config

    # 如果文件存在，读取文件内容
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
        return config

    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to read configuration from '{file_path}': {str(e)}")
        return {}

# 配置设备接口视图
def config_device(request):
    # 读取配置文件
    config = read_config(CONFIG_FILE_PATH)

    # 使用配置文件中的设备信息进行表单初始填充
    device = config['devices'][0]  # 假设只有一个设备的情况

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

            # 使用 Netmiko 连接到设备并配置接口
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

                # 更新设备的接口 IP 地址到配置文件
                device['interface_ip'] = ip_addr
                with open(CONFIG_FILE_PATH, 'w') as file:
                    json.dump(config, file, indent=4)

                messages.success(request, f"Interface Configuration successful: {output}")
            except Exception as e:
                messages.error(request, f"[ERROR] Could not connect to the router: {str(e)}")

        else:
            messages.error(request, "Form data is invalid. Please check your inputs.")

    else:
        # 初始化表单，填充默认值
        form = DeviceConfigForm(initial={
            'ip': device['ip'],
            'username': device['username'],
            'password': device['password'],
            'secret': device['secret']
        })

    return render(request, 'network_app/config_device.html', {'form': form})

# 配置 OSPF 协议视图
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
            process_id = form.cleaned_data['process_id']
            network = form.cleaned_data['network']
            wildcard = form.cleaned_data['wildcard']
            area = form.cleaned_data['area']

            network_device = {
                'device_type': 'cisco_ios',
                'host': ip,
                'username': username,
                'password': password,
                'secret': secret
            }

            commands = [
                f"router ospf {process_id}",
                f"network {network} {wildcard} area {area}"
            ]

            try:
                connection = ConnectHandler(**network_device)
                connection.enable()
                output = connection.send_config_set(commands)
                connection.disconnect()
                messages.success(request, f"OSPF Configuration successful: {output}")
            except Exception as e:
                messages.error(request, f"[ERROR] Could not connect to the router: {str(e)}")

        else:
            messages.error(request, "Form data is invalid. Please check your inputs.")

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
    device = config['devices'][0]

    if request.method == 'POST':
        form = IPSecConfigForm(request.POST)
        if form.is_valid():
            ip = form.cleaned_data['ip']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            secret = form.cleaned_data['secret']
            # 其他表单字段略

            # 配置命令和连接逻辑略

        else:
            messages.error(request, "Form data is invalid. Please check your inputs.")

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
    device = config['devices'][0]

    if request.method == 'POST':
        form = ACLConfigForm(request.POST)
        if form.is_valid():
            ip = form.cleaned_data['ip']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            secret = form.cleaned_data['secret']
            # 其他表单字段略

            # 配置命令和连接逻辑略

        else:
            messages.error(request, "Form data is invalid. Please check your inputs.")

    else:
        form = ACLConfigForm(initial={
            'ip': device['ip'],
            'username': device['username'],
            'password': device['password'],
            'secret': device['secret']
        })

    return render(request, 'network_app/config_acl.html', {'form': form})
