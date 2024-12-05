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
                    'ip': '192.168.56.102',
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
                'secret': secret,
                'timeout': 100,  # 增加超时时间
                'session_log': 'session_log.txt'  # 启用会话日志
            }

            # 配置命令
            commands = [
                f"interface {interface}",
                f"ip address {ip_addr} {mask}"
            ]

            try:
                # 尝试连接到设备
                connection = ConnectHandler(**network_device)
                connection.enable()

                # 使用 send_config_set 而不是逐条 send_command
                output = connection.send_config_set(commands)

                # 断开连接
                connection.disconnect()

                # 设备配置成功后的反馈信息
                messages.success(request, f"Interface Configuration successful: {output}")

                # 在设备配置成功后更新配置文件
                try:
                    # 更新设备的 IP 地址到配置文件中的 'ip' 字段
                    config['devices'][0]['ip'] = ip_addr
                    with open(CONFIG_FILE_PATH, 'w') as file:
                        json.dump(config, file, indent=4)

                    messages.success(request, f"Configuration file updated successfully with new IP: {ip_addr}")
                except Exception as e:
                    messages.error(request, f"[ERROR] Failed to update configuration file: {str(e)}")

            except Exception as e:
                messages.error(request, f"[ERROR] Could not connect to the router: {str(e)}")
        else:
            messages.error(request, "Form data is invalid. Please check your inputs.")

    # 初始化表单，填充默认值（非 POST 请求的情况）
    else:
        form = DeviceConfigForm(initial={
            'ip': device['ip'],
            'username': device['username'],
            'password': device['password'],
            'secret': device['secret'],
            'interface': 'GigabitEthernet1'
        })

    return render(request, 'network_app/config_device.html', {'form': form})

def config_ospf(request):
    file_path = 'network_app/config.json'
    config = read_config(file_path)
    print(config)
    if request.method == 'POST':
        form = OSPFConfigForm(request.POST)
        if form.is_valid():
            ip = form.cleaned_data['ip']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            secret = form.cleaned_data['secret']
            process_id = form.cleaned_data['process_id']
            network = form.cleaned_data['network']
            wildcard_mask = form.cleaned_data['wildcard_mask']
            area = form.cleaned_data['area']

            try:
                # Connect to the device
                device = {
                    'device_type': 'cisco_ios',
                    'host': ip,
                    'username': username,
                    'password': password,
                    'secret': secret
                }
                connection = ConnectHandler(**device)
                connection.enable()

                # Configure OSPF
                commands = [
                    f"router ospf {process_id}",
                    f"network {network} {wildcard_mask} area {area}"
                ]
                connection.send_config_set(commands)
                connection.disconnect()

                messages.success(request, f"Successfully configured OSPF Process ID {process_id} with Network {network}")
            except Exception as e:
                messages.error(request, f"Failed to configure OSPF: {str(e)}")
        else:
            messages.error(request, "Invalid form data")
    else:
        form = OSPFConfigForm(initial={
            'ip': config['devices'][0]['ip'],
            'username': config['devices'][0]['username'],
            'password': config['devices'][0]['password'],
            'secret': config['devices'][0]['secret'],
            'process_id': '1',
            'network': '192.168.56.0',
            'wildcard_mask': '0.0.0.255',
            'area': '0'
        })

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
            source_ip = form.cleaned_data['source_ip']
            wildcard_mask = form.cleaned_data['wildcard_mask']
            interface = form.cleaned_data['interface']
            direction = form.cleaned_data['direction']  # 获取用户选择的方向

            # 配置 ACL 的命令
            commands = [
                f"access-list {acl_number} {action} {source_ip} {wildcard_mask}",
                f"interface {interface}",
                f"ip access-group {acl_number} {direction}"
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

                # 发送配置命令集
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
