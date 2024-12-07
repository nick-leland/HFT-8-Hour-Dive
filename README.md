# HFT-8-Hour-Dive
8 Hour deep dive into HFT algorithms.

# General Idea

## Simulated Environment
In order to utilize the data in this space, we are going to be utilizing data that is a much longer rate then that which is _actual_ HFT data.

For instance, we will be utilizing **Insert Dataset Name Here** which is in time intervals of **INSERT TIME INTERVAL HERE**.  Actual market data is extremely expensive or difficult to obtain, therefore, we will instead be simulating this by applying a scaling time factor to our dataset and converting the **INSERT TIME INTERVAL HERE** to `ticks`.  These ticks are an arbitrary time point, but we will simulate ticks at a rate which will allow us to run algorithms directly on the market data.  This is known as **Event Driven Backtesting**, and it will allow us to use python (typically a very slow language) to understand and simulate some baseline HFT.  THis relies on the mathematical principle of **Scale Invariance**, assuming that regardless of our timeframe, we will still be capable of capturing the underlying market patterns by just _"Pretending"_ our data is at a higher timeframe.

Points for growth: 
- Price Movement Patterns could be different: No matter what, we are directly losing a point of capture within our system.  Some very minor things won't be picked up on.  
- Latency Simulation: Potentially add artificial delays into the system to account for latency, maybe predictions could decay based on required latency to improve overall timeline.

