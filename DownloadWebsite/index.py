from website import WebSite

website = 'https://jon5939.wixsite.com/mysite'
chrome_driver = '/Users/Jon/chromedriver'
web = WebSite(website, chrome_driver)
web.run()
