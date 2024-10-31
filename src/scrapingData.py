from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json
import csv
import config

csv_file = config.csv_file

def initialize_driver():
    """Initialize the WebDriver."""
    driver = webdriver.Chrome()
    return driver

def scrape_data(driver):
    """Scrape forex data from the webpage."""
    # Open the URL
    driver.get("https://www.forex.com/en/forex-trading/eur-usd/")

    # Pause to ensure the page loads fully
    time.sleep(5)

    # Get the page source
    html = driver.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    now = datetime.now()
    date_formatted = now.strftime('%Y-%m-%d')
    time_formatted = now.strftime('%H:%M:%S')

    pricing_div = soup.find('div', class_='instrument-heading-section__pricing')
    data_initial_data = pricing_div['data-initial-data']
    pricing_data = json.loads(data_initial_data)

    bid_price = pricing_data['ratesFields'][0]['fieldValue']  # Sell price
    offer_price = pricing_data['ratesFields'][1]['fieldValue']  # Buy price

    data_row = [
        date_formatted,
        time_formatted,
        bid_price,      # BO
        offer_price,    # AO = ask price
    ]

    return data_row


def save_to_csv(data_row):
    """Append data to the CSV file."""
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Write the header if the file is empty
        if file.tell() == 0:
            writer.writerow([
                "Date", "Time", "bid_price", "ask_price"
            ])
        # Write the data row
        writer.writerow(data_row)

def print_data_form_scrape(data_row):
    """Print the data to the console."""
    print("#"*20,data_row[1],"#"*20)
    print("Date:", data_row[0])
    print("Time:", data_row[1])
    print("bid_price:", data_row[2])
    print("ask_price:", data_row[3])

def main():
    """Main function to run the scraper."""
    driver = initialize_driver()

    try:
        while True:
            data_row = scrape_data(driver)
            save_to_csv(data_row)
            print_data_form_scrape(data_row)

            # Wait for 10 seconds before the next iteration
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nProcess interrupted by the user. Exiting gracefully.")
    finally:
        driver.quit()  # Ensure the WebDriver is closed on exit

if __name__ == "__main__":
    main()
