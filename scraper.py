import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

class ScrapeProductInfo:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        self.driver = webdriver.Chrome(options=chrome_options)


    def identify_platform(self, url):
        if 'flipkart' in url.lower():
            return self.flipkart(url)
        elif 'amazon' in url.lower():
            return self.amazon(url)
        elif 'meesho' in url.lower():
            return self.meesho(url)
        else:
            return "Invalid URL"

    def flipkart(self, url):
        driver = self.driver
        driver.get(url)
        product_title = driver.find_element(By.CSS_SELECTOR, '#container > div > div._2c7YLP.UtUXW0._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div._1YokD2._3Mn1Gg.col-8-12 > div:nth-child(2) > div > div:nth-child(1) > h1').text

        try:
            product_mrp = driver.find_element(By.CSS_SELECTOR, '#container > div > div._2c7YLP.UtUXW0._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div._1YokD2._3Mn1Gg.col-8-12 > div:nth-child(2) > div > div.dyC4hf > div.CEmiEU > div > div._3I9_wc._2p6lqe').text
        except NoSuchElementException:
            product_mrp = driver.find_element(By.CSS_SELECTOR, '#container > div > div._2c7YLP.UtUXW0._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div._1YokD2._3Mn1Gg.col-8-12 > div:nth-child(2) > div > div.dyC4hf.pZkvcx > div.CEmiEU > div > div').text

        return product_title, product_mrp

    def amazon(self, url):
        driver = self.driver
        driver.get(url)
        product_title = driver.find_element(By.CSS_SELECTOR, '#productTitle').text

        try:
            if "refurbished" in product_title.lower():
                product_mrp = driver.find_element(By.CSS_SELECTOR, '#corePrice_desktop > div > table > tbody > tr:nth-child(1) > td.a-span12.a-color-secondary.a-size-base > span.a-price.a-text-price.a-size-base > span:nth-child(2)').text
            else:
                product_mrp = driver.find_element(By.CSS_SELECTOR, '#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-small.aok-align-center > span > span.aok-relative > span.a-size-small.a-color-secondary.aok-align-center.basisPrice > span > span:nth-child(2)').text
        except NoSuchElementException:
            product_mrp = driver.find_element(By.CSS_SELECTOR, '#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center.aok-relative > span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay > span:nth-child(2) > span.a-price-whole').text

        product_mrp = re.sub(r'\D', '', product_mrp)
        return product_title, product_mrp

    def meesho(self, url):
        driver = self.driver
        driver.get(url)
        product_title = driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div/div[2]/div[1]/span').text

        try:
            product_mrp = driver.find_element(By.XPATH,'//p[contains(text(), "₹")]').text
        except NoSuchElementException:
            product_mrp = driver.find_element(By.XPATH,'//h4[contains(text(), "₹")]').text

        product_mrp = re.sub(r'\D', '', product_mrp)
        return product_title, product_mrp

    def __del__(self):
        self.driver.quit()
