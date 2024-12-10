# HFT-8-Hour-Dive
8 Hour deep dive into HFT algorithms.

# General Idea

## Simulated Environment
In order to utilize the data in this space, we are going to be utilizing data that is a much longer rate then that which is _actual_ HFT data.

For instance, we will be utilizing **Insert Dataset Name Here** which is in time intervals of **INSERT TIME INTERVAL HERE**.  Actual market data is extremely expensive or difficult to obtain, therefore, we will instead be simulating this by applying a scaling time factor to our dataset and converting the **INSERT TIME INTERVAL HERE** to `ticks`.  These ticks are an arbitrary time point, but we will simulate ticks at a rate which will allow us to run algorithms directly on the market data.  This is known as **Event Driven Backtesting**, and it will allow us to use python (typically a very slow language) to understand and simulate some baseline HFT.  THis relies on the mathematical principle of **Scale Invariance**, assuming that regardless of our timeframe, we will still be capable of capturing the underlying market patterns by just _"Pretending"_ our data is at a higher timeframe.

![time_series_adjustment](https://github.com/user-attachments/assets/45bee1b4-e1cd-4826-9c9c-1c5e84c174c6)

Points for growth: 
- Price Movement Patterns could be different: No matter what, we are directly losing a point of capture within our system.  Some very minor things won't be picked up on.  
- Latency Simulation: Potentially add artificial delays into the system to account for latency, maybe predictions could decay based on required latency to improve overall timeline.

## Data Collection
We collect data by running the following command:

```
python data_collection.py
```

You will then need to give which stock symbols you would like to collect by giving the symbols in the following format:

```
SYMBOL1, SYMBOL2, SYMBOL3, ..., SYMBOLN
```

## Visualization
You can also visualize with the following command:
```
python plot_series.py your_data.csv
```
Where `your_data.csv` is a file that you collected through the Data Collection function. 

## Gamification

To run the gamification of the files, run the following command:

```
python market_visualizer_pygame.py < data/TSLA.csv
```

This is a simplified PyGame file that runs a simulation of the scraped data. 
<img width="801" alt="Screenshot 2024-12-07 at 10 34 57 PM" src="https://github.com/user-attachments/assets/77211bb1-672e-433b-9eff-5b224d28561a">


# Continuation
Impliment this [Autoregressive Integrated Moving Average](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average)
Long Short-Term Memory Machine Learning
