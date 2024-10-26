import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data from your file
df = pd.read_csv('./data/raw/data.csv')

# Convert 'Date' and 'Time' to datetime
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])

# Create a plot with multiple columns
plt.figure(figsize=(12, 8))

# Plot each column
plt.plot(df['Datetime'], df['Sell'], label='Sell Price', marker='o')
plt.plot(df['Datetime'], df['Buy'], label='Buy Price', marker='o')
plt.plot(df['Datetime'], df['Spread'], label='Spread', marker='o')
plt.plot(df['Datetime'], df['Low'], label='Low Price', marker='o')
plt.plot(df['Datetime'], df['Change'], label='Change', marker='o')
plt.plot(df['Datetime'], df['High'], label='High Price', marker='o')
plt.plot(df['Datetime'], df['Sell (Bid Price)'], label='Sell (Bid Price)', marker='o')
plt.plot(df['Datetime'], df['Buy (Offer Price)'], label='Buy (Offer Price)', marker='o')
plt.plot(df['Datetime'], df['Low Price'], label='Low Price', marker='o')
plt.plot(df['Datetime'], df['Change in Points'], label='Change in Points', marker='o')
plt.plot(df['Datetime'], df['High Price'], label='High Price', marker='o')
plt.plot(df['Datetime'], df['Change Percentage'].str.rstrip('%').astype('float') / 100, label='Change Percentage', marker='o')

# Set plot labels and title
plt.xlabel('Datetime')
plt.ylabel('Values')
plt.title('Financial Data Plot')
plt.legend()

# Display the plot
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
