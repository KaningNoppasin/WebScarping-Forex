from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json
import csv

# Specify the CSV file name
csv_file = './data/raw/data_.csv'

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

def read_csv_and_find_min_max():
    data = []
    max_bid_price = float('-inf')
    min_bid_price = float('inf')
    max_ask_price = float('-inf')
    min_ask_price = float('inf')

    with open(csv_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Convert bid and ask prices to floats
            bid_price = float(row['bid_price'])
            ask_price = float(row['ask_price'])

            # Append row data to list
            row['bid_price'] = bid_price
            row['ask_price'] = ask_price
            data.append(row)

            # Update max and min values for bid and ask prices
            max_bid_price = max(max_bid_price, bid_price)
            min_bid_price = min(min_bid_price, bid_price)
            max_ask_price = max(max_ask_price, ask_price)
            min_ask_price = min(min_ask_price, ask_price)

    return data, max_bid_price, min_bid_price, max_ask_price, min_ask_price

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

def convert_data_from_read_csv(data):
    """Extracts key values from the data for opening and closing prices."""
    bid_open = data[0]["bid_price"]
    ask_open = data[0]["ask_price"]
    latest_entry = data[-1]
    date, time = latest_entry["Date"], latest_entry["Time"]
    bid_close = latest_entry["bid_price"]
    bid_change = bid_close - bid_open

    return {
        "date": date,
        "time": time,
        "bid_open": bid_open,
        "bid_close": bid_close,
        "bid_change": bid_change,
        "ask_open": ask_open
    }

def display_results(results, max_bid, min_bid, max_ask, min_ask):
    """Displays the extracted key values and max/min statistics."""
    print("Date:", results["date"])
    print("Time:", results["time"])
    print("Bid Open (BO):", results["bid_open"])
    print("Bid High (BH):", max_bid)
    print("Bid Low (BL):", min_bid)
    print("Bid Close (BC):", results["bid_close"])
    print("Bid Change (BCH):", results["bid_change"])
    print("Ask Open (AO):", results["ask_open"])
    print("Ask High (AH):", max_ask)
    print("Ask Low (AL):", min_ask)

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
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nProcess interrupted by the user. Exiting gracefully.")
    finally:
        driver.quit()  # Ensure the WebDriver is closed on exit

if __name__ == "__main__":
    # main()
    # print(read_csv_file())

    data, max_bid, min_bid, max_ask, min_ask = read_csv_and_find_min_max()
    results = convert_data_from_read_csv(data)
    display_results(results, max_bid, min_bid, max_ask, min_ask)
