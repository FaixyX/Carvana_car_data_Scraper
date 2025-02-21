# Carvana Vehicle Data Scraper

A Python-based web scraper that extracts vehicle data from Carvana's API across different car categories using proxy rotation for enhanced reliability.

## Project Overview

This project implements a robust scraping solution to collect vehicle data from Carvana's inventory API. It supports multiple vehicle categories and uses proxy rotation to avoid rate limiting and IP blocks.

### Key Features

- Multi-category vehicle data extraction
- Proxy rotation mechanism
- Automatic retry logic
- JSON data storage
- Configurable pagination
- Error handling and logging

## Directory Structure

```
├── CarvanaCarScraper_API.py   # Main scraper script
├── Scraped_data/              # Directory containing scraped JSON files
│   ├── suv_vehicles_data.json
│   ├── sedan_vehicles_data.json
│   └── ...
└── terminal_output.txt        # Contains scraping process logs
```

## Dependencies

- cloudscraper
- random
- json
- time
- ssl
- urllib3
- os

## Configuration

### Proxy Configuration

The script uses a list of proxies for rotation. Each proxy is configured with:
- IP address and port
- Authentication credentials
- HTTP/HTTPS proxy URLs

### Vehicle Categories

Supported vehicle categories:
- SUV
- Sedan
- Pickup
- Coupe
- MiniVan
- Convertible
- Wagon
- Hatchback
- Electric
- Hybrid
- Plug-In Hybrid

### Pagination Settings

- Current configuration: 2 pages per category
- Items per page: 20 (configurable up to 10,000)
- Modify `pageSize` in `json_data` to adjust items per page
- Adjust the range in `make_request_for_category()` to modify number of pages

## Usage

1. Ensure all dependencies are installed:
```bash
pip install cloudscraper urllib3
```

2. Configure proxies in the `proxies_list` if needed

3. Run the script:
```bash
python CarvanaCarScraper_API.py > terminal_output.txt
```

4. Monitor the terminal output (logged to terminal_output.txt)

5. Check the Scraped_data directory for JSON results

## Output Structure

- Each category's data is saved in a separate JSON file
- File naming format: `{category_name}_vehicles_data.json`
- Terminal output is logged to `terminal_output.txt`

### JSON Data Structure

Each vehicle entry contains:
- Vehicle details (make, model, year)
- Pricing information
- Technical specifications
- Available features
- Media links

## Error Handling

- Automatic proxy rotation on 403 errors
- Configurable retry attempts (default: 5)
- Random delays between requests
- SSL verification disabled for proxy compatibility

## Limitations

- Currently scrapes 2 pages per category (40 vehicles)
- Can be extended by modifying the page range
- Maximum page size of 10,000 items supported by API

## Best Practices

1. Respect rate limits
2. Use appropriate delays between requests
3. Regularly update proxy list
4. Monitor terminal output for errors
5. Verify JSON output integrity

## Troubleshooting

### Common Issues

1. Proxy Connection Errors
   - Verify proxy credentials
   - Check proxy server status
   - Try different proxy from the list

2. 403 Forbidden Errors
   - Wait for proxy rotation
   - Verify request headers
   - Check for API changes

3. JSON Parsing Errors
   - Verify API response format
   - Check for incomplete responses
   - Ensure proper error handling

## Future Improvements

1. Add dynamic page numbers
2. Implement concurrent requests
3. Add data validation
4. Enhance error reporting
5. Implement data persistence

## License

This project is for educational purposes only. Ensure compliance with Carvana's terms of service when using this scraper.

## Disclaimer

This tool is for educational purposes only. Users are responsible for ensuring their use complies with Carvana's terms of service and applicable laws.