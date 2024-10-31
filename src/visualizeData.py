from datetime import datetime
import csv
import config
import os
import schedule
import time

csv_file = config.csv_file
visualizeData_csv_file = config.visualizeData_csv_file
position_file = config.position_file
header_line = config.header_line

def load_last_position():
    """Load the last read position from the text file."""
    if os.path.exists(position_file):
        with open(position_file, 'r') as f:
            return int(f.read().strip())
    return 0  # Start from the beginning if the file doesn't exist

def save_last_position(position):
    """Save the last read position to the text file."""
    with open(position_file, 'w') as f:
        f.write(str(position))

def read_csv():
    """Reads the CSV file and extracts bid and ask prices."""
    last_position = load_last_position()
    data = []
    max_bid_price = float('-inf')
    min_bid_price = float('inf')
    max_ask_price = float('-inf')
    min_ask_price = float('inf')

    with open(csv_file, mode='r') as file:
        file.seek(last_position)

        # Skip header if resuming from a position other than the start
        if last_position == 0:
            file.readline()  # Skip the header line
        csv_reader = csv.DictReader(file,fieldnames=header_line.strip().split(','))
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
        last_position = file.tell()
        save_last_position(last_position)  # Save the new position

    return data, max_bid_price, min_bid_price, max_ask_price, min_ask_price

def extract_prices(data):
    """Extracts opening and closing prices from the data."""
    if not data:
        print("--- No new data to process. ---")
        return None  # Or handle this as needed
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
    print("#"*20, stats["time"],"#"*20)
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

def save_to_csv(stats):
    """Append data to the CSV file."""
    data_row = [
        stats["date"],
        stats["time"],
        stats["bid_open"],
        stats["max_bid"],
        stats["min_bid"],
        stats["bid_close"],
        stats["bid_change"],
        stats["ask_open"],
        stats["max_ask"],
        stats["min_ask"]
    ]
    with open(visualizeData_csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Write the header if the file is empty
        if file.tell() == 0:
            writer.writerow([
                "Date", "Time", "BO", "BH", "BL", "BC", "BCh", "AO", "AH", "AL"
            ])
        # Write the data row
        writer.writerow(data_row)

def main():
    """Main function to read data, extract prices, and display results."""
    data, max_bid, min_bid, max_ask, min_ask = read_csv()
    results = extract_prices(data)
    if not results:
        return None
    # Prepare a single dictionary argument for display_statistics
    stats = {
        **results,
        "max_bid": max_bid,
        "min_bid": min_bid,
        "max_ask": max_ask,
        "min_ask": min_ask
    }

    display_statistics(stats)
    save_to_csv(stats)

if __name__ == "__main__":
    # schedule.every(2).minutes.do(main)
    try:
        schedule.every(10).seconds.do(main)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nProcess interrupted by the user. Exiting gracefully.")
