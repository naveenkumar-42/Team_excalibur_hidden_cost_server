import re
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class Amazon:
    def __init__(self, driver):
        self.driver = driver

    def refurbished_scrape_info(self):
        driver = self.driver
        print("refurbished")
        product_mrp = driver.find_element(By.XPATH,
                                          "//*[@id='corePrice_desktop']//span[@class='a-price a-text-price a-size-base']//span[@aria-hidden='true']").text  # Refurbished MRP
        product_selling_price = driver.find_element(By.XPATH,
                                                    "//*[@id='corePrice_desktop']//span[contains(@class,'apexPriceToPay')]//span[@aria-hidden='true']").text  # Selling price

        return product_mrp, product_selling_price

    def scrape_info(self, url):
        product_mrp = None
        product_selling_price = None
        percentage = None
        driver = self.driver
        driver.get(url)

        product_title = driver.find_element(By.CSS_SELECTOR, '#productTitle').text
        print(product_title)
        product_category = driver.find_element(By.XPATH,
                                               "//a[contains(@class,'a-link-normal') and contains(@class,'a-color-tertiary')]").text

        if 'currently unavailable.' in driver.find_element(By.XPATH, "//*[@id='availability']").text.lower():
            print("Product Currently Unavailable")

        else:
            try:
                driver.find_element(By.XPATH, "//*[@id='refurbishedBadge_feature_div']")
                product_mrp, product_selling_price = self.refurbished_scrape_info()

            except NoSuchElementException:
                try:
                    product_mrp = driver.find_element(By.XPATH,
                                                      "//span[@class='a-price a-text-price']//span[@aria-hidden='true']").text  # MRP with discount

                except NoSuchElementException:
                    try:
                        product_mrp = driver.find_element(By.XPATH, "//span[@class='a-price-whole']").text  # MRP only

                    except NoSuchElementException:
                        print("No MRP found")

                try:
                    product_selling_price = driver.find_element(By.XPATH,
                                                                "//*[@id='corePriceDisplay_desktop_feature_div']//span[@class='a-price-whole']").text  # Selling price

                except NoSuchElementException:
                    product_selling_price = None
                    print("No Selling Price Found")

                try:
                    percentage = driver.find_element(By.XPATH, "//*[contains(@class,'savingsPercentage')]").text

                except NoSuchElementException:
                    print("Percentage Not Found")

        if product_mrp is not None:
            product_mrp = re.sub(r'\D', '', product_mrp)
        if product_selling_price is not None:
            product_selling_price = re.sub(r'\D', '', product_selling_price)
        if percentage is not None:
            percentage = re.sub(r'\D', '', percentage)

        return product_title, product_mrp, product_category, percentage, product_selling_price