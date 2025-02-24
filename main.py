from path_utils import get_passwords_files, save_in_json
from wifi_utils import get_wifi_profile, scan_wifi, print_wifi_profiles, back_wifi_profiles, crack_passwords

try:
    import pip
    import importlib
    modules = ['pywifi', 'comtypes']
    for module in modules:
        try:
            importlib.import_module(module)
        except:
            pip.main(['install', module])
    import platform
    import os
    import time
    from pywifi import PyWiFi
    from pywifi import const
    from pywifi import Profile
    import subprocess
    import sys
    import logging
    import random
    import string
    from multiprocessing import Pool

    logging.getLogger("pywifi").setLevel(logging.CRITICAL)  # Отключает ERROR и WARNING
    def main():
        passwords_lists = get_passwords_files()
        if passwords_lists is None:
            exit(1)
        ssid = input("Введите название сети: ")
        if ssid is None:
            exit(1)
        crack_passwords(ssid, passwords_lists)
    if __name__ == "__main__":
        main()

except KeyboardInterrupt:
    print('\n\nExiting program...\n')
except Exception as e:
    print(str(f'\n\n{e}'))
