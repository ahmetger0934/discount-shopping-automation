from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open the Zara "All Products" page
driver.get('https://www.zara.com/tr/tr/man-all-products-l7465.html?v1=2458839')

# Wait for the page to load completely
time.sleep(5)  # You may need to adjust the sleep time depending on your internet speed

try:
    # Find all elements that contain the price information
    price_elements = driver.find_elements(By.CSS_SELECTOR, 'span.money-amount__main')

    # Find all elements that contain the product names within the <h2> tags
    product_elements = driver.find_elements(By.CSS_SELECTOR, 'a.product-link h2')

    # Find all elements that contain the product links
    product_link_elements = driver.find_elements(By.CSS_SELECTOR, 'a.product-link._item.product-grid-product-info__name.link')

    # Extract prices, product names, and associate them with links
    products = []
    for price_element, product_element, link_element in zip(price_elements, product_elements, product_link_elements):
        price_text = price_element.text
        price_value = float(price_text.replace('.', '').replace(',', '.').replace(' TL', ''))
        product_name = product_element.text
        product_link = link_element.get_attribute("href")
        products.append((product_name, price_value, product_link))

    # Find the product with the minimum and maximum prices
    if products:
        min_product = min(products, key=lambda x: x[1])
        max_product = max(products, key=lambda x: x[1])
        print(f"The cheapest product is: '{min_product[0]}' with a price of {min_product[1]:.2f} TL")
        print(f"The most expensive product is: '{max_product[0]}' with a price of {max_product[1]:.2f} TL")

        # Define a function to handle product page navigation, color/size selection, and adding to cart
        def add_product_to_cart(product):
            driver.get(product[2])  # Navigate to the product page directly
            time.sleep(5)  # Wait for the product page to load

            try:
                # Select the size M (US M) or EU 40
                size_buttons = driver.find_elements(By.CSS_SELECTOR, 'button.size-selector-list__item-button')
                for button in size_buttons:
                    size_text = button.find_element(By.CSS_SELECTOR, 'div.product-size-info__main-label').text
                    if 'M (US M)' in size_text or 'EU 44' in size_text:
                        button.click()
                        print(f"Selected size: {size_text}")
                        break
                else:
                    print(f"Size M (US M) or EU 44 not found for '{product[0]}'")

                time.sleep(2)  # Wait for size selection

                # Click the "Add to Cart" button
                add_to_cart_button = driver.find_element(By.CSS_SELECTOR, 'button.zds-button.product-cart-buttons__button.product-cart-buttons__add-to-cart')
                add_to_cart_button.click()
                time.sleep(3)  # Wait for the action to complete

            except Exception as e:
                print(f"Failed to add '{product[0]}' to cart: {e}")

        # Add both the cheapest and most expensive products to the cart
        add_product_to_cart(min_product)
        add_product_to_cart(max_product)

        # Proceed to checkout
        driver.get('https://www.zara.com/tr/tr/shop/cart')  # Navigate to the cart page
        time.sleep(5)  # Wait for the cart page to load

        try:
            proceed_to_checkout_button = driver.find_element(By.CSS_SELECTOR, 'button.zds-button.layout-shop-footer__body-button.zds-button--primary')
            proceed_to_checkout_button.click()
            time.sleep(5)  # Wait for the action to complete
        except Exception as e:
            print(f"Failed to proceed to checkout: {e}")

    else:
        print("No products were found on the page.")

except Exception as e:
    print(f"An error occurred: {e}")

# Keep the browser open by waiting indefinitely (or use a specific timeout if desired)
print("Press Ctrl+C to close the browser...")
while True:
    time.sleep(1)