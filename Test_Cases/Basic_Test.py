# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
from pyvirtualdisplay import Display
from colorama import Fore, Back, Style

test_path = "/root/"
arcanum_executable_path = test_path + 'Arcanum/opt/chromium.org/chromium-unstable/chromium-browser-unstable'
chromedriver_path = test_path + 'chromedriver/chromedriver'
user_data_path = test_path + '/userdata/'
log_path = test_path + 'logs/chromium.log'
os.environ["CHROME_LOG_FILE"] = log_path
v8_log_path = "/ram/analysis/v8logs/"
custom_extension_dir = '/root/extensions/custom/'

def init():
    if os.path.exists(custom_extension_dir) == False:
        os.system('mkdir -p %s'%custom_extension_dir)

    os.system('pkill Xvfb')
    os.system('pkill chrome')
    os.system('pkill chromedriver')
    os.system('pkill wpr')

    # Delete old user data dir
    os.system('rm -rf %s' % user_data_path)
    # Delete old logs
    os.system('rm -rf %s*' % v8_log_path)
    # No need to delete chromium.log since it will be replaced with each run

    display = Display(visible=0, size=(1920, 1080))
    display.start()

def deinit():
    os.system('pkill Xvfb')
    os.system('pkill chrome')
    os.system('pkill chromedriver')
    os.system('pkill wpr')

def launch_driver():
    # Please put ~/Sample_Extensions/Custom/Empty in /root/extensions/custom/
    extension_path = test_path + 'extensions/custom/Empty'
    if os.path.exists(arcanum_executable_path) == False:
        print(Fore.RED + "Error: Given Arcanum executable path [%s] does not exist. " % arcanum_executable_path + Fore.RESET)
        exit(0)
    if os.path.exists(extension_path) == False:
        print(Fore.RED+"Error: Test extension %s does not exist. Download it from the GitHub repo first."%extension_path + Fore.RESET)
        exit(0)

    service = Service(executable_path=chromedriver_path)
    options = webdriver.ChromeOptions()
    options.binary_location = arcanum_executable_path
    options.add_argument('--user-data-dir=%s' % user_data_path)
    options.add_argument("--enable-logging")
    options.add_argument("--v=0")
    options.add_argument('--verbose')
    # options.add_argument('--net-log-capture-mode=IncludeCookiesAndCredentials')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')

    options.add_argument('--load-extension={}'.format(extension_path))
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=service, options=options)
    return driver

def Run_Basic_Test():
    try:
        init()
        driver = launch_driver()
        driver.get('https://google.com')
        driver.quit()
        deinit()
        print('Basic Test: '+ Back.GREEN + "Success"+ Back.RESET + ".")
    except Exception as e:
        print('Basic Test: '+ Fore.RED + "Fail" + Fore.RESET + ":" + str(e))

if __name__ == '__main__':
    Run_Basic_Test()
