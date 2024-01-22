from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import re




def get_data(oras):
    pairs_list = []
    print("Starting")
    #options = Options() 
    #options.add_argument("") 
    browser = webdriver.Firefox()#options=options)

    browser.get(f'https://www.hotels.com/Hotel-Search?destination={oras}')
    browser.implicitly_wait(20)

    print("Website loaded")
    for _ in range(1):
        browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)

    
    try:
        property_listing_results = browser.find_element(By.XPATH, '//*[@data-stid="property-listing-results"]')
        child_elements = property_listing_results.find_elements(By.XPATH, './/*[contains(@class, "uitk-heading")]')
        price_summary_elements = property_listing_results.find_elements(By.XPATH, './/*[contains(@data-test-id, "price-summary-message-line") and contains(., "The price is €")]')
        hidden_text_elements = property_listing_results.find_elements(By.XPATH, './/*[contains(@class, "uitk-text uitk-type-300 uitk-text-default-theme is-visually-hidden")]')
        image_elements = property_listing_results.find_elements(By.XPATH, './/*[contains(@class, "uitk-gallery-carousel-item uitk-gallery-carousel-item-current")]//img[contains(@class, "uitk-image-media")]')

        for child_element, price_summary_element, image in zip(child_elements[1:], price_summary_elements, image_elements):
            child_text = child_element.text
            
            image_src = image.get_attribute('src')
            try:
                numeric_values = re.findall(r'\d+', price_summary_element.text)
                if numeric_values:
                    numeric_value = numeric_values[0]
                else:
                    numeric_value = "No numeric value found"
            except Exception as price_summary_exception:
                numeric_value = "No price summary found"

            pairs_list.append([child_text, numeric_value,image_src])

    except Exception as e:
        print(f"Unable to find and retrieve HTML content: {e}")

    for pair in pairs_list:
        print(pair)
    browser.quit()
    return pairs_list
    

