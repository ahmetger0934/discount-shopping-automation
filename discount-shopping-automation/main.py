from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Function to close overlay if exists
def close_overlay(driver):
    try:
        overlay = driver.find_element(By.CSS_SELECTOR, "div.ins-promotions-wrapper-undefined")
        driver.execute_script("arguments[0].style.visibility='hidden'", overlay)
        print("Overlay closed.")
    except Exception as e:
        print(f"No overlay found or failed to close overlay: {e}")

# Function to scroll and click element
def scroll_and_click(driver, element):
    try:
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()  # Scroll to the element
        element.click()  # Click the element
        print("Element clicked successfully.")
    except Exception as e:
        print(f"Failed to click the element: {e}")
        # As a fallback, use JavaScript to click the element
        driver.execute_script("arguments[0].click();", element)
        print("Element clicked using JavaScript.")

# Function to add product to cart
def add_product_to_cart(product):
    driver.get(product[2])  # Navigate to the product page directly
    time.sleep(5)  # Wait for the product page to load

    try:
        # Close any overlay that might be blocking
        close_overlay(driver)

        # Define preferred sizes
        preferred_sizes = ['M', 'L', '29-30', '30-30', '30-32', '29-32', 'S', 'XL']
        size_selected = False

        # Attempt to select size from dropdown (if it exists)
        try:
            size_select = driver.find_element(By.CSS_SELECTOR, 'select.size-select-list')
            size_options = size_select.find_elements(By.TAG_NAME, 'option')
            for option in size_options:
                size_name = option.text.strip()
                if size_name in preferred_sizes:
                    option.click()
                    time.sleep(1)  # Wait for the selection to be applied
                    size_selected = True
                    print(f"Selected size '{size_name}' from dropdown for '{product[0]}'.")
                    break
        except Exception as dropdown_error:
            print(f"No dropdown found or could not select size from dropdown: {dropdown_error}")

        # If dropdown selection didn't work or wasn't found, try radio buttons
        if not size_selected:
            try:
                size_options = driver.find_elements(By.CSS_SELECTOR, 'ul.size-list li.size-li')
                for option in size_options:
                    label = option.find_element(By.TAG_NAME, 'label')
                    size_name = label.get_attribute('data-name').strip()
                    if size_name in preferred_sizes:
                        label.click()
                        time.sleep(1)  # Wait for the selection to be applied
                        size_selected = True
                        print(f"Selected size '{size_name}' from radio buttons for '{product[0]}'.")
                        break
            except Exception as radio_error:
                print(f"No radio buttons found or could not select size from radio buttons: {radio_error}")

        if not size_selected:
            print(f"No preferred size available for '{product[0]}'. Skipping to next product.")
            return

        # Try clicking the add to cart button after scrolling
        add_to_cart_button = driver.find_element(By.ID, "addtocartbutton")
        scroll_and_click(driver, add_to_cart_button)

    except Exception as e:
        print(f"Failed to process '{product[0]}': {e}")

# Open the Colins product listing page
driver.get('https://www.colins.com.tr/c/tum-urunler-1?specs=7,67,231')

# Wait for the page to load completely
time.sleep(5)  # Adjust sleep time as needed

try:
    # Find all elements that contain the product names
    product_name_elements = driver.find_elements(By.CSS_SELECTOR, 'a.product-name.track-link')

    # Find all elements that contain the price information
    price_elements = driver.find_elements(By.CSS_SELECTOR, 'span.product-new-price')

    # Extract prices, product names, and associate them with links
    products = []
    for name_element, price_element in zip(product_name_elements, price_elements):
        try:
            # Extract the product name
            product_name = name_element.get_attribute("title").strip()

            # Extract the price
            price_text = price_element.text.strip().replace(' TL', '').replace('.', '').replace(',', '.')
            price_value = float(price_text)

            # Extract the product link
            product_link = name_element.get_attribute("href")

            # Append the product info to the list
            products.append((product_name, price_value, product_link))
        except Exception as e:
            print(f"Failed to extract product details: {e}")
            continue  # Skip this product if extraction fails

    # Identify the most popular and most expensive products
    if products:
        most_popular_product = products[0]  # Assume the first product is the most popular
        most_expensive_product = max(products, key=lambda x: x[1])  # Find the most expensive product

        print(f"The most popular product is: '{most_popular_product[0]}' with a price of {most_popular_product[1]:.2f} TL")
        print(f"The most expensive product is: '{most_expensive_product[0]}' with a price of {most_expensive_product[1]:.2f} TL")

        # Add both the most popular and most expensive products to the cart
        add_product_to_cart(most_popular_product)
        add_product_to_cart(most_expensive_product)

        # Proceed to checkout
        try:
            driver.get("https://www.colins.com.tr/cart")  # Go to the cart page
            time.sleep(3)  # Wait for the cart page to load

            proceed_to_checkout_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a#nextStep'))
            )
            scroll_and_click(driver, proceed_to_checkout_button)
            time.sleep(5)  # Wait for the checkout page to load
            print("Proceeding to checkout...")

            # Fill in login details to complete the purchase
            try:
                email_input = driver.find_element(By.ID, "LoginModel_Email")
                email_input.send_keys("your_email@example.com")  # Replace with your email

                password_input = driver.find_element(By.ID, "LoginModel_Password")
                password_input.send_keys("your_password")  # Replace with your password

                login_button = driver.find_element(By.CSS_SELECTOR, 'input.btn.btn-primary.w-100')
                scroll_and_click(driver, login_button)
                time.sleep(5)  # Wait for the login to complete
                print("Logged in and proceeding with checkout...")
            except Exception as login_error:
                print(f"Failed to log in: {login_error}")

        except Exception as checkout_error:
            print(f"Failed to proceed to checkout: {checkout_error}")

    else:
        print("No products were found on the page.")

    # Keep the browser open by waiting indefinitely (or use a specific timeout if desired)
    print("Press Ctrl+C to close the browser...")
    while True:
        time.sleep(1)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()  # Ensure the driver is closed when done