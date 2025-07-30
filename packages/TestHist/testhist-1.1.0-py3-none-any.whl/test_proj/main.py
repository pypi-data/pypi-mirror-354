# histogram_example.py

import matplotlib.pyplot as plt
import pandas as pd

def generate_histogram(data, bins=10):
    """
    Generates and displays a histogram for the given data.

    Parameters:
    - data: List of numerical values to be plotted.
    - bins: Number of bins in the histogram.
    """
    # Create a histogram
    plt.hist(data, bins=bins, edgecolor='black')

    # Add a title and labels
    plt.title('Histogram of Sample Data')
    plt.xlabel('Value')
    plt.ylabel('Frequency')

    # Show the plot
    plt.show()

def main():
    # Sample data
    data = [23, 45, 56, 78, 33, 44, 56, 23, 89, 90, 12, 67, 43, 56, 78]
    
    # Generate and display the histogram
    generate_histogram(data)

if __name__ == "__main__":
    main()
