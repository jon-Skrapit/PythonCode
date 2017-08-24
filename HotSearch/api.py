import requests
from selenium import webdriver
import time
import _thread
import re


def getProxies(num, v_num):
    url = 'http://lab.crossincode.com/proxy/get/?num='+str(num)+'&v_num='+str(v_num)
    r = requests.get(url)
    ip_array = r.json()['proxies']
    ips = []
    for ip in ip_array:
        ips.append(ip['http'])
    return ips


def wbSearch(text, proxy, times=100):
    url = 'http://s.weibo.com/weibo/'+text
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server={0}'.format(proxy))
    browser = webdriver.Chrome('/Users/Jon/chromedriver', chrome_options=chrome_options)
    #  browser.set_page_load_timeout(5)
    for i in range(times):
        try:
            browser.get(url)
            time.sleep(10)
        except Exception as e:
            print(e)
    browser.quit()


def bdSearch(text, proxy, times=100):
    url = 'https://www.baidu.com/s?wd=' + text
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server={0}'.format(proxy))
    browser = webdriver.Chrome('/Users/Jon/chromedriver', chrome_options=chrome_options)
    #  browser.set_page_load_timeout(5)
    for i in range(times):
        try:
            browser.get(url)
            time.sleep(10)
        except Exception as e:
            print(e)
    browser.quit()


def becomeHotSearch(text, ips, function):
    if ips is None or len(ips) <= 0:
        return
    for ip in ips:
        _thread.start_new_thread(function, (text, ip))


def proxy66(num):
    code = ''
    url = 'http://www.66ip.cn/getzh.php?getzh='+code+'&getnum='+str(num)+'&isp=0&anonymoustype=2&start=&ports=&export=&ipaddress=&area=1&proxytype=0&api=https'
    r = requests.get(url)
    text = r.text.strip()
    pattern = re.compile(r'([0-9]{1,}\.[0-9]{1,}\.[0-9]{1,}\.[0-9]{1,}:[0-9]{2,})')
    match = pattern.findall(text)
    if match:
        return match
    else:
        return None