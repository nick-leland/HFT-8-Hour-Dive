import pandas as pd
import matplotlib.pyplot as plt

def plot_csv_series(filename, has_header=False):
    # Read the CSV file
    if has_header:
        data = pd.read_csv(filename)
    else:
        data = pd.read_csv(filename, header=None, names=['value'])
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(data['value'])
    
    # Customize the plot
    plt.title(f"Time Series Plot - {filename}")
    plt.xlabel("Time Steps")
    plt.ylabel("Value")
    plt.grid(True)
    
    # Show the plot
    plt.show()
    
    return data

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python plot_series.py <filename.csv>")
        sys.exit(1)
        
    filename = sys.argv[1]
    try:
        data = plot_csv_series(filename)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except Exception as e:
        print(f"Error: {str(e)}")
