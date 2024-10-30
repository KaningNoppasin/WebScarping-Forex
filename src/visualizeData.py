from datetime import datetime
import csv
import config

csv_file = config.csv_file

def read_csv():
    """Reads the CSV file and extracts bid and ask prices."""
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

            # Store converted prices back in the row
            row['bid_price'] = bid_price
            row['ask_price'] = ask_price
            data.append(row)

            # Update max and min values for bid and ask prices
            max_bid_price = max(max_bid_price, bid_price)
            min_bid_price = min(min_bid_price, bid_price)
            max_ask_price = max(max_ask_price, ask_price)
            min_ask_price = min(min_ask_price, ask_price)

    return data, max_bid_price, min_bid_price, max_ask_price, min_ask_price

def extract_prices(data):
    """Extracts opening and closing prices from the data."""
    bid_open = data[0]["bid_price"]
    ask_open = data[0]["ask_price"]
    latest_entry = data[-1]
    bid_close = latest_entry["bid_price"]
    bid_change = bid_close - bid_open

    return {
        "date": latest_entry["Date"],
        "time": latest_entry["Time"],
        "bid_open": bid_open,
        "bid_close": bid_close,
        "bid_change": bid_change,
        "ask_open": ask_open
    }

def display_statistics(stats):
    """Displays the statistics from a single dictionary argument."""
    print("Date:", stats["date"])
    print("Time:", stats["time"])
    print("Bid Open (BO):", stats["bid_open"])
    print("Bid High (BH):", stats["max_bid"])
    print("Bid Low (BL):", stats["min_bid"])
    print("Bid Close (BC):", stats["bid_close"])
    print("Bid Change (BCH):", stats["bid_change"])
    print("Ask Open (AO):", stats["ask_open"])
    print("Ask High (AH):", stats["max_ask"])
    print("Ask Low (AL):", stats["min_ask"])

def main():
    """Main function to read data, extract prices, and display results."""
    data, max_bid, min_bid, max_ask, min_ask = read_csv()
    results = extract_prices(data)

    # Prepare a single dictionary argument for display_statistics
    stats = {
        **results,
        "max_bid": max_bid,
        "min_bid": min_bid,
        "max_ask": max_ask,
        "min_ask": min_ask
    }

    display_statistics(stats)

if __name__ == "__main__":
    main()
