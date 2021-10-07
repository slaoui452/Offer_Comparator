import requests
from seleniumwire import webdriver


def get_Proxy_list(Path):
    """
     Scrape proxies to defend our selves from AliExpress which can block our IP address

    :param Path: Path to the Chrome WebDriver
    :return: list of proxies IP:Port

    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    driver = webdriver.Chrome(Path, options=chrome_options)
    driver.get("https://www.sslproxies.org/")
    driver.execute_script("window.scrollTo(0,200);")
    driver.find_element_by_xpath("//*[@id=\"list\"]/div/div[1]/ul/li[5]/a").click()
    proxies = driver.find_element_by_xpath("//*[@id=\"raw\"]/div/div/div[2]/textarea").get_attribute("value")
    driver.close()
    pos = proxies.find("UTC.") + 6
    return proxies[pos:].split('\n')[:-1]


def det_Av_Proxy(Proxies):
    """
    Test a request to AliExpress website and get the available proxy

    :param Proxies: List of Proxies
    :return: Return an Available proxy

    """
    for proxy in Proxies:
        try:
            requests.get("https://www.aliexpress.com", proxies = {"http": "http://"+proxy,"https" : "http://"+proxy} , timeout=1)
            return proxy
        except:
            pass





