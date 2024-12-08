import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_series(series, title=None):
    plt.figure(figsize=(10, 6))
    plt.plot(series)
    plt.xlabel("Index")
    plt.ylabel("Value")
    if title:
        plt.title(title)
    else:
        plt.title("Time Series Plot")
    plt.grid(True)
    plt.show()

def adjust_price_series(df, jump_threshold=5, price_column='Typical Price'):
    previous = None
    adjustment = 0
    adjusted_ts = []
    
    for point in df[price_column]:
        if previous is not None:
            difference = abs(point - previous)
            
            if difference > jump_threshold:
                if point > previous:
                    adjustment -= difference
                else:
                    adjustment += difference
                    
        previous = point
        adjusted_ts.append(point + adjustment)
        
    return adjusted_ts

def adjusted_portion(input_df, stock_name, plot=False, adjusted_price=True):
    # Create a copy to avoid modifying original data
    input = input_df.copy()
    
    # Handle CSV file format
    if isinstance(input.index, pd.RangeIndex):  # This checks if it's a regular CSV import
        name = input.iloc[0].iloc[0]
        input.drop(0, inplace=True)
        input.drop(1, inplace=True)
        if 'Price' in input.columns:
            input.drop('Price', axis=1, inplace=True)
        input = input.reset_index(drop=True)
        
        # Convert columns to float
        input['High'] = input['High'].astype(float)
        input['Low'] = input['Low'].astype(float)
        input['Close'] = input['Close'].astype(float)
    else:  # Handle yfinance format
        if 'Price' in input.columns:
            input = input.drop('Price', axis=1)
        input = input.reset_index()
    
    # Calculate typical price using the actual columns
    input['Typical Price'] = (input['High'] + input['Low'] + input['Close']) / 3
    output = input['Typical Price']

    # Plot if requested
    if plot:
        plot_series(output, title=f"Time Series Plot - {stock_name}")
    
    if adjusted_price:
        output = adjust_price_series(input)
        output = pd.Series(output)
        if plot:
            plot_series(output, title=f"Time Series Plot Adjusted - {stock_name}")

    # Save to CSV
    os.makedirs("data", exist_ok=True)
    output.to_csv(f"data/{stock_name}.csv", index=False, header=False)
    return output

if __name__ == "__main__":
    input = pd.read_csv("TSLA.csv")
    adjusted_portion(input, "TSLA", plot=True)
