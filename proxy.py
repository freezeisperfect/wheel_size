import random
import sys

import requests
from selenium import webdriver


class Proxy:
    def __init__(self):
        # self.req_proxy = RequestProxy()  # you may get different number of proxy when  you run this at each time
        # self._proxies = self.req_proxy.get_proxy_list()  # this will create proxy list
        proxy_url = 'http://prontoproxy.info'
        self.ygo_proxies = requests \
            .get(f'{proxy_url}') \
            .text.strip().split('\n')

    @property
    def random_proxy_dict(self):
        proxy = random.choice(self.ygo_proxies)
        proxy_list = proxy.split(":")
        proxy_str = f"http://{proxy_list[2]}:{proxy_list[3]}@{proxy_list[0]}:{proxy_list[1]}"
        return {
            "http": proxy_str,
            "https": proxy_str,
            "ftp": proxy_str
        }

    def get_random_from_proxy_list(self):
        return random.choice(self.ygo_proxies)

    def run_driver(self, with_proxy=False):
        """
        This is a function for running a new driver
        :return:
        """
        if with_proxy:
            proxy = self.get_random_from_proxy_list()
            webdriver.DesiredCapabilities.CHROME['proxy'] = {
                "httpProxy": proxy,
                "ftpProxy": proxy,
                "sslProxy": proxy,

                "proxyType": "MANUAL",
            }
        if 'win32' in sys.platform:  # If the OS is Windows
            chromedriver = 'C:\\chromedriver'
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            # options.add_argument('headless')
            t_driver = webdriver.Chrome(executable_path=chromedriver, options=options)
        else:  # if not Windows OS.
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            t_driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options)
        return t_driver
