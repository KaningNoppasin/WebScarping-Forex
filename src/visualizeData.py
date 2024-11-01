from datetime import datetime
import csv
import config
import os
import schedule
import time

csv_file = config.csv_file
visualizeData_csv_files = {
    10: config.visualizeData_csv_file_10,
    30: config.visualizeData_csv_file_30,
    60: config.visualizeData_csv_file_60
}
position_files = {
    10: config.position_file_10,
    30: config.position_file_30,
    60: config.position_file_60
}
header_line = config.header_line

def load_last_position(position_file):
    """Load the last read position from the text file for a given interval."""
    if os.path.exists(position_file):
        with open(position_file, 'r') as f:
            return int(f.read().strip())
    return 0

def save_last_position(position, position_file):
    """Save the last read position to the text file for a given interval."""
    with open(position_file, 'w') as f:
        f.write(str(position))

def read_csv(interval):
    """Reads the CSV file and extracts bid and ask prices for a specific interval."""
    last_position = load_last_position(position_files[interval])
    data = []
    max_bid_price = float('-inf')
    min_bid_price = float('inf')
    max_ask_price = float('-inf')
    min_ask_price = float('inf')

    with open(csv_file, mode='r') as file:
        file.seek(last_position)

        if last_position == 0:
            file.readline()
        csv_reader = csv.DictReader(file, fieldnames=header_line.strip().split(','))
        for row in csv_reader:
            bid_price = float(row['bid_price'])
            ask_price = float(row['ask_price'])
            row['bid_price'] = bid_price
            row['ask_price'] = ask_price
            data.append(row)

            max_bid_price = max(max_bid_price, bid_price)
            min_bid_price = min(min_bid_price, bid_price)
            max_ask_price = max(max_ask_price, ask_price)
            min_ask_price = min(min_ask_price, ask_price)
        last_position = file.tell()
        save_last_position(last_position, position_files[interval])

    return data, max_bid_price, min_bid_price, max_ask_price, min_ask_price

def extract_prices(data):
    """Extracts opening and closing prices from the data."""
    if not data:
        print("--- No new data to process. ---")
        return None
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

def display_statistics(stats, interval):
    """Displays the statistics for a specific interval."""
    print("#"*20, f"{stats['time']} - {interval} min", "#"*20)
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

def save_to_csv(stats, interval):
    """Append data to the CSV file for a specific interval."""
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
    file_name = visualizeData_csv_files[interval]
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow([
                "Date", "Time", "BO", "BH", "BL", "BC", "BCh", "AO", "AH", "AL"
            ])
        writer.writerow(data_row)

def main(interval):
    """Main function to read data, extract prices, and display results for a specific interval."""
    print("=> interval:",interval)
    data, max_bid, min_bid, max_ask, min_ask = read_csv(interval)
    results = extract_prices(data)
    if not results:
        return None
    stats = {
        **results,
        "max_bid": max_bid,
        "min_bid": min_bid,
        "max_ask": max_ask,
        "min_ask": min_ask
    }

    display_statistics(stats, interval)
    save_to_csv(stats, interval)

if __name__ == "__main__":
    schedule.every(10).minutes.do(lambda: main(10))
    schedule.every(30).minutes.do(lambda: main(30))
    schedule.every(60).minutes.do(lambda: main(60))

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nProcess interrupted by the user. Exiting gracefully.")
