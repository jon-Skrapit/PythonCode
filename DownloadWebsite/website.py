import os
import urllib.request
import re
from selenium import webdriver
from bs4 import BeautifulSoup


class WebSite(object):
    def __init__(self, website, chrome_driver):
        self.website = website
        self.chrome_driver = chrome_driver
        self.current_path = os.path.abspath(os.curdir)
        self.folder_path = {}
        self.init_folder()

    def run(self):
        # 使用webdriver获取网页源代码比较容易，而简单地使用requests获取不到网页源代码
        browser = webdriver.Chrome(self.chrome_driver)
        browser.get(self.website)
        html = browser.page_source
        browser.quit()
        self.write_context_to_file(html, self.current_path, 'index.html')
        soup = BeautifulSoup(html, 'lxml')
        for css_or_js in soup.find_all('link'):
            if 'href' in css_or_js.attrs:
                if css_or_js['href'].endswith('js'):
                    download_url = self.get_download_url(css_or_js['href'])
                    self.save_file(download_url, self.folder_path['js'])
                elif css_or_js['href'].endswith('css'):
                    download_url = self.get_download_url(css_or_js['href'])
                    self.save_file(download_url, self.folder_path['css'])

        for img in soup.find_all('img'):
            if 'src' in img.attrs:
                download_url = self.get_download_url(img['src'])
                self.save_file(download_url, self.folder_path['img'])

        for js in soup.find_all('script'):
            if 'src' in js.attrs:
                download_url = self.get_download_url(js['src'])
                self.save_file(download_url, self.folder_path['js'])

        for css in soup.find_all('style'):
            if 'src' in css.attrs:
                download_url = self.get_download_url(css['src'])
                self.save_file(download_url, self.folder_path['css'])

    def init_folder(self):
        folder_names = ['js', 'css', 'img']
        for name in folder_names:
            path = self.current_path + '/' + name
            if os.path.exists(path):
                self.delete_file_folder(path)
            os.mkdir(path)
            self.folder_path[name] = path

    def delete_file_folder(self, src):
        if os.path.isfile(src):
            try:
                os.remove(src)
            except:
                pass
        elif os.path.isdir(src):
            for item in os.listdir(src):
                itemsrc = os.path.join(src, item)
                self.delete_file_folder(itemsrc)
            try:
                os.rmdir(src)
            except:
                pass

    def download_file(self, url):
        try:
            print(url)
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko')
            response = urllib.request.urlopen(req)
            return response.read()
        except urllib.error.HTTPError as e:
            print(e)
            return None

    def save_file(self, url, folder):
        os.chdir(folder)  # 跳转到下载目录
        filename = url.split('/')[-1]  # 获取下载文件名
        file = self.download_file(url)
        if file is not None:
            with open(filename, 'wb') as f:
                f.write(file)
                f.close()
            return None

    def write_context_to_file(self, context, folder, filename):
        os.chdir(folder)
        with open(filename, 'wb') as f:
            if isinstance(context, str):
                context = bytes(context, encoding='utf-8')
            f.write(context)
            f.close()
            return None

    def get_download_url(self, fileurl):
        if '?' in fileurl:
            fileurl = fileurl.split('?')[0]
        if fileurl.startswith('http'):
            return fileurl
        elif fileurl.startswith('//'):
            return 'http:' + fileurl
        else:
            if self.website.startswith('/'):
                website = self.website[:-1]
            matchObj = re.match(r'[\.\./|\./]{0,}([a-z|/|0-9|A-Z|\.|\-]{1,})', fileurl)
            if matchObj and matchObj.group(1):
                fileurl = matchObj.group(1)
            return website + '/' + fileurl