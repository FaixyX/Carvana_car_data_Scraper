import cloudscraper
import random
import json
import time
import ssl
import urllib3
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


proxies_list = [
    {
        'address': '123.23.23.23',
        'port': 1234,
        'username': 'admin',
        'password': 'password',
        'http': 'http://admin:password@123.23.23.23:1234',
        'https': 'http://admin:password@123.23.23.23:1234'
    },
    {
        'address': '123.23.23.23',
        'port': 1234,
        'username': 'admin',
        'password': 'password',
        'http': 'http://admin:password@123.23.23.23:1234',
        'https': 'http://admin:password@123.23.23.23:1234'
    },
    {
        'address': '123.23.23.23',
        'port': 1234,
        'username': 'admin',
        'password': 'password',
        'http': 'http://admin:password@123.23.23.23:1234',
        'https': 'http://admin:password@123.23.23.23:1234'
    },
    {
        'address': '123.23.23.23',
        'port': 1234,
        'username': 'admin',
        'password': 'password',
        'http': 'http://admin:password@123.23.23.23:1234',
        'https': 'http://admin:password@123.23.23.23:1234'
    },
    {
        'address': '123.23.23.23',
        'port': 1234,
        'username': 'admin',
        'password': 'password',
        'http': 'http://admin:password@123.23.23.23:1234',
        'https': 'http://admin:password@123.23.23.23:1234'
    },
    {
        'address': '123.23.23.23',
        'port': 1234,
        'username': 'admin',
        'password': 'password',
        'http': 'http://admin:password@123.23.23.23:1234',
        'https': 'http://admin:password@123.23.23.23:1234'
    },
]

headers = {
    'authority': 'apik.carvana.io',
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'Bearer',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://www.carvana.com',
    'pragma': 'no-cache',
    'referer': 'https://www.carvana.com/',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}

json_data = {
    'analyticsData': {
        'browser': 'Chrome',
        'clientId': 'srp_ui',
        'deviceName': '',
        'isFirstActiveSearchSession': True,
        'isMobileDevice': True,
        'previousSearchRequestId': 'abd4abc8-88aa-4bab-876b-8914f65cf3c9',
        'referrer': '',
        'searchSessionId': '449dc18f-af31-4624-a4f7-209d5298e624',
        'utmParams': {},
    },
    'browserCookieId': '60aae661-abb5-945a-cfb2-2ac42f96d3a2',
    'filters': {
        'bodyStyles': [
            'Suv',
        ],
    },
    'pagination': {
        'page': 1,
        'pageSize': 10000,
    },
    'requestedFeatures': [
        'EarliestAcquisitionBoosting',
        'ExcludeFacetData',
        'HideImpossibleCombos',
        'LoanTermPricing',
        'LocationBasedPrefiltering',
        'Personalization',
        'Sprinkles',
        'ApplyTradeIn',
    ],
    'sortBy': 'MostPopular',
    'zip5': '90060',
    'preferredAcquisitionName': '',
}

def create_scraper_with_proxy(proxy):
    # Create SSL context
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    # Create scraper with custom settings
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'mobile': False
        },
        debug=False,
        ssl_context=ssl_context,
        interpreter='nodejs'
    )
    
    # Configure proxy
    scraper.proxies.update({
        'http': proxy['http'],
        'https': proxy['https']
    })
    
    # Update headers
    scraper.headers.update(headers)
    
    return scraper

# List of vehicle categories to search
CATEGORIES = [
    'Suv', 'Sedan', 'Pickup', 'Coupe', 'MiniVan',
    'Convertible', 'Wagon', 'Hatchback', 'Electric',
    'Hybrid', 'Plug-In Hybrid']

def make_request_for_category(category, max_retries=5):
    used_proxies = set()
    all_vehicles = []  # List to store vehicles from all pages for this category
    
    for page in range(1, 3):  # Loop for 2 pages (page 1 and page 2)
        json_data['filters']['bodyStyles'] = [category]  # Update the category filter
        json_data['pagination']['page'] = page
        
        for attempt in range(max_retries):
            try:
                # Get a proxy we haven't used yet
                available_proxies = [p for p in proxies_list if p['address'] not in used_proxies]
                if not available_proxies:
                    print(f"All proxies have been tried for category {category}")
                    break
                    
                proxy = random.choice(available_proxies)
                used_proxies.add(proxy['address'])
                
                print(f"\nAttempt {attempt + 1} using proxy: {proxy['address']}:{proxy['port']} for category {category}, page {page}")
                
                # Create a new scraper with the proxy
                scraper = create_scraper_with_proxy(proxy)
                
                # First visit the main site to establish cookies
                print("Visiting www.carvana.com...")
                main_response = scraper.get(
                    'https://www.carvana.com/',
                    allow_redirects=True
                )
                print(f"Main site status code: {main_response.status_code}")
                
                # Add a realistic delay
                time.sleep(random.uniform(2, 4))
                
                # Make the API request
                print("Making API request...")
                response = scraper.post(
                    'https://apik.carvana.io/merch/search/api/v2/search',
                    json=json_data,
                    timeout=30
                )
                
                print(f"Status Code: {response.status_code}")
                
                if response.status_code == 403:
                    print("Received 403 Forbidden - Trying another proxy...")
                    time.sleep(random.uniform(1, 2))
                    continue
                    
                try:
                    result = response.json()
                    
                    # Check if vehicles data exists in the response
                    if 'inventory' in result and 'vehicles' in result['inventory']:
                        # Append vehicles from this page to the all_vehicles list
                        all_vehicles.extend(result['inventory']['vehicles'])
                        print(f"Found {len(result['inventory']['vehicles'])} vehicles for category {category} on page {page}")
                    
                    # If we successfully got the data, break out of the retry loop
                    break
                    
                except json.JSONDecodeError:
                    if attempt < max_retries - 1:
                        continue
                    else:
                        raise
                        
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(random.uniform(2, 3))
                    continue
                else:
                    raise
    
    return all_vehicles  # Return the concatenated vehicles data for this category


if __name__ == "__main__":
    try:
        # Create the 'Scraper_data' folder if it doesn't exist
        if not os.path.exists('Scraper_data'):
            os.makedirs('Scraper_data')
            print("Created folder: Scraper_data")

        for category in CATEGORIES:
            print(f"\nFetching data for category: {category}")
            
            # Fetch all vehicles data for the current category
            vehicles_data = make_request_for_category(category)
            
            if vehicles_data:
                print(f"\nSuccessful response for category {category}:")
                
                # Save only the vehicles data to a JSON file named after the category
                filename = f"{category.lower().replace(' ', '_')}_vehicles_data.json"
                filepath = os.path.join('Scraped_data', filename)  # Save inside the folder
                with open(filepath, 'w') as f:
                    json.dump(vehicles_data, f, indent=2)
                print(f"Vehicles data saved to {filename}")
                
                # Print summary of results
                print(f"\nTotal vehicles found for {category}: {len(vehicles_data)}")
            else:
                print(f"\nNo vehicles data found for category {category}.")
            
    except Exception as e:
        print(f"\nFinal error: {str(e)}")