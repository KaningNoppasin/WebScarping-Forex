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

    instrument_heading = soup.find('div', class_='instrument-heading-section__pricing instrument-pricing')
    instrument_pricing_rates = instrument_heading.find('div', class_='instrument-pricing__rates')

    sell_value = instrument_pricing_rates.find('div', class_='instrument-pricing__bid').find('div', class_='instrument-pricing__rate-value').text
    buy_value = instrument_pricing_rates.find('div', class_='instrument-pricing__offer').find('div', class_='instrument-pricing__rate-value').text

    now = datetime.now()
    date_formatted = now.strftime('%Y-%m-%d')
    time_formatted = now.strftime('%H:%M:%S')

    bid_price = sell_value      # Sell price
    offer_price = buy_value     # Buy price

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
            time.sleep(50)
    except KeyboardInterrupt:
        print("\nProcess interrupted by the user. Exiting gracefully.")
    except Exception as err:
        print("Error:",err)
    finally:
        try:
            driver.quit()  # Ensure the WebDriver is closed on exit
        except Exception as err:
            print("Error:",err)

if __name__ == "__main__":
    main()
