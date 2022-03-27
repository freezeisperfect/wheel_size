import requests
from bs4 import BeautifulSoup
from proxy import Proxy

proxy = Proxy()


def with_driver(link):
    driver = proxy.run_driver()
    driver.get(link)
    html = driver.page_source
    driver.quit()
    return BeautifulSoup(html, "html.parser")


def without_driver(link):
    html = requests.get(link, proxies=proxy.random_proxy_dict, verify=False).text
    return BeautifulSoup(html, "html.parser")
