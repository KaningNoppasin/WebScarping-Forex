from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json
import csv

# Specify the CSV file name
csv_file = './data/raw/data.csv'

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
    instrument_pricing_content = instrument_heading.find('div', class_='instrument-pricing__content')
    instrument_pricing_value = instrument_pricing_content.find_all('span', class_='instrument-pricing__value')

    sell_value = instrument_pricing_rates.find('div', class_='instrument-pricing__bid').find('div', class_='instrument-pricing__rate-value').text
    buy_value = instrument_pricing_rates.find('div', class_='instrument-pricing__offer').find('div', class_='instrument-pricing__rate-value').text
    spread_value = instrument_heading.find('div', class_='instrument-pricing__spread').text

    low_value = instrument_pricing_value[0].text
    change_value = instrument_pricing_value[1].text
    high_value = instrument_pricing_value[2].text
    change_percentage_value = instrument_pricing_value[3].text

    now = datetime.now()
    date_formatted = now.strftime('%Y-%m-%d')
    time_formatted = now.strftime('%H:%M:%S')

    pricing_div = soup.find('div', class_='instrument-heading-section__pricing')
    data_initial_data = pricing_div['data-initial-data']
    pricing_data = json.loads(data_initial_data)

    bid_price = pricing_data['ratesFields'][0]['fieldValue']  # Sell price
    offer_price = pricing_data['ratesFields'][1]['fieldValue']  # Buy price
    low_price = pricing_data['pricingFields'][0]['fieldValue']  # Low price
    change_points = pricing_data['pricingFields'][1]['fieldValue']  # Change in points
    high_price = pricing_data['pricingFields'][2]['fieldValue']  # High price
    change_percentage = pricing_data['pricingFields'][3]['fieldValue']  # Change percentage

    data_row = [
        date_formatted,
        time_formatted,
        sell_value,
        buy_value,
        spread_value,
        low_value,
        change_value,
        high_value,
        change_percentage_value,
        bid_price,
        offer_price,
        low_price,
        change_points,
        high_price,
        change_percentage,
    ]

    return data_row

def save_to_csv(data_row):
    """Append data to the CSV file."""
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Write the header if the file is empty
        if file.tell() == 0:
            writer.writerow([
                "Date", "Time", "Sell", "Buy", "Spread", "Low", 
                "Change", "High", "Change %", "Sell (Bid Price)", 
                "Buy (Offer Price)", "Low Price", "Change in Points", 
                "High Price", "Change Percentage"
            ])
        # Write the data row
        writer.writerow(data_row)

def print_data(data_row):
    """Print the data to the console."""
    print("#"*20,data_row[1],"#"*20)
    print("Date:", data_row[0])
    print("Time:", data_row[1])
    print("Sell:", data_row[2])
    print("Buy:", data_row[3])
    print("Spread:", data_row[4])
    print("Low:", data_row[5])
    print("Change:", data_row[6])
    print("High:", data_row[7])
    print("Change %:", data_row[8])
    print("Sell (Bid Price):", data_row[9])
    print("Buy (Offer Price):", data_row[10])
    print("Low Price:", data_row[11])
    print("Change in Points:", data_row[12])
    print("High Price:", data_row[13])
    print("Change Percentage:", data_row[14])

def main():
    """Main function to run the scraper."""
    driver = initialize_driver()

    try:
        while True:
            data_row = scrape_data(driver)
            save_to_csv(data_row)
            print_data(data_row)

            # Wait for 10 seconds before the next iteration
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nProcess interrupted by the user. Exiting gracefully.")
    finally:
        driver.quit()  # Ensure the WebDriver is closed on exit

if __name__ == "__main__":
    main()
    # driver = initialize_driver()
    # driver.get("https://www.forex.com/en/forex-trading/eur-usd/")
    # time.sleep(120)