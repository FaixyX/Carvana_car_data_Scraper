import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json

def setup_driver(headless=True):
    options = uc.ChromeOptions()
    
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Enable headless mode (set to False for debugging)
    if headless:
        options.add_argument('--headless=new')
    
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument('--disable-features=IsolateOrigins,site-per-process')
    
    driver = uc.Chrome(options=options)
    return driver

def get_max_pages(driver):
    """Fetch the last page number for pagination"""
    try:
        pagination_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul#pagination li"))
        )
        if pagination_elements:
            last_page_text = pagination_elements[-2].text.strip()
            return 1
            # return int(last_page_text) if last_page_text.isdigit() else 1
    except (TimeoutException, NoSuchElementException):
        print("Pagination not found or only one page available.")
    return 1

def scrape_carvana_category(driver, url_base, category):
    """Scrape vehicle links from Carvana category pages"""
    all_vehicle_links = []
    
    # Load existing links if file exists
    json_file = f'carvana_{category}_links.json'
    try:
        with open(json_file, 'r') as f:
            all_vehicle_links = json.load(f)
        print(f"Loaded {len(all_vehicle_links)} existing links from {json_file}")
    except FileNotFoundError:
        print(f"Starting new collection for {category}")

    try:
        print(f"Accessing {url_base}")
        driver.get(url_base)

        # Wait for page to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#results-section"))
        )
        time.sleep(5)

        max_pages = get_max_pages(driver)
        print(f"Total pages found: {max_pages}")

        for page in range(1, max_pages + 1):
            try:
                url = f"{url_base}&page={page}"
                print(f"Scraping page {page}/{max_pages}")
                driver.get(url)

                # Wait for results to load
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#results-section"))
                )
                time.sleep(5)

                vehicle_elements = driver.find_elements(By.CSS_SELECTOR, "#results-section div.h-full div a")
                new_links = []
                for element in vehicle_elements:
                    href = element.get_attribute('href')
                    if href and href not in all_vehicle_links:
                        new_links.append(href)
                        all_vehicle_links.append(href)

                # Save links after each page
                if new_links:
                    print(f"Found {len(new_links)} new vehicles on page {page}")
                    with open(json_file, 'w') as f:
                        json.dump(all_vehicle_links, f, indent=2)
                    print(f"Updated {json_file} with new links")
                else:
                    print(f"No new vehicles found on page {page}")

                time.sleep(3)

            except TimeoutException:
                print(f"Timeout on page {page}, skipping...")
                time.sleep(10)
                continue
            except Exception as e:
                print(f"Error on page {page}: {e}")
                time.sleep(10)
                continue

    except Exception as e:
        print(f"Initial request failed: {e}")

    return all_vehicle_links

def main():
    urls = {
        'suv': 'https://www.carvana.com/cars/filters?cvnaid=eyJmaWx0ZXJzIjp7ImJvZHlTdHlsZXMiOlsiU3V2Il19fQ',
        'sedan': 'https://www.carvana.com/cars/filters?cvnaid=eyJmaWx0ZXJzIjp7ImJvZHlTdHlsZXMiOlsiU2VkYW4iXX19',
        'truck': 'https://www.carvana.com/cars/filters?cvnaid=eyJmaWx0ZXJzIjp7ImJvZHlTdHlsZXMiOlsiUGlja3VwIl19fQ',
        'coupe': 'https://www.carvana.com/cars/filters?cvnaid=eyJmaWx0ZXJzIjp7ImJvZHlTdHlsZXMiOlsiQ291cGUiXX19',
        'minivan': 'https://www.carvana.com/cars/filters?cvnaid=eyJmaWx0ZXJzIjp7ImJvZHlTdHlsZXMiOlsiTWluaVZhbiJdfX0',
        'convertible': 'https://www.carvana.com/cars/filters?cvnaid=eyJmaWx0ZXJzIjp7ImJvZHlTdHlsZXMiOlsiQ29udmVydGlibGUiXX19',
        'wagon': 'https://www.carvana.com/cars/filters?cvnaid=eyJmaWx0ZXJzIjp7ImJvZHlTdHlsZXMiOlsiV2Fnb24iXX19',
        'hatchback': 'https://www.carvana.com/cars/filters?cvnaid=eyJmaWx0ZXJzIjp7ImJvZHlTdHlsZXMiOlsiSGF0Y2hiYWNrIl19fQ',
        'electric': 'https://www.carvana.com/cars/filters?cvnaid=eyJmaWx0ZXJzIjp7ImZ1ZWxUeXBlcyI6WyJFbGVjdHJpYyJdfX0',
        'pluginhybrid': 'https://www.carvana.com/cars/filters?cvnaid=eyJmaWx0ZXJzIjp7ImZ1ZWxUeXBlcyI6WyJQbHVnLUluIEh5YnJpZCJdfX0',
        'hybrid': 'https://www.carvana.com/cars/filters?cvnaid=eyJmaWx0ZXJzIjp7ImZ1ZWxUeXBlcyI6WyJIeWJyaWQiXX19',
    }

    driver = setup_driver(headless=False)  # Set to True for headless mode
    all_results = {}

    try:
        for category, url in urls.items():
            print(f"\nScraping {category.upper()} category...")
            vehicle_links = scrape_carvana_category(driver, url, category)
            all_results[category] = vehicle_links
            print(f"Total {len(vehicle_links)} vehicles found in {category} category")
            time.sleep(5)

        print("\nScraping completed!")
        for category, links in all_results.items():
            print(f"{category.upper()}: {len(links)} vehicles found")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()