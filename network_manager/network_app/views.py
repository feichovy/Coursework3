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
                    'secret': 'enable_password',
                    'interfaces': {}
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

# 更新配置文件
def write_config(file_path, config):
    try:
        with open(file_path, 'w') as file:
            json.dump(config, file, indent=4)
        print(f"[INFO] Configuration file '{file_path}' updated successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to update configuration file '{file_path}': {str(e)}")

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

                # 更新配置文件中的接口信息
                device['interfaces'][interface] = {
                    'ip': ip_addr,
                    'mask': mask
                }
                write_config(CONFIG_FILE_PATH, config)

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
