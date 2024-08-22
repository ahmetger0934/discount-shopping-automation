
# Discount Shopping Automation

## Overview
This project is a Python-based automation script designed to streamline online shopping during discount days. It uses Selenium WebDriver to automate the process of navigating e-commerce websites, selecting the appropriate sizes, and adding products to your cart.

## Features
- **Web Scraping:** Automates the extraction of product names, prices, and links.
- **Overlay Handling:** Manages and closes pop-ups and overlays that interfere with automated clicks.
- **Dynamic Content Management:** Adapts to dynamically loaded content, ensuring reliable performance.
- **Error Handling:** Incorporates robust error handling for scenarios like unavailable sizes or non-clickable elements.
- **Checkout Process:** Automates the checkout process, including login and final purchase steps.

## Requirements
- Python 3.x
- Selenium WebDriver
- ChromeDriver (compatible with the version of Chrome installed)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ahmetger0934/discount-shopping-automation.git
   cd discount-shopping-automation
   
2. **Install required packages:**
   pip install -r requirements.txt

3.**Download ChromeDriver:**
Download ChromeDriver and place it in the project directory or a directory in your system's PATH.

**Usage**

1.**Run the script:**

-Before running, ensure you have configured the necessary parameters (e.g., your email and password) in the script.
-Execute the script with the following command:

 python discount-shopping-automation.py

2.**Automation Process:**

- The script will automatically:
- Navigate to the e-commerce site.
- Identify and select the most popular and the most expensive products.
- Choose the preferred sizes.
- Add the products to the shopping cart.
- Proceed to the checkout page.
- Log in using the provided credentials and complete the purchase.

**Notes**
- Responsibility: This script is intended for educational purposes and should be used responsibly. Ensure you have permission to automate interactions with any website.
- Customization: Modify the script to fit other websites or different product preferences.

**Contributing**

- Contributions are welcome! Feel free to fork the repository, make improvements, and submit a Pull Request.


