import json
import os
from netmiko import ConnectHandler
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .forms import DeviceConfigForm, OSPFConfigForm, IPSecConfigForm, ACLConfigForm

# 配置文件路径
CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

# Welcome interface Function
def welcome(request):
    return render(request, 'network_app/welcome.html')

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
    if 'devices' not in config or len(config['devices']) == 0:
        messages.error(request, "Configuration file is missing valid 'devices' data. Please check the configuration file.")
        return render(request, 'network_app/config_device.html', {'form': DeviceConfigForm()})

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

                # 更新设备的 IP 地址到配置文件中的 'ip' 字段
                device['ip'] = ip_addr
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

def config_ospf(request):
    # 尝试读取配置文件
    config = {}
    if os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, 'r') as f:
            config = json.load(f)

    # 初始化表单默认值
    initial_data = {
        'device_ip': config.get('ip', '192.168.56.104'),  # 默认值为 192.168.56.104
        'username': config.get('username', 'admin'),      # 默认值为 'admin'
        'password': config.get('password', 'defaultpassword'),  # 默认值为 'defaultpassword'
        'enable_secret': config.get('secret', ''),        # 默认值为空字符串
        'ospf_process_id': '1',                           # 默认 OSPF Process ID 为 1
        'ospf_network': '192.168.56.0',                   # 默认网络地址为 192.168.56.0
        'wildcard_mask': '0.0.0.255',                     # 默认 Wildcard Mask 为 0.0.0.255
        'ospf_area': '0',                                 # 默认 Area 为 0
    }

    if request.method == 'POST':
        form = OSPFConfigForm(request.POST)
        if form.is_valid():
            # 获取表单数据
            device_ip = form.cleaned_data['device_ip']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            enable_secret = form.cleaned_data['enable_secret']
            ospf_process_id = form.cleaned_data['ospf_process_id']
            ospf_network = form.cleaned_data['ospf_network']
            wildcard_mask = form.cleaned_data['wildcard_mask']
            ospf_area = form.cleaned_data['ospf_area']

            # 配置 OSPF 的命令
            commands = [
                f"router ospf {ospf_process_id}",
                f"network {ospf_network} {wildcard_mask} area {ospf_area}"
            ]

            # 使用 Netmiko 连接到设备
            network_device = {
                'device_type': 'cisco_ios',
                'host': device_ip,
                'username': username,
                'password': password,
                'secret': enable_secret
            }

            try:
                connection = ConnectHandler(**network_device)
                connection.enable()
                output = connection.send_config_set(commands)
                connection.disconnect()

                # 成功配置的提示信息
                messages.success(request, f"OSPF Configuration successful: {output}")
            except Exception as e:
                messages.error(request, f"[ERROR] Could not connect to the router: {str(e)}")

        else:
            messages.error(request, "Form data is invalid. Please check your inputs.")

    else:
        # 初始化表单，填充默认值
        form = OSPFConfigForm(initial=initial_data)

    return render(request, 'network_app/config_ospf.html', {'form': form})
def config_ipsec(request):
    # 读取配置文件
    config = read_config(CONFIG_FILE_PATH)
    device = config['devices'][0]  # 假设只有一个设备

    if request.method == 'POST':
        form = IPSecConfigForm(request.POST)
        if form.is_valid():
            # 获取表单数据
            ip = form.cleaned_data['ip']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            secret = form.cleaned_data['secret']
            isakmp_policy = form.cleaned_data['isakmp_policy']
            transform_set = form.cleaned_data['transform_set']
            peer_ip = form.cleaned_data['peer_ip']
            acl_number = form.cleaned_data['acl_number']

            # 配置 IPSec 的命令
            commands = [
                f"crypto isakmp policy {isakmp_policy}",
                f"crypto ipsec transform-set {transform_set} esp-aes esp-sha-hmac",
                f"crypto map MYMAP 10 ipsec-isakmp",
                f"set peer {peer_ip}",
                f"set transform-set {transform_set}",
                f"match address {acl_number}",
                "interface GigabitEthernet0/0",
                "crypto map MYMAP"
            ]

            # 使用 Netmiko 连接到设备进行配置
            network_device = {
                'device_type': 'cisco_ios',
                'host': ip,
                'username': username,
                'password': password,
                'secret': secret
            }

            try:
                connection = ConnectHandler(**network_device)
                connection.enable()
                output = connection.send_config_set(commands)
                connection.disconnect()

                # 成功后反馈给用户
                messages.success(request, f"IPSec Configuration successful: {output}")

            except Exception as e:
                messages.error(request, f"[ERROR] Could not connect to the router: {str(e)}")

        else:
            messages.error(request, "Form data is invalid. Please check your inputs.")
    else:
        # 初始化表单，填充默认值
        form = IPSecConfigForm(initial={
            'ip': device['ip'],
            'username': device['username'],
            'password': device['password'],
            'secret': device['secret']
        })

    return render(request, 'network_app/config_ipsec.html', {'form': form})

def config_acl(request):
    # 读取配置文件
    config = read_config(CONFIG_FILE_PATH)
    device = config['devices'][0]  # 假设只有一个设备

    if request.method == 'POST':
        form = ACLConfigForm(request.POST)
        if form.is_valid():
            # 获取表单数据
            ip = form.cleaned_data['ip']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            secret = form.cleaned_data['secret']
            acl_number = form.cleaned_data['acl_number']
            action = form.cleaned_data['action']
            protocol = form.cleaned_data['protocol']
            source = form.cleaned_data['source']
            destination = form.cleaned_data['destination']

            # 配置 ACL 的命令
            commands = [
                f"access-list {acl_number} {action} {protocol} {source} {destination}"
            ]

            # 使用 Netmiko 连接到设备进行配置
            network_device = {
                'device_type': 'cisco_ios',
                'host': ip,
                'username': username,
                'password': password,
                'secret': secret
            }

            try:
                connection = ConnectHandler(**network_device)
                connection.enable()
                output = connection.send_config_set(commands)
                connection.disconnect()

                # 成功后反馈给用户
                messages.success(request, f"ACL Configuration successful: {output}")

            except Exception as e:
                messages.error(request, f"[ERROR] Could not connect to the router: {str(e)}")

        else:
            messages.error(request, "Form data is invalid. Please check your inputs.")
    else:
        # 初始化表单，填充默认值
        form = ACLConfigForm(initial={
            'ip': device['ip'],
            'username': device['username'],
            'password': device['password'],
            'secret': device['secret']
        })

    return render(request, 'network_app/config_acl.html', {'form': form})
